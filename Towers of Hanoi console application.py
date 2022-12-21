def tower_of_hanoi(n, source, auxiliary, target, step):
    if n == 1:
        print("Move disk 1 from source", source, "to target", target)
        step += 1  # increase steps by 1 for each move
        return step

    step = tower_of_hanoi(n - 1, source, target, auxiliary, step)  # recurse on the first tower
    print("Move disk", n, "from source", source, "to target", target)
    step += 1  # increase steps by 1 for each move
    step = tower_of_hanoi(n - 1, auxiliary, source, target, step)  # recurse on the second tower

    return step


# Get the number of disks from the user
num_disks = int(input("Enter the number of disks: "))
info = "Disk 1 is the smallest and Disk " + str(num_disks) + " is the largest. The aim is to shift all the disks from " \
                                                             "source to the target column by only placing a smaller " \
                                                             "disk on a larger disk "
print("\n")
print("*" * (len(info) + 3))  # top border
print("* " + info + "*")  # content
print("*" * (len(info) + 3), "\n")  # bottom border

steps = 0  # define steps before calling tower_of_hanoi

# Solve the Tower of Hanoi game with the given number of disks
steps = tower_of_hanoi(num_disks, "Column 1", "Column 2", "Column 3", steps)
print("\nMinimum number of steps to complete the game is:", steps)
