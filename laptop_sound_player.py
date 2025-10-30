#!/usr/bin/env python3
"""
Halloween Ball Toss Game - Laptop Sound Player

This script listens to the ESP32 via serial port and plays sounds
based on whether the player hit the good or bad sensor.

Requirements:
- pyserial (for serial communication)
- pygame (for sound playback)
"""

import serial
import serial.tools.list_ports
import pygame
import sys
import time
import os

# Configuration
BAUD_RATE = 115200
GOOD_SOUND = "good_sound.wav"  # Place your good sound file here
BAD_SOUND = "bad_sound.wav"    # Place your bad sound file here

def find_esp32_port():
    """
    Automatically find the ESP32 serial port.
    Returns the port name or None if not found.
    """
    ports = serial.tools.list_ports.comports()
    
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port.device} - {port.description}")
    
    # Common ESP32 identifiers
    esp32_keywords = ['CP210', 'CH340', 'USB', 'UART', 'Serial']
    
    for port in ports:
        for keyword in esp32_keywords:
            if keyword.lower() in port.description.lower():
                return port.device
    
    return None

def select_port_manually():
    """
    Let user manually select a port if auto-detection fails.
    """
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("ERROR: No serial ports found!")
        return None
    
    print("\nPlease select the ESP32 port:")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port.device} - {port.description}")
    
    try:
        choice = int(input("\nEnter port number: "))
        if 0 <= choice < len(ports):
            return ports[choice].device
        else:
            print("Invalid selection!")
            return None
    except ValueError:
        print("Invalid input!")
        return None

def play_beep(frequency, duration_ms):
    """
    Generate and play a simple beep tone if sound files are not available.
    """
    sample_rate = 22050
    samples = int(sample_rate * duration_ms / 1000)
    
    # Generate sine wave
    import numpy as np
    wave = np.sin(2 * np.pi * frequency * np.arange(samples) / sample_rate)
    wave = (wave * 32767).astype(np.int16)
    
    # Convert to stereo
    stereo_wave = np.column_stack((wave, wave))
    
    sound = pygame.sndarray.make_sound(stereo_wave)
    sound.play()
    pygame.time.wait(duration_ms)

def play_good_sound():
    """Play the good/success sound."""
    if os.path.exists(GOOD_SOUND):
        try:
            sound = pygame.mixer.Sound(GOOD_SOUND)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
        except Exception as e:
            print(f"Error playing good sound: {e}")
            play_beep(800, 200)  # High pitch success beep
    else:
        # Play success beep pattern: high-high-higher
        print("🎉 GOOD! (Playing beep - add 'good_sound.wav' for custom sound)")
        play_beep(600, 150)
        time.sleep(0.05)
        play_beep(700, 150)
        time.sleep(0.05)
        play_beep(900, 300)

def play_bad_sound():
    """Play the bad/failure sound."""
    if os.path.exists(BAD_SOUND):
        try:
            sound = pygame.mixer.Sound(BAD_SOUND)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
        except Exception as e:
            print(f"Error playing bad sound: {e}")
            play_beep(200, 500)  # Low pitch failure beep
    else:
        # Play failure beep pattern: low-lower
        print("❌ BAD! (Playing beep - add 'bad_sound.wav' for custom sound)")
        play_beep(300, 300)
        time.sleep(0.05)
        play_beep(200, 500)

def main():
    """Main function to listen to serial port and play sounds."""
    
    # Initialize pygame mixer for sound
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    print("=" * 50)
    print("Halloween Ball Toss Game - Sound Player")
    print("=" * 50)
    
    # Find the ESP32 port
    port = find_esp32_port()
    
    if port is None:
        print("\nCouldn't auto-detect ESP32. Manual selection required.")
        port = select_port_manually()
    else:
        print(f"\nAuto-detected ESP32 on: {port}")
    
    if port is None:
        print("No port selected. Exiting.")
        sys.exit(1)
    
    # Connect to serial port
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for connection to stabilize
        print(f"✓ Connected to {port} at {BAUD_RATE} baud")
        print("\nListening for game events...")
        print("-" * 50)
    except serial.SerialException as e:
        print(f"ERROR: Could not open serial port {port}")
        print(f"Details: {e}")
        print("\nMake sure:")
        print("  1. ESP32 is connected via USB")
        print("  2. Arduino IDE Serial Monitor is CLOSED")
        print("  3. You have permission to access the port")
        sys.exit(1)
    
    # Main listening loop
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Only print debug info (not GOOD/BAD as they're handled separately)
                if line and line not in ["GOOD", "BAD"]:
                    print(line)
                
                # Check for game signals
                if line == "GOOD":
                    print("\n🎯 >>> GOOD HIT! Playing success sound...")
                    play_good_sound()
                    print("")
                elif line == "BAD":
                    print("\n💥 >>> BAD HIT! Playing failure sound...")
                    play_bad_sound()
                    print("")
    
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        ser.close()
        pygame.mixer.quit()
        sys.exit(0)
    
    except Exception as e:
        print(f"\nERROR: {e}")
        ser.close()
        pygame.mixer.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()

