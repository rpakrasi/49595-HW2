#!/usr/bin/env python3
"""
Script to launch Duckiebot keyboard control.
Discovers duckiebot9 and then starts keyboard_control.
Uses the default macOS Terminal application.
"""

import subprocess
import time
import sys

DUCKIEBOT_NAME = "duckiebot9"
DISCOVERY_TIMEOUT = 60  # seconds
DISCOVERY_CHECK_INTERVAL = 2  # seconds

def open_terminal_and_discover():
    """
    Open the default macOS Terminal and start fleet discovery.
    Returns the terminal process.
    """
    # AppleScript to open Terminal and run dts fleet discover
    apple_script = f"""
    tell application "Terminal"
        activate
        do script "cd ~; dts fleet discover"
    end tell
    """
    
    subprocess.run(["osascript", "-e", apple_script], check=True)
    print("✓ Terminal opened and fleet discovery started")
    print("  Monitoring for duckiebot9 availability...")
    time.sleep(1)

def run_keyboard_control():
    """
    Open a new Terminal window and run the keyboard_control command.
    """
    apple_script = f"""
    tell application "Terminal"
        activate
        do script "dts duckiebot keyboard_control {DUCKIEBOT_NAME} --browser"
    end tell
    """
    
    subprocess.run(["osascript", "-e", apple_script], check=True)
    print(f"\n✓ Keyboard control launched for {DUCKIEBOT_NAME}")
    print("  Browser should open with the controller interface")

def check_duckiebot_availability():
    """
    Run dts fleet discover and check if duckiebot9 is available.
    Returns True if available, False otherwise.
    """
    try:
        result = subprocess.run(
            ["dts", "fleet", "discover"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
        
        # Check if duckiebot9 is in the output
        if DUCKIEBOT_NAME in output:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return False

def main():
    """Main execution flow."""
    print(f"🤖 Duckiebot Launcher - Searching for {DUCKIEBOT_NAME}")
    print("-" * 50)
    
    # Start discovery in Terminal
    open_terminal_and_discover()
    
    # Monitor for duckiebot availability
    print(f"\n⏳ Waiting for {DUCKIEBOT_NAME} to be discovered...")
    print(f"   (timeout: {DISCOVERY_TIMEOUT} seconds)")
    
    elapsed = 0
    while elapsed < DISCOVERY_TIMEOUT:
        if check_duckiebot_availability():
            print(f"\n✅ {DUCKIEBOT_NAME} is available!")
            time.sleep(2)  # Give brief moment for discovery to fully complete
            run_keyboard_control()
            print("\n✨ Setup complete! Check the Terminal window for the controller.")
            return 0
        
        time.sleep(DISCOVERY_CHECK_INTERVAL)
        elapsed += DISCOVERY_CHECK_INTERVAL
        dots = "." * (elapsed // DISCOVERY_CHECK_INTERVAL)
        print(f"   Checking{dots}", end="\r")
    
    print(f"\n❌ Timeout: {DUCKIEBOT_NAME} not found after {DISCOVERY_TIMEOUT} seconds")
    print("   Make sure:")
    print("   - Your Duckiebot is powered on and connected to your network")
    print("   - You have DTS (Duckietown Shell) properly installed")
    print("   - You're connected to the same network as the Duckiebot")
    return 1

if __name__ == "__main__":
    sys.exit(main())
