import tkinter as tk

class HanoiGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tower of Hanoi")
        self.geometry("600x400")

        self.num_disks = tk.StringVar()
        num_disks_label = tk.Label(self, text="Enter number of disks:")
        num_disks_label.pack()
        num_disks_entry = tk.Entry(self, textvariable=self.num_disks)
        num_disks_entry.pack()

        play_button = tk.Button(self, text="Play", command=self.play)
        play_button.pack()

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(expand=True, fill="both")

        self.poles = [self.create_pole(150,150), self.create_pole(300,150), self.create_pole(450,150)]