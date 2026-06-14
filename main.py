import tkinter as tk
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


def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)

    # Update every second
    root.after(1000, update_clock)

update_clock()

root.mainloop()