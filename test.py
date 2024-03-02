import sys

counter = 0
while True:
    counter += 1
    sys.stdout.write(f"\r{str(counter)}")
    sys.stdout.flush()
