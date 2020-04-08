def is_prime(num):
    # deliberately not efficient
    result = True
    for i in range(2, num - 1):
        if num % i == 0:
            result = False
    return result
