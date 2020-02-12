from melon import Melon
from genie import Genie
import multiprocessing
import time

if __name__ == "__main__":
    t1 = time.time()

    jobs = []

    pr1 = multiprocessing.Process(target=Melon().page_parse())
    pr2 = multiprocessing.Process(target=Genie().page_parse())

    pr1.start()
    pr2.start()

    pr1.join()
    pr2.join()

    t2 = time.time()

    print(t2 - t1)
