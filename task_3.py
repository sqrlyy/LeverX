from threading import Lock
import concurrent.futures


class Solution:
    def __init__(self):
        self.lock = Lock()
        self.value = 0

    def increment(self, arg):
        for i in range(arg):
            with self.lock:
                self.value += 1


def main():
    result = Solution()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = []
        for i in range(5):
            threads.append(executor.submit(result.increment, arg=100000))

    print("----------------------", result.value)


if __name__ == '__main__':
    main()