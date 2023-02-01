import tkinter as tk
import time
import threading
import random


class TypeSpeedGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Application")
        self.root.geometry("800x600")

        self.texts = open("texts.txt", "r").read().split("\n")
        self.high = float(open("high_score.txt", "r").read())

        self.frame = tk.Frame(self.root)

        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = tk.Label(self.frame, text=f"High_Score: {self.high:.2f} WPM\nSpeed: \n0.00 CPM\n0.00 WPM",
                                    font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset, font=("Helvetica", 24))
        self.reset_button.grid(row=3, column=0, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if event.keycode not in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.sample_label.cget("text").startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get() == self.sample_label.cget('text'):
            self.running = False
            self.input_entry.config(fg="green")

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wpm = cpm/5
            self.speed_label.config(text=f"High_Score: {self.high:.2f} WPM\nSpeed: \n{cpm:.2f} CPM\n{wpm:.2f} WPM")
            if wpm > self.high:
                f = open("high_score.txt", "w")
                f.write(f"{wpm}")
                f.close()
        else:
            if wpm > self.high:
                self.high=wpm

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text=f"High_Score: {self.high:.2f} WPM\nSpeed: \n0.00 CPM\n0.00 WPM")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)


TypeSpeedGUI()
