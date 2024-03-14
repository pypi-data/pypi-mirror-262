"""Module for converting a SAS database in the sas7bdat file format"""

from __future__ import annotations

import os
import time
import math
import logging
import threading
from pathlib import Path

import pyreadstat  # type: ignore
import pyarrow.parquet as pq  # type: ignore

_MODULE_LOGGER = logging.getLogger(__name__)
_MODULE_LOGGER.addHandler(logging.NullHandler())


class Converter:
    """Class to convert a database directory containing SAS files to another format"""

    def __init__(self, db_path: Path = Path.cwd(), target_in_memory_size=1e8) -> None:
        self.db_path = db_path
        self.target_in_memory_size = target_in_memory_size
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.logger.debug("Converter: initialized to %s", self.db_path)

    @staticmethod
    def _get_sas_path(parquet_path: Path) -> Path:
        """
        Returns a Path to the SAS file corresponding to the input parquet file

        :param parquet_path: the path to the parquet file to find the
        corresponding SAS file for
        :returns: Path to SAS file
        """

        return parquet_path.parent.joinpath(
            f"{parquet_path.name.removesuffix('.parquet')}.sas7bdat"
        )

    @staticmethod
    def _get_parquet_path(sas_path: Path) -> Path:
        """
        Returns a Path to the parquet file corresponding to the input SAS file

        :param sas_path: the path to the SAS file to find the corresponding
        parquet file for
        :returns: Path to parquet file
        """

        parquet_path = sas_path.parent.joinpath(
            f"{sas_path.name.removesuffix('.sas7bdat')}.parquet"
        )
        return parquet_path

    def _get_chunk_size(self, sas_path: Path) -> int:
        """
        Returns the optimal chunk size for reading a SAS file.
        Estimates the number of rows that will keep the in-memory
        size of the chunk close to target_in_memory_size.

        :param sas_path: the Path to the SAS file to calculate chunk size for.
        :returns: an integer number of rows to include in each chunk.
        """

        row, _ = next(
            pyreadstat.read_file_in_chunks(
                pyreadstat.read_sas7bdat, sas_path, chunksize=1
            )
        )
        size = row.memory_usage(index=True, deep=True).sum()
        return math.floor(self.target_in_memory_size / size)

    def _convert_sas(self, sas_path: Path) -> Path:
        """Converts a SAS file and returns the path to the generated parquet file"""

        log_prefix = "Converter._convert_sas"

        chunk_size = self._get_chunk_size(sas_path)
        self.logger.debug(
            "%s: chunk size for %s set to %d", log_prefix, sas_path, chunk_size
        )

        chunk_iterator = pyreadstat.read_file_in_chunks(
            pyreadstat.read_sas7bdat, sas_path, chunksize=chunk_size
        )
        parquet_path = Converter._get_parquet_path(sas_path)
        if parquet_path.exists():
            self.logger.error(
                "%s: aborted because %s already exists", log_prefix, parquet_path
            )
            raise FileExistsError(f"{parquet_path} already exists")
        start_time = time.perf_counter()
        for index, (chunk, _) in enumerate(chunk_iterator):
            if index == 0:
                chunk.to_parquet(parquet_path, engine="fastparquet", index=False)
            else:
                chunk.to_parquet(
                    parquet_path, engine="fastparquet", index=False, append=True
                )
            end_time = time.perf_counter()
            self.logger.debug(
                "%s.iteration: %d, %d", log_prefix, index, end_time - start_time
            )
            start_time = time.perf_counter()

        return parquet_path

    def _validate_chunk(self, chunk) -> bool:
        """
        Determines whether two chunks (SAS and parquet) are equals

        :param chunk: should contain the SAS and parquet chunks in the following
        format: (SAS: pd.DataFrame, _), parquet: pyarrow.RecordBatch
        :returns: whether the chunks are equal (bool)
        """

        (sas_frame, _), parquet_batch = chunk
        parquet_frame = parquet_batch.to_pandas()
        return sas_frame.equals(parquet_frame)

    def _validate_parquet_file(self, parquet_path: Path) -> bool:
        """
        Returns whether the parquet file matches the corresponding SAS file

        :param parquet_path: the parquet file to validate
        :returns: (bool) whether the parquet file is a copy of the SAS file or
        not
        """

        log_prefix = "Converter._validate_parquet_file"

        sas_path = Converter._get_sas_path(parquet_path)
        parquet_file = pq.ParquetFile(parquet_path)

        # Divide by two because two chunks will be read simultaneously
        chunk_size = math.floor(self._get_chunk_size(sas_path) / 2)

        self.logger.debug(
            "%s: chunk size for %s set to %d", log_prefix, sas_path, chunk_size
        )
        sas_iter = pyreadstat.read_file_in_chunks(
            pyreadstat.read_sas7bdat, sas_path, chunksize=chunk_size
        )
        parquet_iter = parquet_file.iter_batches(batch_size=chunk_size)

        results = set()
        start_time = time.perf_counter()
        combined_chunk_iterable = enumerate(zip(sas_iter, parquet_iter))
        for index, chunk in combined_chunk_iterable:
            results.add(self._validate_chunk(chunk))
            end_time = time.perf_counter()
            self.logger.debug(
                "%s.iteration: %d, %d", log_prefix, index, end_time - start_time
            )
            start_time = time.perf_counter()

        return False not in results

    def convert_sas(self, sas_path: Path, delete: bool = False) -> bool:
        """
        Converts the input SAS file and deletes it if the conversion is
        successful.  Returns True upon success. Returns False if validation
        fails.

        :param sas_path: the Path to the file to convert
        :returns: success of the operation (bool)
        """

        log_prefix = "Converter.convert_sas"

        parquet_path = self._convert_sas(sas_path)
        if not self._validate_parquet_file(parquet_path):
            self.logger.error(
                "%s: %s failed due to failed validation", log_prefix, sas_path
            )
            return False

        if delete:
            sas_path = Converter._get_sas_path(parquet_path)
            with open(sas_path, "w", encoding="utf-8"):
                pass
            os.remove(sas_path)
            self.logger.info("%s: file %s deleted", log_prefix, sas_path)

        return True

    class ConvertThread(threading.Thread):
        """Helper class to create a thread for convert_sas_database"""

        def __init__(
            self,
            thread_id: int,
            converter: Converter,
            sas_path: Path,
            result_set: set,
        ) -> None:
            threading.Thread.__init__(self)
            self.thread_id = thread_id
            self.converter = converter
            self.sas_path = sas_path
            self.result_set = result_set

        def run(self) -> None:
            print(f"thread {self.name} started")
            self.result_set.add(self.converter.convert_sas(self.sas_path))

    def convert_sas_database(self) -> bool:
        """
        Converts all SAS files in the input directory and deletes the original
        files. Returns the success of the entire conversion.

        :returns: True if all conversions succeeded, False otherwise
        """

        sas_paths = sorted(list(self.db_path.glob("*.sas7bdat")))
        conversion_results: set = set()
        threads = [
            Converter.ConvertThread(index, self, sas_path, conversion_results)
            for index, sas_path in enumerate(sas_paths)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return False not in conversion_results
