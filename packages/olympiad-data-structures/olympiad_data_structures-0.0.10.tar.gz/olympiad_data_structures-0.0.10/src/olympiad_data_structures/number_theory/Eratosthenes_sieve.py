from typing import List, Callable, Tuple
from bitarray import bitarray
from math import sqrt


class EratosthenesSieve:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.count_of_primes: int = 0
        self.prime: bitarray = bitarray(n)
        self.prime.setall(True)

    def build(self) -> None:
        self.prime[0] = False
        self.prime[1] = False
        for i in range(2, int(sqrt(self.n)) + 1):
            if self.prime[i]:
                self.count_of_primes += 1
                for j in range(i * i, self.n, i):
                    self.prime[j] = False

    def get_sieve_in_list(self) -> bitarray:
        return self.prime

    def is_prime(self, num: int) -> bool:
        return bool(self.prime[num])

    def get_length(self) -> int:
        return self.n

    def get_count_of_primes(self) -> int:
        return self.count_of_primes

    def go_through_prime_numbers(self, process_prime: Callable[[int], None]) -> None:
        for i in range(2, self.get_length()):
            if self.is_prime(i):
                process_prime(i)

    def get_prime_numbers(self) -> List[int]:
        answer: List[int] = []
        for i in range(2, self.get_length()):
            if self.is_prime(i):
                answer.append(i)
        return answer

    def go_through_prime_numbers_with_their_multiples(
            self, process_prime: Callable[[int], None],
            get_prime_and_multiple: Callable[[int, int], None]) -> None:
        for i in range(2, self.get_length()):
            if self.is_prime(i):
                process_prime(i)
                for j in range(i * i, self.get_length(), i):
                    get_prime_and_multiple(i, j)

    @staticmethod
    def is_prime_sqrt_method(n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        sq: int = int(sqrt(n))
        for i in range(3, sq + 1, 2):
            if n % i == 0:
                return False
        return True


def get_goldbach_expansion(n: int) -> Tuple[int, int]:
    prime: EratosthenesSieve = EratosthenesSieve(n)
    prime.build()

    for i in range(2, n + 1):
        if not prime.is_prime(i):
            continue
        j: int = n - i
        if not prime.is_prime(j):
            continue
        return i, j
    return 0, 0


def make_sure_that_bertrand_postulate_is_correct(n: int, search_all: bool = False) -> List[int]:
    prime: EratosthenesSieve = EratosthenesSieve(2 * n + 1)
    prime.build()
    primes: List[int] = []
    j: int = n + 1
    while j < 2 * n:
        if prime.is_prime(j):
            primes.append(j)
            if not search_all:
                return primes
            break
        j += 1
    j += 1
    while j < 2 * n:
        if prime.is_prime(j):
            primes.append(j)
        j += 1
    return primes
