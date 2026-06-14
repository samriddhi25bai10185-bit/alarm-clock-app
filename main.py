import tkinter as tk
from tkinter import ttk
from datetime import datetime

root = tk.Tk()
root.title("Smart Alarm Clock")
root.geometry("600x500")

title = tk.Label(
    root,
    text="Smart Alarm Clock",
    font=("Segoe UI", 24, "bold")
)
title.pack(pady=20)

clock_label = tk.Label(
    root,
    text="00:00:00",
    font=("Consolas", 32, "bold")
)
clock_label.pack(pady=20)

hour_var = tk.StringVar(value="00")
minute_var = tk.StringVar(value="00")
second_var = tk.StringVar(value="00")

hours = [f"{i:02}" for i in range(24)]
minutes = [f"{i:02}" for i in range(60)]
seconds = [f"{i:02}" for i in range(60)]

time_frame = tk.Frame(root)
time_frame.pack(pady=20)

tk.Label(
    time_frame,
    text="Hour",
    font=("Segoe UI", 10)
).grid(row=0, column=0, padx=10)

tk.Label(
    time_frame,
    text="Minute",
    font=("Segoe UI", 10)
).grid(row=0, column=1, padx=10)

tk.Label(
    time_frame,
    text="Second",
    font=("Segoe UI", 10)
).grid(row=0, column=2, padx=10)

hour_menu = ttk.Combobox(
    time_frame,
    textvariable=hour_var,
    values=hours,
    width=5,
    state="readonly"
)

hour_menu.grid(row=1, column=0, padx=10, pady=5)

minute_menu = ttk.Combobox(
    time_frame,
    textvariable=minute_var,
    values=minutes,
    width=5,
    state="readonly"
)

minute_menu.grid(row=1, column=1, padx=10, pady=5)

second_menu = ttk.Combobox(
    time_frame,
    textvariable=second_var,
    values=seconds,
    width=5,
    state="readonly"
)

second_menu.grid(row=1, column=2, padx=10, pady=5)

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)

    root.after(1000, update_clock)

update_clock()

root.mainloop()