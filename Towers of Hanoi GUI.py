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

    def create_pole(self, x, y):
        pole = self.canvas.create_rectangle(x - 5, y, x + 5, y - 150, fill="black")
        return pole

    def create_disk(self, x, y, width, pole):
        disk = self.canvas.create_rectangle(x - width / 2, y, x + width / 2, y + 20, fill="blue")
        self.canvas.tag_bind(disk, "<ButtonPress-1>", self.on_disk_press)
        self.canvas.tag_bind(disk, "<ButtonRelease-1>", self.on_disk_release)
        self.canvas.tag_bind(disk, "<B1-Motion>", self.on_disk_motion)
        self.canvas.tag_lower(disk, pole)
        return disk

    def on_disk_press(self, event):
        self.selected_disk = event.widget.find_closest(event.x, event.y)[0]
        self.offset_x = event.x - self.canvas.coords(self.selected_disk)[0]
        self.offset_y = event.y - self.canvas.coords(self.selected_disk)[1]

    def on_disk_release(self, event):
        pass

    def on_disk_motion(self, event):
        self.canvas.move(self.selected_disk, event.x - self.offset_x - self.canvas.coords(self.selected_disk)[0],
                         event.y - self.offset_y - self.canvas.coords(self.selected_disk)[1])

    