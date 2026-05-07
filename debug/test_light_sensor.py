import time

from furpberry.util.light_sensor import LightSense

ls = LightSense()

print("Testing light sensor and printing output, press CTRL+C to exit")
try:
    while True:
        print(ls.measure())
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")
