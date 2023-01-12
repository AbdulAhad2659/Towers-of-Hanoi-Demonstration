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

    def play(self):
        num_disks = int(self.num_disks.get())
        self.disks = []
        for i in range(num_disks, 0, -1):
            disk = self.create_disk(150, 150 - (i - 1) * 20, i * 20, self.poles[0])
            self.disks.append(disk)
            self.tower_of_hanoi(i, self.poles[0], self.poles[2], self.poles[1], self.disks)
            self.canvas.update()
            self.canvas.after(1000)

    def tower_of_hanoi(self, n, from_pole, to_pole, aux_pole, disks):
        if n == 0:
            return
        self.tower_of_hanoi(n - 1, from_pole, aux_pole, to_pole, disks)
        disk_to_move = disks.pop()
        self.canvas.move(disk_to_move, self.canvas.coords(to_pole)[0] - self.canvas.coords(from_pole)[0],
                         self.canvas.coords(to_pole)[1] - self.canvas.coords(from_pole)[1] - 20 * (len(disks)))
        disks.append(disk_to_move)
        self.tower_of_hanoi(n - 1, aux_pole, to_pole, from_pole, disks)

    