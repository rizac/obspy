# -*- coding: utf-8 -*-
from io import BytesIO

import numpy as np

from obspy.core.util import open_bytes_stream, from_bytes_stream
from .record import WtnRecord, WthRecord
from .define import SIZE_WT_HEADER


class _WtTape(object):
    def __init__(self):
        self._record = None
        self._handle = None

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self, filename):
        if isinstance(filename, BytesIO):
            filename.seek(0)
            return filename
        else:
            self._handle = open_bytes_stream(filename)
        return self

    def close(self):
        self._handle.close()


class WtnTape(_WtTape):

    def __next__(self):
        self._record = from_bytes_stream(self._handle, dtype=np.uint8)
        if self._record.size == 0:
            raise StopIteration()
        if np.array_equal(self._record[0:SIZE_WT_HEADER],
                          self._record[SIZE_WT_HEADER:SIZE_WT_HEADER * 2]):
            return WtnRecord(self._record[SIZE_WT_HEADER:])
        return WtnRecord(self._record)


class WthTape(_WtTape):

    def __next__(self):
        self._record = from_bytes_stream(self._handle, dtype=np.uint8)
        if self._record.size == 0:
            raise StopIteration()
        if np.array_equal(self._record[0:SIZE_WT_HEADER],
                          self._record[SIZE_WT_HEADER:SIZE_WT_HEADER * 2]):
            return WthRecord(self._record[SIZE_WT_HEADER:])
        return WthRecord(self._record)