"""Main module."""

from .data import Node
from datetime import datetime
from typing import Any
from .utility import get_logger


logger = get_logger(__name__)


class CircularQueue:

    def __init__(self, size: int) -> None:
        self._max_size = size
        self._write_ptr = 0
        self._read_ptr = 0
        self._container: list[Node] = [None] * self._max_size
        self._init_container()
        self._readbuffer = [None] * self._max_size
        pass

    def _init_container(self) -> None:

        for i in range(self._max_size):
            self._container[i] = Node.create_dummy()
        pass

    def add(self, content: Any) -> None:
        now = datetime.now()
        inx: int = self._write_ptr % self._max_size
        self._container[inx].replace_contents(self._write_ptr, now, content)
        self._write_ptr += 1
        pass

    def remove(self) -> Any:
        if self.is_empty():
            return None
        max_size: int = self._max_size
        new_read_ptr: int = self._get_read_inx_adj_overflow()
        content = self._container[new_read_ptr % max_size].get_payload()
        new_read_ptr += 1
        self._read_ptr = new_read_ptr
        return content

    def peek(self) -> Any:
        if self.is_empty():
            return None
        max_size: int = self._max_size
        peek_ptr: int = self._get_read_inx_adj_overflow()
        content = self._container[peek_ptr % max_size].get_payload()
        return content

    def peak(self) -> Any:
        if self.is_empty():
            return None
        max_size: int = self._max_size
        peek_ptr: int = self.get_last_write_ptr()
        content = self._container[peek_ptr % max_size].get_payload()
        return content

    def peak_n_recent_elements(self, n: int) -> list:
        max_size: int = self._max_size
        read_last_n_elements = min(n, self.length())
        last_element: int = self._write_ptr
        start_read_inx = last_element - read_last_n_elements
        return [
            self._container[i % max_size].get_payload()
            for i in range(start_read_inx, last_element)
        ]

    def _get_read_inx_adj_overflow(self) -> int:
        max_size: int = self._max_size
        cur_read_ptr: int = self._read_ptr
        dist: int = self._write_ptr - cur_read_ptr
        if dist < max_size:
            return cur_read_ptr
        # Penalty for overflow of circular queue
        # we need extra operation to skip elements
        adj: int = int(dist % max_size > 1)
        cur_read_ptr += dist - max_size + adj
        # logger.debug(f"read_ptr: {self._read_ptr}, inx: {inx}")
        return cur_read_ptr

    def length(self) -> int:
        return min(self._write_ptr - self._read_ptr, self._max_size)

    def size(self) -> int:
        return self._max_size

    def is_empty(self) -> bool:
        return self.length() == 0

    def reset(self) -> None:
        self._read_ptr = self._write_ptr = 0
        self._init_container()

    def get_last_write_ptr(self) -> int:
        return self._write_ptr - 1

    def get_last_read_ptr(self) -> int:
        return self._read_ptr - 1
