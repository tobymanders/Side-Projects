from pynput import keyboard
import time
from plexapi.myplex import MyPlexAccount
import pickle

# Credentials
account = MyPlexAccount('yadingus', 'N7PJgLYhg')
plex = account.resource('spergmaster').connect()
show = plex.library.section('TV Shows').search('Sunny')[0].episodes()[0]
client = plex.client('Living Room')
client.playMedia(show)

timepoints = []
print('Starting timer now.')
start = time.time()
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        timepoint = time.time()
        timepoints.append(timepoint - start)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    if key == keyboard.Key.esc:
        # Write timepoints
        with open('/Users/cytology/Documents/code/video_editing/clips/timepoints', 'wb') as cr:
        	pickle.dump(timepoints, cr)

        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

print(timepoints)