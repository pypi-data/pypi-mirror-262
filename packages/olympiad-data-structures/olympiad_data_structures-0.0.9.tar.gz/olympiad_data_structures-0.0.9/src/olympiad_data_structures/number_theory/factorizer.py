from typing import List
from .Eratosthenes_sieve import EratosthenesSieve


class Factorizer:
    def __init__(self) -> None:
        self.n: int = 0
        self.minimal_prime_divisors: List[int] = []

    def get_size(self) -> int:
        return self.n

    def is_prime(self, n: int) -> bool:
        return self.get_minimal_prime_divisor(n) == n

    def build(self, n: int) -> None:
        recommended_max_size: int = int(1e6)
        self.n = min(n, recommended_max_size)
        self.minimal_prime_divisors = [-1] * self.n
        sieve = EratosthenesSieve(self.get_size())
        sieve.build()
        sieve.go_through_prime_numbers_with_their_multiples(self._process_prime, self._add_min_divisor)

    def get_minimal_prime_divisor(self, n: int) -> int:
        return self.minimal_prime_divisors[n]

    def factorize(self, n: int, repetitions: bool = True) -> List[int]:
        if n >= self.get_size():
            if EratosthenesSieve.is_prime_sqrt_method(n):
                return [n]
        prime_factors: List[int] = []
        current_i: int = 0
        while n >= self.get_size() > current_i:
            if self.is_prime(current_i) and n % current_i == 0:
                count: int = 1
                minimal_prime_divisor: int = current_i
                n //= minimal_prime_divisor
                while n % minimal_prime_divisor == 0:
                    n //= minimal_prime_divisor
                    count += 1
                prime_factors.extend(((count - 1) * repetitions + 1) * [minimal_prime_divisor])
            current_i += 1
        if current_i >= self.get_size():
            if n >= self.get_size() and prime_factors:
                if EratosthenesSieve.is_prime_sqrt_method(n):
                    prime_factors.append(n)
                    return prime_factors
            while n >= self.get_size():
                if n % current_i == 0 and EratosthenesSieve.is_prime_sqrt_method(current_i):
                    count: int = 1
                    minimal_prime_divisor: int = current_i
                    n //= minimal_prime_divisor
                    while n % minimal_prime_divisor == 0:
                        n //= minimal_prime_divisor
                        count += 1
                    prime_factors.extend(((count - 1) * repetitions + 1) * [minimal_prime_divisor])
                current_i += 1
        while n > 1:
            count: int = 0
            minimal_prime_divisor: int = self.get_minimal_prime_divisor(n)
            while n % minimal_prime_divisor == 0:
                n //= minimal_prime_divisor
                count += 1
            prime_factors.extend(((count - 1) * repetitions + 1) * [minimal_prime_divisor])
        return prime_factors

    def _add_min_divisor(self, i: int, j: int) -> None:
        if self.minimal_prime_divisors[j] == -1:
            self.minimal_prime_divisors[j] = i

    def _process_prime(self, i: int) -> None:
        self.minimal_prime_divisors[i] = i
