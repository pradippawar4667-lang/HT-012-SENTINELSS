from pynput import keyboard
import time
import csv

class TypingCollector:
    def __init__(self):
        self.data = []
        self.last_time = None
        
    def on_press(self, key):
        current_time = time.time()
        if self.last_time:
            # Calculate time between keys (flight time)
            flight_time = current_time - self.last_time
            self.data.append([current_time, 'PRESS', str(key), flight_time])
        self.last_time = current_time
        
    def on_release(self, key):
        # Record key release
        self.data.append([time.time(), 'RELEASE', str(key), 0])
        if key == keyboard.Key.esc:
            return False  # Stop on ESC

    def save_data(self):
        with open('typing_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'event', 'key', 'flight_time'])
            writer.writerows(self.data)
        print("Data saved to typing_data.csv")

# Start collecting
collector = TypingCollector()
print("Start typing! Press ESC to stop...")
with keyboard.Listener(
    on_press=collector.on_press,
    on_release=collector.on_release
) as listener:
    listener.join()

collector.save_data()