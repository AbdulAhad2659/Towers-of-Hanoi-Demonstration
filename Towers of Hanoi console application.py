def tower_of_hanoi(n, source, auxiliary, target):
    if n == 1:
        print("Move disk 1 from source", source, "to target", target)

        return

    tower_of_hanoi(n - 1, source, target, auxiliary)

    print("Move disk", n, "from source", source, "to target", target)

    tower_of_hanoi(n - 1, auxiliary, source, target)


# Get the number of disks from the user
num_disks = int(input("Enter the number of disks: "))
info = "Disk 1 is the smallest and Disk " + str(num_disks) + " is the largest. The aim is to shift all the disks from " \
                                                            "source to the target column by only placing a smaller " \
                                                            "disk on a larger disk "
print("\n")
print("*" * (len(info) + 3))  # top border
print("* " + info + "*")  # content
print("*" * (len(info) + 3), "\n")  # bottom border

# Solve the Tower of Hanoi game with the given number of disks
tower_of_hanoi(num_disks, "Column 1", "Column 2", "Column 3")
