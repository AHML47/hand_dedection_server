from camera import CameraHelper
from detector import HandDetector
from streamer import StreamerHTTP
import threading
import requests
import time
import cv2
from queue import Queue

streamer=StreamerHTTP('index.html')
detector=HandDetector()
cam=CameraHelper()
cam.start()

leds = [f"led{i}" for i in range(5)]
led_Que = Queue()
NODEMCU_URL = "http://192.168.1.102:80"

def turn_led_control():
    while True:
        print(list(led_Que.queue))
        for i in range(5):
            # Check if the LED index is in the queue
            if i in list(led_Que.queue):
                # Send a request to turn the LED on
                try:
                    response = requests.get(f"{NODEMCU_URL}/led?{leds[i]}=on")
                    if response.status_code == 200:
                        print(f"LED {i} turned on: {response.text}")
                    else:
                        print(f"Failed to turn on LED {i}: {response.status_code}")
                    led_Que.queue.remove(i)
                except Exception as e:
                    print(f"Error while turning on LED {i}: {e}")
            else:
                # Send a request to turn the LED off
                try:
                    response = requests.get(f"{NODEMCU_URL}/led?{leds[i]}=off")
                    if response.status_code == 200:
                        print(f"LED {i} turned off: {response.text}")
                    else:
                        print(f"Failed to turn off LED {i}: {response.status_code}")
                except Exception as e:
                    print(f"Error while turning off LED {i}: {e}")

        # Add a delay to avoid spamming the server
        time.sleep(0.1)

def generate_frames():

    while True:
        # Capture frame-by-frame
        frame = cam.capture_arrays()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = detector.process_image(frame,led_Que)
        print(list(led_Que.queue))


        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame in multipart format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

if __name__ == '__main__':
    try:
        threading.Thread(target=turn_led_control, daemon=True).start()
        streamer.run(5000, generate_frames)
    finally:
        cam.strop()
        print('Closing video feed')


