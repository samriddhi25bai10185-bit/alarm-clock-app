
# Smart Alarm Clock Pro V3.0
# Install: pip install customtkinter pygame plyer

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
from plyer import notification
import pygame, threading, json, os, time

DATA_FILE = "alarms_v3.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

pygame.mixer.init()

class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Alarm Clock Pro V3")
        self.root.geometry("1280x800")

        self.alarms = []
        self.tone = ""
        self.ringing = False
        self.status_text = ctk.StringVar(value="🟢 Ready")

        self.build_ui()
        self.load_data()

        threading.Thread(target=self.monitor_alarms, daemon=True).start()
        self.update_ui()

    def build_ui(self):
        self.hero = ctk.CTkFrame(self.root, corner_radius=20)
        self.hero.pack(fill="x", padx=20, pady=15)

        self.clock = ctk.CTkLabel(self.hero, text="00:00:00",
                                  font=("Consolas", 64, "bold"))
        self.clock.pack(pady=(20,5))

        self.date_lbl = ctk.CTkLabel(self.hero, text="")
        self.date_lbl.pack()

        self.countdown_lbl = ctk.CTkLabel(self.hero, text="No alarms scheduled",
                                          font=("Segoe UI",18,"bold"))
        self.countdown_lbl.pack(pady=15)

        body = ctk.CTkFrame(self.root)
        body.pack(fill="both", expand=True, padx=20, pady=10)

        left = ctk.CTkFrame(body)
        left.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(left, text="Add Alarm",
                     font=("Segoe UI",20,"bold")).pack(pady=10)

        self.label_entry = ctk.CTkEntry(left, placeholder_text="Alarm Label")
        self.label_entry.pack(fill="x", padx=15, pady=5)

        tf = ctk.CTkFrame(left)
        tf.pack(pady=10)

        self.h = ctk.CTkComboBox(tf, values=[f"{i:02}" for i in range(24)], width=70)
        self.m = ctk.CTkComboBox(tf, values=[f"{i:02}" for i in range(60)], width=70)
        self.s = ctk.CTkComboBox(tf, values=[f"{i:02}" for i in range(60)], width=70)

        for w in [self.h,self.m,self.s]:
            w.set("00")
            w.pack(side="left", padx=4)

        self.snooze_box = ctk.CTkComboBox(left, values=["5","10","15"])
        self.snooze_box.set("5")
        self.snooze_box.pack(pady=5)

        ctk.CTkButton(left, text="🎵 Select Tone",
                      command=self.select_tone).pack(pady=5)

        self.tone_lbl = ctk.CTkLabel(left, text="No tone selected")
        self.tone_lbl.pack()

        ctk.CTkButton(left, text="➕ Add Alarm",
                      command=self.add_alarm).pack(pady=10)

        ctk.CTkLabel(left, text="Volume").pack()
        self.vol = ctk.CTkSlider(left, from_=0, to=100,
                                 command=lambda v: pygame.mixer.music.set_volume(float(v)/100))
        self.vol.set(70)
        self.vol.pack(fill="x", padx=10)

        self.status = ctk.CTkLabel(left, textvariable=self.status_text,
                                   font=("Segoe UI",16,"bold"))
        self.status.pack(pady=15)

        right = ctk.CTkFrame(body)
        right.pack(side="right", fill="both", expand=True, padx=10)

        ctk.CTkLabel(right, text="Active Alarms",
                     font=("Segoe UI",20,"bold")).pack(pady=10)

        self.alarm_area = ctk.CTkScrollableFrame(right)
        self.alarm_area.pack(fill="both", expand=True, padx=10, pady=10)

        controls = ctk.CTkFrame(right)
        controls.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(controls, text="🔕 Snooze",
                      command=self.snooze_alarm).pack(side="left", padx=5)

        ctk.CTkButton(controls, text="⏹ Stop Alarm",
                      fg_color="#dc2626",
                      hover_color="#b91c1c",
                      command=self.stop_alarm).pack(side="left", padx=5)

        ctk.CTkButton(controls, text="🌙 Toggle Theme",
                      command=self.toggle_theme).pack(side="left", padx=5)

        ctk.CTkButton(controls, text="🗑 Clear All",
                      command=self.clear_all).pack(side="left", padx=5)

    def select_tone(self):
        path = filedialog.askopenfilename(filetypes=[("Audio","*.mp3 *.wav")])
        if path:
            self.tone = path
            self.tone_lbl.configure(text=os.path.basename(path))

    def add_alarm(self):
        alarm = {
            "label": self.label_entry.get() or "Alarm",
            "time": f"{self.h.get()}:{self.m.get()}:{self.s.get()}"
        }
        self.alarms.append(alarm)
        self.save_data()
        self.render_alarms()

    def render_alarms(self):
        for w in self.alarm_area.winfo_children():
            w.destroy()

        if not self.alarms:
            ctk.CTkLabel(
                self.alarm_area,
                text="No alarms scheduled\n\nCreate your first alarm."
            ).pack(pady=50)
            return

        for idx, alarm in enumerate(self.alarms):
            card = ctk.CTkFrame(self.alarm_area, corner_radius=15)
            card.pack(fill="x", padx=8, pady=8)

            ctk.CTkLabel(card,
                         text=f"🟢 {alarm['label']}",
                         font=("Segoe UI",16,"bold")).pack(anchor="w", padx=10, pady=(8,2))

            ctk.CTkLabel(card, text=alarm["time"]).pack(anchor="w", padx=10)

            ctk.CTkButton(card, text="Delete",
                          width=90,
                          command=lambda i=idx:self.delete_alarm(i)).pack(anchor="e", padx=10, pady=8)

    def delete_alarm(self, idx):
        self.alarms.pop(idx)
        self.save_data()
        self.render_alarms()

    def monitor_alarms(self):
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            for alarm in self.alarms[:]:
                if alarm["time"] == now:
                    self.trigger_alarm(alarm)
            time.sleep(1)

    def trigger_alarm(self, alarm):
        self.ringing = True
        self.status_text.set("🔔 Alarm Ringing")

        try:
            if self.tone:
                pygame.mixer.music.load(self.tone)
                pygame.mixer.music.play(-1)
        except:
            pass

        notification.notify(
            title="Alarm Time Reached",
            message=alarm["label"],
            timeout=5
        )

        if alarm in self.alarms:
            self.alarms.remove(alarm)
            self.save_data()
            self.render_alarms()

    def stop_alarm(self):
        pygame.mixer.music.stop()
        self.ringing = False
        self.status_text.set("🟢 Ready")

    def snooze_alarm(self):
        if not self.ringing:
            messagebox.showinfo("Snooze","No alarm is ringing.")
            return

        mins = int(self.snooze_box.get())
        t = (datetime.now()+timedelta(minutes=mins)).strftime("%H:%M:%S")

        self.alarms.append({"label":"Snoozed Alarm","time":t})
        self.stop_alarm()
        self.save_data()
        self.render_alarms()

    def clear_all(self):
        self.alarms.clear()
        self.save_data()
        self.render_alarms()

    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

    def update_ui(self):
        now = datetime.now()
        self.clock.configure(text=now.strftime("%H:%M:%S"))
        self.date_lbl.configure(text=now.strftime("%A, %d %B %Y"))

        if self.alarms:
            nxt = sorted(self.alarms, key=lambda a: a["time"])[0]
            self.countdown_lbl.configure(text=f"Next Alarm: {nxt['label']} • {nxt['time']}")
        else:
            self.countdown_lbl.configure(text="No alarms scheduled")

        self.root.after(1000, self.update_ui)

    def save_data(self):
        with open(DATA_FILE,"w") as f:
            json.dump(self.alarms,f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE,"r") as f:
                    self.alarms = json.load(f)
            except:
                self.alarms = []
        self.render_alarms()

root = ctk.CTk()
app = AlarmApp(root)
root.mainloop()
