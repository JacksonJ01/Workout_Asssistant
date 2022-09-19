import sys
from time import time as t, sleep as s

# Hours, Minutes, Seconds
timed = [1, 0, 0]


def timer(timerFor):
    startTime = int(t())
    totalTime = (timerFor[0] * 3600) + \
                (timerFor[1] * 60) + \
                (timerFor[2])

    oldElapsed = None
    while True:
        currentTime = int(t())
        elapsed = currentTime - startTime

        if elapsed > totalTime:
            print("\rTimer Done")
            return True

        else:
            if oldElapsed != elapsed:
                oldElapsed = elapsed
                sys.stdout.write(f"\rTime Left: {totalTime - elapsed}")
                sys.stdout.flush()


# for x in range(5, 0, -1):
#     sys.stdout.write(f"\r{x}")
#     sys.stdout.flush()
#     s(1)

timer(timed)
