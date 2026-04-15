import tkinter as tk
import threading
import os
import speech_recognition as sr
import webbrowser
import datetime
import random
import audioop

running = False
volume_level = 50

# 🔊 SPEAK
def speak(text):
    status_label.config(text=f"KAI: {text}")
    os.system(f'say "{text}"')

# 🎤 TAKE COMMAND
def take_command():
    global volume_level
    r = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)

        audio = r.listen(source)

        try:
            volume_level = audioop.rms(audio.frame_data, 2)
        except:
            volume_level = random.randint(50, 200)

    try:
        status_label.config(text="🧠 Recognizing...")
        command = r.recognize_google(audio, language='en-IN')
        print("You said:", command)
        return command.lower()
    except:
        return ""

# 🌊 ANIMATION (FIXED)
def animate_circle():
    global volume_level

    # Idle animation
    if volume_level < 100:
        size = random.randint(80, 120)
    else:
        size = min(max(volume_level // 20, 100), 200)

    canvas.coords(
        circle,
        200 - size,
        200 - size,
        200 + size,
        200 + size
    )

    window.after(60, animate_circle)

# 🤖 MAIN LOGIC
def run_kai():
    global running
    speak("Say wake up")

    while running:
        command = take_command()

        if "wake up" in command:
            speak("I am online Kabir")

            while running:
                command = take_command()

                if command == "":
                    continue

                elif "open google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://google.com")

                elif "open chrome" in command:
                    speak("Opening Chrome")
                    os.system("open -a 'Google Chrome'")

                elif "time" in command:
                    time_now = datetime.datetime.now().strftime("%H:%M")
                    speak(f"The time is {time_now}")

                elif "who are you" in command:
                    speak("I am Kai, your personal AI assistant created by Kabir.")

                elif "what can you do" in command:
                    speak("I can open apps, search the web, and help you.")

                elif "tell joke" in command:
                    jokes = [
                        "Why do programmers hate nature? Too many bugs.",
                        "Why did the computer freeze? It left its Windows open.",
                        "I told my computer I needed a break, it said no problem and froze."
                    ]
                    speak(random.choice(jokes))

                elif "stop" in command:
                    speak("Going to sleep")
                    running = False
                    break

                else:
                    speak("I did not understand")

# ▶️ START
def start_kai():
    global running
    if not running:
        running = True
        threading.Thread(target=run_kai, daemon=True).start()

# ⛔ STOP
def stop_kai():
    global running
    running = False
    status_label.config(text="🛑 Stopped")

# 🖥️ GUI
window = tk.Tk()
window.title("KAI Assistant")
window.geometry("400x450")
window.configure(bg="black")

title = tk.Label(window, text="KAI AI Assistant", font=("Arial", 18), fg="cyan", bg="black")
title.pack(pady=10)

status_label = tk.Label(window, text="Click Start", font=("Arial", 12), fg="white", bg="black")
status_label.pack(pady=10)

# 🌊 CANVAS (FIXED)
canvas = tk.Canvas(window, width=400, height=300, bg="black", highlightthickness=0)
canvas.pack()

# 🔥 BIG CENTER CIRCLE (VISIBLE)
circle = canvas.create_oval(100, 100, 300, 300, fill="cyan", outline="")

# Buttons
start_button = tk.Button(window, text="Start 🎤", command=start_kai, bg="green", fg="white")
start_button.pack(pady=10)

stop_button = tk.Button(window, text="Stop ⛔", command=stop_kai, bg="red", fg="white")
stop_button.pack(pady=10)

# 🔥 START ANIMATION LOOP
animate_circle()

window.mainloop()