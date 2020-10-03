import math


class Math:

    def __init__(self):
        self.primenumbers = {}

    def is_prime(self, num):
        if num <= 3:
            if num == 2 or num == 3:
                self.primenumbers.__setitem__(num, True)
            else:
                self.primenumbers.__setitem__(num, False)
            return self.primenumbers[num]
        if num not in self.primenumbers.keys():
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    self.primenumbers.__setitem__(num, False)
                    break
                self.primenumbers.__setitem__(num, True)
        return self.primenumbers[num]


if __name__ == "__main__":
    m = Math()
    for i in range(100):
        m.is_prime(i)
    primes = []
    for k, v in m.primenumbers.items():
        if v:
            primes.append(k)
    print(primes)
