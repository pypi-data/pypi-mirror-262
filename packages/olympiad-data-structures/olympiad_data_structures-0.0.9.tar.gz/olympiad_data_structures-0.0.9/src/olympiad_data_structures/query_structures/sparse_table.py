from abc import ABC, abstractmethod
from typing import TypeVar, List, Callable
from ..number_theory import floor_log

T = TypeVar('T')

BinaryFunction = Callable[[T, T], T]


class ISparseTable[T](ABC):
    def __init__(self, v: List[T], func: BinaryFunction[T]) -> None:
        self._n = len(v)
        self._size = self._n
        self._log = floor_log.FloorLog.get_floor_log(self._n) + 1
        self._a = v[:]
        self._f = func
        self.initialize()

    @abstractmethod
    def initialize(self) -> None:
        pass

    @property
    def size(self) -> int:
        return self._size

    @property
    def count_of_levels(self) -> int:
        return self._log

    @abstractmethod
    def ask_value(self, left: int, right: int) -> T:
        pass


class SparseTableWithIdempotency[T](ISparseTable):
    def __init__(self, v: List[T], func: BinaryFunction[T]) -> None:
        self._sparse = []
        super().__init__(v, func)

    def initialize(self) -> None:
        self._sparse = [[0] * self._size for _ in range(self._log)]
        for j in range(self._n):
            self._sparse[0][j] = j
        for level in range(1, self._log):
            for i in range(self._n - (1 << level) + 1):
                self._sparse[level][i] = self._get_index(self._sparse[level - 1][i],
                                                         self._sparse[level - 1][i + (1 << (level - 1))])

    def _get_index(self, i: int, j: int) -> int:
        return i if self._f(self._a[i], self._a[j]) == self._a[i] else j

    def ask_index(self, left: int, right: int) -> int:
        length = right - left + 1
        level = floor_log.FloorLog.get_floor_log(length)
        left = self._sparse[level][left]
        right = self._sparse[level][right - (1 << level) + 1]
        return self._get_index(left, right)

    def ask_value(self, left: int, right: int) -> T:
        index = self.ask_index(left, right)
        return self._a[index]


class SparseTable[T](ISparseTable):
    def __init__(self, v: List[T], func: BinaryFunction[T]) -> None:
        self._sparse = []
        super().__init__(v, func)

    def initialize(self) -> None:
        self._sparse = [[0] * self._size for _ in range(self._log)]
        for j in range(self._n):
            self._sparse[0][j] = self._a[j]
        for level in range(1, self._log):
            for i in range(self._n - (1 << level) + 1):
                self._sparse[level][i] = self._f(self._sparse[level - 1][i],
                                                 self._sparse[level - 1][i + (1 << (level - 1))])

    def ask_value(self, left: int, right: int) -> T:
        result = self._sparse[0][left]
        left += 1
        for level in range(self._log, -1, -1):
            if left + (1 << level) - 1 <= right:
                result = self._f(result, self._sparse[level][left])
                left += (1 << level)
        return result
