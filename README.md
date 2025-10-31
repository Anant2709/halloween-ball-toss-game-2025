# 🎃 Halloween Ball Toss Game

A Halloween-themed interactive game using an ESP32 microcontroller with 4 vibration sensors. Players throw a ball at a cardboard target to earn points! Each target square is worth 25, 50, 75, or 100 points, randomly assigned after each throw.

## 🎮 How It Works

1. **Hardware**: 4 vibration sensors are placed behind a cardboard target
2. **Game Logic**: Each sensor is worth points: 25, 50, 75, or 100 points (randomly assigned)
3. **Gameplay**: Players throw a ball at the target
   - Hit any sensor → Earn points and hear a sound! 🎉
   - Higher points = Better sound effects
   - Score is tracked automatically
4. **Randomization**: After each hit, the game locks for 5 seconds, then randomly reassigns the point values to different sensors

## 📋 Hardware Requirements

- **ESP32-S Module** (or compatible ESP32 board)
- **4x SW-420 Vibration Sensors** (or similar)
- **Cardboard target** (divided into 4 squares)
- **USB cable** to connect ESP32 to laptop
- **Laptop** with Python for sound playback

### Wiring

Connect the vibration sensors to the ESP32:

| Sensor | ESP32 GPIO Pin |
|--------|----------------|
| S1 DO  | GPIO 36        |
| S2 DO  | GPIO 39        |
| S3 DO  | GPIO 34        |
| S4 DO  | GPIO 35        |

All sensors should have VCC connected to 3.3V and GND to GND.

## 🚀 Setup Instructions

### Step 1: Upload Code to ESP32

1. Open Arduino IDE
2. Install ESP32 board support if not already installed:
   - Go to `File > Preferences`
   - Add this URL to "Additional Board Manager URLs": 
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to `Tools > Board > Boards Manager`
   - Search for "ESP32" and install "esp32 by Espressif Systems"

3. Open `halloween_game.ino` in Arduino IDE
4. Select your board: `Tools > Board > ESP32 Arduino > ESP32 Dev Module` (or your specific board)
5. Select the correct port: `Tools > Port > [Your ESP32 Port]`
6. Click the **Upload** button (→)
7. Wait for upload to complete

### Step 2: Set Up Python Environment on Laptop

1. Make sure Python 3.7+ is installed:
   ```bash
   python3 --version
   ```

2. Install required Python packages:
   ```bash
   cd /Users/juhi2/Desktop/AnantUNI/Bhav_halloween_game
   pip3 install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip3 install pyserial pygame numpy
   ```

### Step 3: Add Sound Files (Optional)

The game works with built-in beep sounds that vary by point value, but you can add custom sound files:

1. Download or create sound files for each point value:
   - `25.wav` - Plays when earning 25 points
   - `50.wav` - Plays when earning 50 points
   - `75.wav` - Plays when earning 75 points
   - `100.wav` - Plays when earning 100 points

2. Place them in the same folder as `laptop_sound_player.py`

**Free Sound Resources:**
- [Freesound.org](https://freesound.org/) - Search for "success", "points", "score" sounds
- [Pixabay Sounds](https://pixabay.com/sound-effects/) - Free sound effects
- [Zapsplat](https://www.zapsplat.com/) - Free with attribution

Look for:
- **25 points**: Simple beep, coin sound
- **50 points**: Pleasant chime, "good job"
- **75 points**: Success jingle, applause
- **100 points**: Jackpot, fanfare, "amazing!"

## ▶️ Running the Game

### Start the Game:

1. **Make sure Arduino IDE Serial Monitor is CLOSED** (it can't be open while Python uses the port)

2. Connect your ESP32 to laptop via USB

3. Run the Python script:
   ```bash
   cd /Users/juhi2/Desktop/AnantUNI/Bhav_halloween_game
   python3 laptop_sound_player.py
   ```

4. The script will:
   - Auto-detect your ESP32 (or let you select it manually)
   - Connect to the serial port
   - Start listening for game events

5. **Play!** Throw balls at the cardboard target

### What You'll See:

**In the Python terminal:**
```
==================================================
Halloween Ball Toss Game - Sound Player
==================================================
Points System: 25, 50, 75, or 100 points per throw
==================================================

Point assignments:
  Sensor 1: 75 points
  Sensor 2: 25 points
  Sensor 3: 100 points
  Sensor 4: 50 points
---------------------------

>>> HIT DETECTED on Sensor 3 - Worth 100 points!
🎯 >>> SCORED 100 POINTS!
🎉 100 POINTS! JACKPOT!
📊 Score: 100 points | Throws: 1 | Avg: 100.0

--- READY FOR NEXT THROW ---
```

### Stopping the Game:

- Press `Ctrl+C` in the Python terminal to stop the sound player
- You'll see your final score summary:
  ```
  ==================================================
  GAME OVER!
  ==================================================
  Final Score: 325 points
  Total Throws: 5
  Average Points per Throw: 65.0
  ==================================================
  ```
- The ESP32 will continue running (you can unplug it or press the reset button)

## 🔧 Troubleshooting

### Arduino Upload Issues:

**"Port not found"**
- Make sure USB cable is connected
- Try a different USB port
- Press the "BOOT" button on ESP32 while uploading

**"Permission denied" (Mac/Linux)**
```bash
sudo chmod 666 /dev/tty.* 
# Or add yourself to dialout group on Linux
```

### Python Script Issues:

**"No module named serial"**
```bash
pip3 install pyserial
```

**"Could not open serial port"**
- Close Arduino IDE Serial Monitor
- Make sure no other program is using the serial port
- On Mac: Look for `/dev/cu.usbserial-*` or `/dev/cu.SLAB_USBtoUART`
- On Windows: Look for `COM3`, `COM4`, etc.
- On Linux: Look for `/dev/ttyUSB0` or `/dev/ttyACM0`

**Script connects but no sounds play**
- Check that the vibration sensors are wired correctly
- Tap each sensor to verify they're working
- Check the Serial Monitor output to see if sensors are detecting

**Multiple detections from one throw**
- The 5-second lockout should prevent this
- If it still happens, increase `LOCK_DURATION_MS` in the Arduino code

### Sensor Issues:

**Sensors not detecting vibration**
- Check wiring connections
- Make sure sensors have power (3.3V)
- Some sensors need adjustment with the onboard potentiometer
- Try setting `ACTIVE_LOW = true` in the Arduino code if sensors are inverted

**Sensors too sensitive / not sensitive enough**
- Most SW-420 sensors have a sensitivity adjustment potentiometer
- Turn clockwise to decrease sensitivity
- Turn counter-clockwise to increase sensitivity

## ⚙️ Configuration

### Arduino Code (`halloween_game.ino`):

```cpp
const bool ACTIVE_LOW = false;  // Change to true if sensors are inverted
const unsigned long DEBOUNCE_MS = 30;  // Adjust for sensor noise
const unsigned long LOCK_DURATION_MS = 5000;  // Time between rounds (milliseconds)
```

### Python Code (`laptop_sound_player.py`):

```python
BAUD_RATE = 115200  // Must match Arduino code
SOUND_25 = "25.wav"   // 25 points sound
SOUND_50 = "50.wav"   // 50 points sound
SOUND_75 = "75.wav"   // 75 points sound
SOUND_100 = "100.wav" // 100 points sound
```

## 📁 Project Structure

```
Bhav_halloween_game/
├── halloween_game.ino          # ESP32 Arduino code
├── laptop_sound_player.py      # Python sound player with score tracking
├── requirements.txt            # Python dependencies
├── README.md                   # Full documentation
├── QUICK_START.md             # Quick start guide
├── SOUND_RESOURCES.md         # Sound file resources
├── 25.wav                     # 25 points sound
├── 50.wav                     # 50 points sound
├── 75.wav                     # 75 points sound
└── 100.wav                    # 100 points sound
```

## 🎯 Game Tips

- Mark the squares on your cardboard so players know where to aim
- Use a soft ball (foam, tennis ball) to avoid damaging sensors
- Test each sensor individually before playing
- Adjust the 5-second delay if needed for your gameplay
- Add decorative elements for Halloween theme! 🎃👻

## 📝 Notes

- The ESP32 uses GPIO 36, 39, 34, 35 (input-only pins, perfect for sensors)
- Serial communication runs at 115200 baud for fast response
- The Python script includes auto-detection of the ESP32 port
- Built-in beep sounds work if you don't have custom sound files (different sounds for each point value!)
- Game automatically randomizes point assignments after each round
- Score tracking shows total points, number of throws, and average per throw
- Press Ctrl+C to see final score summary

## 🤝 Debugging Mode

Both the Arduino and Python scripts include verbose output for debugging:

- **Arduino Serial Monitor**: Shows which sensor is "good", hit detection, and game state
- **Python Terminal**: Shows all ESP32 messages plus sound playback status

You can open Arduino IDE Serial Monitor for debugging **when the Python script is NOT running**.

---

**Have fun and Happy Halloween!** 🎃🎮👻

