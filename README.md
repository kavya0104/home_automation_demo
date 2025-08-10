# 🏠 Home Automation Demo in Python

A simple yet feature-rich **Home Automation System** built with Python, featuring:
- ✅ GUI Control (Tkinter)
- 🎙 Voice Commands (SpeechRecognition)
- 📡 IoT MQTT Messaging (paho-mqtt)
- 💡 Raspberry Pi GPIO Support for Real Devices

---

## 📦 Features
1. **Graphical User Interface** – Control devices with buttons.
2. **Voice Commands** – Speak "Turn on light" or "Turn off fan".
3. **MQTT IoT Messaging** – Sends device updates to an MQTT broker.
4. **Raspberry Pi GPIO** – Real hardware control for LEDs, fans, etc.

---

## 🚀 Installation      
**Install dependencies:** *pip install -r requirements.txt*     
>[!TIP]
>**Note:** On Raspberry Pi,   
also run: *pip install RPi.GPIO*

▶ **Usage :**   
python home_automation.py

**🎙 Voice Commands:**  
Examples:  
*Turn on light,   
*Turn off fan,   
*Switch on AC.  

**🌐 MQTT Setup:**  
The project uses a public broker:  
1.Broker: test.mosquitto.org  
2.Topic: home/demo/device  

```
**🔌 Raspberry Pi GPIO Mapping**   

    **Device**	**GPIO Pin**
     Light   	  17
     Fan	      27
     AC	          22
     TV	          23




### 1️⃣ Clone the repository
bash
git clone https://github.com/kavya0104/home-automation-demo.git
cd home-automation-demo
