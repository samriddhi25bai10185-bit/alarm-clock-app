import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
import threading
import time
import pygame
import os

# ---------------- COLORS ---------------- #

BG = "#1E1E2E"
CARD = "#313244"
TEXT = "#FFFFFF"
ACCENT = "#89B4FA"
SUCCESS = "#A6E3A1"

# ---------------- AUDIO ---------------- #

pygame.mixer.init()

# ---------------- WINDOW ---------------- #

root = tk.Tk()
root.title("Smart Alarm Clock")
root.geometry("750x650")
root.resizable(False, False)
root.configure(bg=BG)

# ---------------- VARIABLES ---------------- #

alarm_time = ""
alarm_tone = ""
alarm_active = False
alarm_triggered = False

# ---------------- TITLE ---------------- #

title = tk.Label(
    root,
    text="⏰ Smart Alarm Clock",
    font=("Segoe UI", 24, "bold"),
    bg=BG,
    fg=ACCENT
)
title.pack(pady=15)

# ---------------- DIGITAL CLOCK ---------------- #

clock_label = tk.Label(
    root,
    text="00:00:00",
    font=("Consolas", 36, "bold"),
    bg=BG,
    fg=TEXT
)
clock_label.pack(pady=10)

# ---------------- CARD ---------------- #

card = tk.Frame(
    root,
    bg=CARD,
    padx=20,
    pady=20
)
card.pack(pady=15)

# ---------------- TIME VARIABLES ---------------- #

hour_var = tk.StringVar(value="00")
minute_var = tk.StringVar(value="00")
second_var = tk.StringVar(value="00")

hours = [f"{i:02}" for i in range(24)]
minutes = [f"{i:02}" for i in range(60)]
seconds = [f"{i:02}" for i in range(60)]

# ---------------- TIME SELECTOR ---------------- #

tk.Label(
    card,
    text="Hour",
    bg=CARD,
    fg=TEXT
).grid(row=0, column=0, padx=10)

tk.Label(
    card,
    text="Minute",
    bg=CARD,
    fg=TEXT
).grid(row=0, column=1, padx=10)

tk.Label(
    card,
    text="Second",
    bg=CARD,
    fg=TEXT
).grid(row=0, column=2, padx=10)

hour_menu = ttk.Combobox(
    card,
    textvariable=hour_var,
    values=hours,
    width=5,
    state="readonly"
)
hour_menu.grid(row=1, column=0, padx=10, pady=5)

minute_menu = ttk.Combobox(
    card,
    textvariable=minute_var,
    values=minutes,
    width=5,
    state="readonly"
)
minute_menu.grid(row=1, column=1, padx=10, pady=5)

second_menu = ttk.Combobox(
    card,
    textvariable=second_var,
    values=seconds,
    width=5,
    state="readonly"
)
second_menu.grid(row=1, column=2, padx=10, pady=5)

# ---------------- TONE SELECTION ---------------- #

def select_tone():
    global alarm_tone

    file_path = filedialog.askopenfilename(
        title="Select Alarm Tone",
        filetypes=[
            ("Audio Files", "*.mp3 *.wav"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        alarm_tone = file_path

        tone_label.config(
            text=f"Selected: {os.path.basename(file_path)}"
        )

# ---------------- VOLUME ---------------- #

def set_volume(value):
    pygame.mixer.music.set_volume(float(value) / 100)

# ---------------- ALARM CHECKER ---------------- #

def check_alarm():
    global alarm_active
    global alarm_triggered

    while alarm_active:

        current_time = datetime.now().strftime("%H:%M:%S")

        if current_time == alarm_time:

            alarm_triggered = True

            status_label.config(
                text="🔔 ALARM RINGING!"
            )

            if alarm_tone:
                try:
                    pygame.mixer.music.load(alarm_tone)
                    pygame.mixer.music.play(-1)
                except Exception as e:
                    messagebox.showerror(
                        "Audio Error",
                        str(e)
                    )

            alarm_active = False
            break

        time.sleep(1)

# ---------------- SET ALARM ---------------- #

def set_alarm():
    global alarm_time
    global alarm_active
    global alarm_triggered

    if not alarm_tone:
        messagebox.showerror(
            "Error",
            "Please select an alarm tone."
        )
        return

    alarm_triggered = False

    alarm_time = (
        f"{hour_var.get()}:"
        f"{minute_var.get()}:"
        f"{second_var.get()}"
    )

    current_alarm_label.config(
        text=f"Current Alarm: {alarm_time}"
    )

    alarm_active = True

    status_label.config(
        text=f"Alarm Set For: {alarm_time}"
    )

    threading.Thread(
        target=check_alarm,
        daemon=True
    ).start()

# ---------------- STOP ---------------- #

def stop_alarm():
    global alarm_active
    global alarm_triggered

    pygame.mixer.music.stop()

    alarm_active = False
    alarm_triggered = False

    status_label.config(
        text="Alarm Stopped"
    )

# ---------------- SNOOZE ---------------- #

def snooze_alarm():
    global alarm_time
    global alarm_active
    global alarm_triggered

    if not alarm_triggered:
        messagebox.showinfo(
            "Snooze",
            "No alarm is currently ringing."
        )
        return

    pygame.mixer.music.stop()

    new_time = datetime.now() + timedelta(minutes=5)

    alarm_time = new_time.strftime("%H:%M:%S")

    current_alarm_label.config(
        text=f"Current Alarm: {alarm_time}"
    )

    alarm_active = True
    alarm_triggered = False

    status_label.config(
        text=f"Snoozed Until: {alarm_time}"
    )

    threading.Thread(
        target=check_alarm,
        daemon=True
    ).start()

# ---------------- RESET ---------------- #

def reset_alarm():
    global alarm_time
    global alarm_active
    global alarm_triggered

    pygame.mixer.music.stop()

    alarm_time = ""
    alarm_active = False
    alarm_triggered = False

    current_alarm_label.config(
        text="Current Alarm: None"
    )

    status_label.config(
        text="Alarm Reset"
    )

# ---------------- TONE BUTTON ---------------- #

tone_button = tk.Button(
    card,
    text="🎵 Select Alarm Tone",
    command=select_tone,
    font=("Segoe UI", 11)
)
tone_button.grid(row=2, column=0, columnspan=3, pady=15)

tone_label = tk.Label(
    card,
    text="No Tone Selected",
    bg=CARD,
    fg=TEXT
)
tone_label.grid(row=3, column=0, columnspan=3)

# ---------------- ALARM LABEL ---------------- #

current_alarm_label = tk.Label(
    root,
    text="Current Alarm: None",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 11)
)
current_alarm_label.pack(pady=5)

# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=15)

set_btn = tk.Button(
    button_frame,
    text="Set Alarm",
    width=12,
    command=set_alarm
)
set_btn.grid(row=0, column=0, padx=5)

snooze_btn = tk.Button(
    button_frame,
    text="Snooze",
    width=12,
    command=snooze_alarm
)
snooze_btn.grid(row=0, column=1, padx=5)

stop_btn = tk.Button(
    button_frame,
    text="Stop",
    width=12,
    command=stop_alarm
)
stop_btn.grid(row=0, column=2, padx=5)

reset_btn = tk.Button(
    button_frame,
    text="Reset",
    width=12,
    command=reset_alarm
)
reset_btn.grid(row=0, column=3, padx=5)

# ---------------- VOLUME ---------------- #

volume_label = tk.Label(
    root,
    text="Volume",
    bg=BG,
    fg=TEXT
)
volume_label.pack()

volume_slider = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
    command=set_volume,
    bg=BG,
    fg=TEXT,
    highlightthickness=0
)

volume_slider.set(70)
volume_slider.pack()

# ---------------- STATUS ---------------- #

status_label = tk.Label(
    root,
    text="No Alarm Set",
    bg=BG,
    fg=SUCCESS,
    font=("Segoe UI", 12, "bold")
)
status_label.pack(pady=15)

# ---------------- LIVE CLOCK ---------------- #

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)

update_clock()

# ---------------- RUN ---------------- #

root.mainloop()