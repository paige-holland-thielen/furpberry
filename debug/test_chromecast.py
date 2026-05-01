import time
from furpberry.util.google_home import GoogleHome


gh = GoogleHome("furby")

# Print basic info
print("Cast status:", gh.cast.status)
print("\nNamespaces:", gh.cast.status.namespaces)

# Get media controller info
mc = gh.cast.media_controller
print(f"\nMedia controller status: {mc.status.player_state}")
print(f"App: {gh.cast.app_display_name}")

# Listen for messages
print("\n--- Listening for 30 seconds (try pausing/playing music) ---")
print(gh.read_status())
time.sleep(10)
print(gh.read_status())
time.sleep(10)
print(gh.read_status())
time.sleep(10)
print(gh.read_status())
time.sleep(10)
print(gh.read_status())
time.sleep(10)
print(gh.read_status())
gh.stop()