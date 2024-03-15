from typing import List


class FloorLog:
    maximum_computed_logarithm: int = 1
    floor_log: List[int] = [0, 0]

    @staticmethod
    def initialize_to_or_clear_after(n: int) -> None:
        if n <= FloorLog.maximum_computed_logarithm:
            del FloorLog.floor_log[n + 1:]
            FloorLog.maximum_computed_logarithm = n
            return None

        if FloorLog.maximum_computed_logarithm < n:
            FloorLog.floor_log += [0] * (n - FloorLog.maximum_computed_logarithm)
            for i in range(FloorLog.maximum_computed_logarithm + 1, n + 1):
                FloorLog.floor_log[i] = FloorLog.floor_log[i // 2] + 1
            FloorLog.maximum_computed_logarithm = n

    @staticmethod
    def get_floor_log(n: int) -> int:
        FloorLog.initialize_to_or_clear_after(n)
        return FloorLog.floor_log[n]
