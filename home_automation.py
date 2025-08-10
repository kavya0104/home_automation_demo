"""
Home Automation Demo Project
Features:
- GUI control (tkinter)
- Voice control (speech_recognition)
- IoT MQTT publishing (paho-mqtt)
- Raspberry Pi GPIO control (optional)
"""

import tkinter as tk
import threading
import time

# Optional imports (may not be available on all systems)
try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import paho.mqtt.client as mqtt
except Exception:
    mqtt = None

try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except Exception:
    RPI_AVAILABLE = False

# ===== CONFIG =====
MQTT_BROKER = "test.mosquitto.org"  # Public broker for demo (change for production)
MQTT_PORT = 1883
MQTT_TOPIC = "home/demo/device"

devices = {
    "Light": False,
    "Fan": False,
    "AC": False,
    "TV": False
}

# ===== GPIO SETUP (Only if on Raspberry Pi) =====
GPIO_PINS = {
    "Light": 17,
    "Fan": 27,
    "AC": 22,
    "TV": 23
}

if RPI_AVAILABLE:
    GPIO.setmode(GPIO.BCM)
    for pin in GPIO_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# ===== MQTT SETUP =====
mqtt_client = None
if mqtt is not None:
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print("Connected to MQTT broker:", MQTT_BROKER)
    except Exception as e:
        print("Warning: MQTT connection failed:", e)
        mqtt_client = None
else:
    print("paho-mqtt not installed; MQTT features disabled.")

# ===== DEVICE CONTROL FUNCTIONS =====
def publish_state(device_name):
    state = "ON" if devices[device_name] else "OFF"
    payload = f"{device_name} {state}"
    if mqtt_client:
        try:
            mqtt_client.publish(MQTT_TOPIC, payload)
        except Exception as e:
            print("MQTT publish failed:", e)
    print(payload)

def set_device(device_name, on_off):
    """Set device state to True (ON) or False (OFF)"""
    devices[device_name] = bool(on_off)
    # GPIO
    if RPI_AVAILABLE:
        pin = GPIO_PINS.get(device_name)
        if pin is not None:
            GPIO.output(pin, GPIO.HIGH if devices[device_name] else GPIO.LOW)
    publish_state(device_name)
    refresh_buttons()

def toggle_device(device_name):
    set_device(device_name, not devices[device_name])

# ===== VOICE CONTROL =====
def _voice_listen_and_handle():
    if sr is None:
        print("SpeechRecognition not available. Install 'speechrecognition' and 'pyaudio'.")
        return
    recognizer = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone unavailable:", e)
        return

    with mic as source:
        print("Listening... speak a command like 'turn on light' or 'turn off fan'.")
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("Heard:", text)
        handled = False
        for device in devices:
            dn = device.lower()
            if dn in text:
                if "on" in text or "turn on" in text or "switch on" in text:
                    set_device(device, True)
                    handled = True
                    break
                elif "off" in text or "turn off" in text or "switch off" in text:
                    set_device(device, False)
                    handled = True
                    break
        if not handled:
            print("No recognizable device + action found in the command.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Speech recognition service error:", e)
    except Exception as e:
        print("Voice command error:", e)

def voice_command_async():
    t = threading.Thread(target=_voice_listen_and_handle, daemon=True)
    t.start()

# ===== GUI =====
root = tk.Tk()
root.title("Home Automation Demo")
root.geometry("340x360")

header = tk.Label(root, text="Home Automation Demo", font=("Arial", 16))
header.pack(pady=10)

buttons = {}
status_labels = {}

def refresh_buttons():
    for device, btn in buttons.items():
        state = devices[device]
        btn.config(text=f"{device} — {'ON' if state else 'OFF'}")


for device in devices:
    frm = tk.Frame(root)
    frm.pack(pady=6, padx=12, fill='x')
    btn = tk.Button(frm, text=f"{device} — OFF", width=22, command=lambda d=device: toggle_device(d))
    btn.pack(side='left')
    buttons[device] = btn
    lbl = tk.Label(frm, text=" ", width=8, anchor='w')
    lbl.pack(side='left', padx=8)
    status_labels[device] = lbl

voice_btn = tk.Button(root, text="Voice Command (speak)", width=25, command=voice_command_async)
voice_btn.pack(pady=14)

info = tk.Label(root, text="MQTT broker: {}\nTopic: {}".format(MQTT_BROKER, MQTT_TOPIC))
info.pack(pady=6)

def on_close():
    if RPI_AVAILABLE:
        GPIO.cleanup()
    if mqtt_client:
        try:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        except Exception:
            pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# start gui loop
if __name__ == '__main__':
    refresh_buttons()
    root.mainloop()
