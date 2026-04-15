import tkinter as tk
import threading
import os
import speech_recognition as sr
import webbrowser
import datetime
import random
import audioop
import time
import math
from memory import *

running = False
volume_level = 50
wave_offset = 0

# 🔊 SPEAK
def speak(text):
    chatbox.insert(tk.END, f"KAI: {text}\n")
    chatbox.see(tk.END)
    os.system(f'say "{text}"')

# 🎤 LISTEN
def take_command():
    global volume_level
    r = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)

            try:
                volume_level = audioop.rms(audio.frame_data, 2)
            except:
                volume_level = random.randint(50, 200)

            try:
                command = r.recognize_google(audio, language='en-IN')
                print("You said:", command)
                chatbox.insert(tk.END, f"You: {command}\n")
                chatbox.see(tk.END)
                return command.lower()
            except:
                return ""
        except:
            return ""

# 🌊 WAVE
def draw_wave():
    global wave_offset, volume_level

    canvas.delete("wave")

    width = 500
    height = 120
    center_y = height // 2

    amplitude = max(10, min(volume_level // 10, 40))
    frequency = 0.05

    for i in range(3):
        points = []
        offset = wave_offset + i * 1.5

        for x in range(width):
            y = center_y + amplitude * math.sin(frequency * x + offset)
            points.append(x)
            points.append(y)

        canvas.create_line(points, fill="#00ffff", width=2 + i, smooth=1, tags="wave")

    wave_offset += 0.3
    root.after(30, draw_wave)

# ⏰ REMINDER
def reminder_checker():
    while True:
        reminders = get_reminders()
        now = datetime.datetime.now().strftime("%H:%M")

        for r in reminders:
            if r["time"] == now:
                speak(f"Reminder: {r['text']}")
                time.sleep(60)

        time.sleep(10)

# 🤖 MAIN
def run_kai():
    global running
    speak("KAI running")

    while running:
        command = take_command()

        if command == "":
            continue

        # 👋 FIXED HELLO
        elif command.strip() == "hello":
            name = get_name()
            if name:
                speak(f"Hello {name}")
            else:
                speak("Hello")

        elif "my name is" in command:
            name = command.replace("my name is", "").strip()
            set_name(name)
            speak(f"Saved {name}")

        elif "who are you" in command:
            speak("I am KAI, your personal AI assistant created by Kabir.")

        elif "what can you do" in command:
            speak("I can talk with you, open apps, set reminders, and help you.")

        elif "tell joke" in command:
            jokes = [
                "Why do programmers hate nature? Too many bugs.",
                "Why did the computer freeze? It left its Windows open.",
                "I told my computer I needed a break, it said no problem and froze."
            ]
            speak(random.choice(jokes))

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "time" in command:
            speak(datetime.datetime.now().strftime("%H:%M"))

        # ⏰ REMINDER
        elif "remind me to" in command and "at" in command:
            try:
                parts = command.replace("remind me to", "").split("at")
                task = parts[0].strip()
                time_input = parts[1].strip().lower()

                if "pm" in time_input or "am" in time_input:
                    time_input = time_input.replace(" ", "")

                    if "pm" in time_input:
                        time_input = time_input.replace("pm", "")
                        hh, mm = time_input.split(":")
                        hh = int(hh)
                        if hh != 12:
                            hh += 12
                        time_input = f"{hh:02d}:{mm}"

                    elif "am" in time_input:
                        time_input = time_input.replace("am", "")
                        hh, mm = time_input.split(":")
                        hh = int(hh)
                        if hh == 12:
                            hh = 0
                        time_input = f"{hh:02d}:{mm}"

                else:
                    time_input = time_input.replace(".", ":").replace(" ", "")
                    hh, mm = time_input.split(":")[0], time_input.split(":")[1][:2]
                    time_input = f"{int(hh):02d}:{mm}"

                add_reminder(task, time_input)
                speak(f"Reminder set for {time_input}")

            except:
                speak("Say time like 9:30 PM or 21:30")

        elif "stop" in command:
            running = False
            speak("Stopping")
            break

        else:
            speak("I did not understand")

# ▶️ START
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=run_kai, daemon=True).start()
        threading.Thread(target=reminder_checker, daemon=True).start()

# ⛔ STOP
def stop():
    global running
    running = False

# 🖥️ UI
root = tk.Tk()
root.title("KAI Assistant")
root.geometry("500x650")
root.configure(bg="black")

title = tk.Label(root, text="KAI AI Assistant", font=("Arial", 20), fg="cyan", bg="black")
title.pack(pady=10)

canvas = tk.Canvas(root, width=500, height=120, bg="black", highlightthickness=0)
canvas.pack(pady=10)

chatbox = tk.Text(root, width=60, height=20, bg="black", fg="white", insertbackground="white")
chatbox.pack(pady=10)

start_btn = tk.Button(root, text="Start 🎤", command=start, bg="green", fg="white")
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop ⛔", command=stop, bg="red", fg="white")
stop_btn.pack(pady=5)

draw_wave()

root.mainloop()