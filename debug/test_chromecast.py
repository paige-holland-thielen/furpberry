from furpberry.util.logger import configure_logging
import time
from furpberry.util.google_home import GoogleHome

configure_logging("DEBUG")
gh = GoogleHome("furby")

print("Testing chromecast interactions and printing output, press CTRL+C to exit. "
      "Also play/pause music or whatever during this test to see things change")
try:
    while True:
        print(f"Google home PLAYING: {gh.read_status()}")
        time.sleep(3)
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")
finally:
    gh.stop()
