#!/usr/bin/env python3
"""
Halloween Ball Toss Game - Laptop Sound Player

This script listens to the ESP32 via serial port and plays sounds
based on the point value earned (25, 50, 75, or 100 points).

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

# Optional custom sound files (place in same folder as script)
SOUND_25 = "25.wav"   # 25 points sound
SOUND_50 = "50.wav"   # 50 points sound
SOUND_75 = "75.wav"   # 75 points sound
SOUND_100 = "100.wav" # 100 points sound

# Score tracking
total_score = 0
throw_count = 0

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

def play_points_sound(points):
    """Play sound based on points earned."""
    global total_score, throw_count
    
    # Update score tracking
    total_score += points
    throw_count += 1
    
    # Determine which sound file to use
    sound_file = None
    if points == 100:
        sound_file = SOUND_100
    elif points == 75:
        sound_file = SOUND_75
    elif points == 50:
        sound_file = SOUND_50
    elif points == 25:
        sound_file = SOUND_25
    
    # Try to play custom sound file if it exists
    if sound_file and os.path.exists(sound_file):
        try:
            sound = pygame.mixer.Sound(sound_file)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
            return
        except Exception as e:
            print(f"Error playing sound file: {e}")
    
    # Otherwise, play beeps based on point value
    if points == 100:
        # Jackpot! - Ascending fanfare
        print("🎉 100 POINTS! JACKPOT!")
        play_beep(600, 100)
        time.sleep(0.05)
        play_beep(700, 100)
        time.sleep(0.05)
        play_beep(800, 100)
        time.sleep(0.05)
        play_beep(1000, 400)
    elif points == 75:
        # Great! - Triple ascending beeps
        print("🌟 75 POINTS! Great throw!")
        play_beep(600, 150)
        time.sleep(0.05)
        play_beep(750, 150)
        time.sleep(0.05)
        play_beep(900, 300)
    elif points == 50:
        # Good - Double beeps
        print("✨ 50 POINTS! Good job!")
        play_beep(500, 150)
        time.sleep(0.05)
        play_beep(700, 250)
    elif points == 25:
        # Okay - Single beep
        print("💫 25 POINTS! Nice!")
        play_beep(500, 300)

def main():
    """Main function to listen to serial port and play sounds."""
    
    global total_score, throw_count
    
    # Initialize pygame mixer for sound
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    print("=" * 50)
    print("Halloween Ball Toss Game - Sound Player")
    print("=" * 50)
    print("Points System: 25, 50, 75, or 100 points per throw")
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
                
                # Check for points message (format: "POINTS:value")
                if line.startswith("POINTS:"):
                    try:
                        points = int(line.split(":")[1])
                        print(f"\n🎯 >>> SCORED {points} POINTS!")
                        play_points_sound(points)
                        
                        # Display score summary
                        avg_score = total_score / throw_count if throw_count > 0 else 0
                        print(f"📊 Score: {total_score} points | Throws: {throw_count} | Avg: {avg_score:.1f}")
                        print("")
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing points: {e}")
                
                # Print all other debug messages
                elif line and not line.startswith("POINTS:"):
                    print(line)
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 50)
        print("GAME OVER!")
        print("=" * 50)
        print(f"Final Score: {total_score} points")
        print(f"Total Throws: {throw_count}")
        if throw_count > 0:
            avg = total_score / throw_count
            print(f"Average Points per Throw: {avg:.1f}")
        print("=" * 50)
        print("\nShutting down...")
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

