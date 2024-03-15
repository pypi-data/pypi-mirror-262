from src.olympiad_data_structures import number_theory
from src.olympiad_data_structures import PointVector
import time
from functools import reduce


def main():
    p1 = PointVector.PointVector(*[0, 1, 2])
    p2 = PointVector.PointVector(*[0, 1, 4])
    print(p1.distance(p2))

    n = 10**6
    sieve = number_theory.EratosthenesSieve(n)
    t1 = time.time()
    sieve.build()
    t2 = time.time()
    print(t2 - t1)
    k = int(input())
    print(sieve.is_prime(k), sieve.is_prime_sqrt_method(k))

    n = 10**5
    factorizer = number_theory.Factorizer()
    factorizer.build(n)
    k = int(input())
    factorization = factorizer.factorize(k)
    print("multiplication(", factorization, ") =", reduce(lambda x, y: x * y, factorization, 1))


    return 0


if __name__ == "__main__":
    main()
