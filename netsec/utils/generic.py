def is_prime(num):
    # deliberately not efficient
    for i in range(2, num - 1):
        if num % i == 0:
            return False
    return True
