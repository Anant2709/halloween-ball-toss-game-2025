# 🚀 Quick Start Guide

## TL;DR - Get Your Game Running in 5 Minutes

### 1️⃣ Upload Arduino Code (2 minutes)
```
1. Open Arduino IDE
2. Open halloween_game.ino
3. Select Board: Tools > Board > ESP32 Dev Module
4. Select Port: Tools > Port > [Your ESP32 Port]
5. Click Upload button (→)
```

### 2️⃣ Install Python Requirements (1 minute)
```bash
cd /Users/juhi2/Desktop/AnantUNI/Bhav_halloween_game
pip3 install -r requirements.txt
```

### 3️⃣ Run the Game (30 seconds)
```bash
# Make sure Arduino IDE Serial Monitor is CLOSED!
python3 laptop_sound_player.py
```

### 4️⃣ Play!
Throw balls at your cardboard target. The script will auto-play sounds!

---

## 🎵 About Sounds

The game **works immediately** with built-in beep sounds that vary by point value:
- **100 points**: Jackpot fanfare (4 ascending beeps)
- **75 points**: Great job (3 ascending beeps)
- **50 points**: Good throw (2 beeps)
- **25 points**: Nice (single beep)

No sound files needed!

**Want custom sounds?** See `SOUND_RESOURCES.md` for free sound links.

---

## 📁 Files in This Project

| File | Purpose |
|------|---------|
| `halloween_game.ino` | ESP32 Arduino code (upload this to your microcontroller) |
| `laptop_sound_player.py` | Python script (run this on your laptop) |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation and troubleshooting |
| `SOUND_RESOURCES.md` | Where to find free sound effects |
| `QUICK_START.md` | This file! |

---

## ⚠️ Common Issues

**"Port not found" when uploading Arduino code:**
- Check USB cable is connected
- Try a different USB port

**"Could not open serial port" when running Python:**
- **Close Arduino IDE Serial Monitor first!** ← Most common issue
- Make sure ESP32 is plugged in

**No sounds playing:**
- Check that sensors are wired correctly (see README.md)
- Try tapping each sensor to verify they work

---

## 🔧 Hardware Wiring

```
Sensor 1 (DO) → ESP32 GPIO 36
Sensor 2 (DO) → ESP32 GPIO 39
Sensor 3 (DO) → ESP32 GPIO 34
Sensor 4 (DO) → ESP32 GPIO 35

All sensors: VCC → 3.3V, GND → GND
```

---

## 🎮 How the Game Works

1. ESP32 randomly assigns point values (25, 50, 75, 100) to each sensor
2. Player throws ball at cardboard target
3. Hit any sensor → Earn points + hear sound! 🎉
4. Higher points = Better sound effects
5. Score is tracked automatically
6. Wait 5 seconds, then randomize point assignments
7. Repeat forever! Try to maximize your score!

---

**Need more help?** Check `README.md` for full documentation.

**Happy gaming!** 🎃👻

