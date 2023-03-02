import time


def print_two():
    print(start)

if __name__ == '__main__':
    start = time.time()
    print_two()
    for i in range(2000000):
        i += 1
        print(i)
    print(time.time() - start)
