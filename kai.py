print("PROGRAM STARTED")
import os
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"

import speech_recognition as sr
import webbrowser
import datetime
import tkinter as tk
from threading import Thread

# 🔊 Speak
def speak(text):
    print("KAI:", text)
    os.system(f'say "{text}"')

# 🎤 Voice input
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        window.update()

        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        status_label.config(text="Recognizing...")
        window.update()

        command = r.recognize_google(audio, language='en-IN')
        print("You said:", command)
        return command.lower()
    except:
        return ""

# 🧠 Offline AI (simple rule-based)
def offline_ai(command):
    if "who are you" in command:
        return "I am Kai, your personal AI assistant."

    elif "how are you" in command:
        return "I am functioning perfectly."

    elif "your name" in command:
        return "My name is Kai."

    elif "what can you do" in command:
        return "I can open apps, websites, and assist you."

    else:
        return "I did not understand that."

# 🚀 Main AI loop
def run_kai():
    speak("Say wake up to activate")

    while True:
        command = take_command()

        if "wake up" in command:
            speak("I am online Kabir")

            while True:
                command = take_command()

                if command == "":
                    continue

                # 🌐 Websites
                elif "open google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://google.com")

                elif "open youtube" in command:
                    speak("Opening YouTube")
                    webbrowser.open("https://youtube.com")

                # 💻 Apps
                elif "open chrome" in command:
                    speak("Opening Chrome")
                    os.system("open -a 'Google Chrome'")

                elif "open vscode" in command:
                    speak("Opening VS Code")
                    os.system("open -a 'Visual Studio Code'")

                # ⏰ Time
                elif "time" in command:
                    time_now = datetime.datetime.now().strftime("%H:%M")
                    speak(f"The time is {time_now}")

                # ❌ Exit
                elif "exit" in command or "stop" in command:
                    speak("Going to sleep")
                    break

                # 🧠 Offline AI response
                else:
                    reply = offline_ai(command)
                    speak(reply)

# 🖥️ GUI Setup
window = tk.Tk()
window.title("KAI Assistant")
window.geometry("400x300")

title = tk.Label(window, text="KAI AI Assistant", font=("Arial", 18))
title.pack(pady=10)

status_label = tk.Label(window, text="Click Start", font=("Arial", 12))
status_label.pack(pady=20)

# ▶️ Start button
def start_kai():
    thread = Thread(target=run_kai)
    thread.daemon = True
    thread.start()

start_button = tk.Button(window, text="Start KAI", command=start_kai)
start_button.pack(pady=10)

# ❌ Exit button
exit_button = tk.Button(window, text="Exit", command=window.quit)
exit_button.pack(pady=10)

window.mainloop()