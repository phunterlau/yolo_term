#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run script for Yolo Terminal game.
Allows users to choose between terminal and web interface.
"""

import os
import sys
import subprocess
import threading
import webbrowser
import time

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_terminal_game():
    """Run the terminal version of the game."""
    clear_screen()
    print("Starting Yolo Terminal in terminal mode...")
    print("Press Ctrl+C to exit.")
    print()
    
    # Run the terminal game
    try:
        os.system('python yolo_terminal.py')
    except KeyboardInterrupt:
        print("\nExiting terminal game...")

def run_web_server():
    """Run the web server."""
    # Start the Flask server in a separate process
    server_process = subprocess.Popen([sys.executable, 'server.py'])
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Open the web browser
    webbrowser.open('http://localhost:5001')
    
    print("Web server running at http://localhost:5001")
    print("Press Ctrl+C to stop the server and exit.")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the server when Ctrl+C is pressed
        server_process.terminate()
        print("\nStopping web server...")

def main():
    """Main function to run the game."""
    clear_screen()
    print("=" * 60)
    print("                     YOLO TERMINAL")
    print("=" * 60)
    print("\nWelcome to Yolo Terminal, a stock trading simulation game!")
    print("\nChoose how you want to play:")
    print("1. Terminal Interface (Original)")
    print("2. Web Interface (New)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            run_terminal_game()
            break
        elif choice == '2':
            run_web_server()
            break
        elif choice == '3':
            print("\nExiting Yolo Terminal. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
