import random


class Cat:
    def __init__(self, name, row, column, index):
        self.name = name        # display name, e.g. "Biscuit"
        self.row = row          # row in the grid (starts at 0)
        self.column = column    # column in the grid (starts at 0)
        self.index = index      # position in a flat list, used as world[index]


def make_cat_table(row, col, names_by_letter):
    """Build a row x col grid of cats with names in (mostly) alphabetical order."""
    skips_allowed = 26 - row * col   # how many letters we can skip and still have enough names
    names = []

    # Walk through the letters A to Z, sometimes skipping one
    for letter in names_by_letter:
        if random.random() < 0.2 and skips_allowed != 0:
            skips_allowed -= 1
            continue
        else:
            names.append(random.choice(names_by_letter[letter]))  # pick 1 of the 3 names
            if len(names) == row * col:
                break

    grid = [] 
    index = 0

    # Fill the grid row by row, taking names from the front of the list
    for i in range(row):
        grid.append([])
        for j in range(col):
            grid[i].append(Cat(names.pop(0), i, j, index))
            index += 1

    return grid


def find_neighbors(matrix, row, col):
    """Return the cats directly above, below, left and right (no diagonals)."""
    rows = len(matrix)       # number of rows in the grid
    cols = len(matrix[0])    # number of columns in the grid
    neighbors = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right

    # Check each direction and keep the ones that are inside the grid
    for dr, dc in directions:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbors.append(matrix[new_r][new_c])

    return neighbors


def main():
    # Load names from file into {"A": ["Ash", "Apricot", "Angus"], "B": [...], ...}
    names_by_letter = {}
    with open("cat/cat_names.txt") as f:
        for line in f:
            letter, names = line.strip().split(": ")
            names_by_letter[letter] = names.split(", ")

    cat_grid = make_cat_table(3, 2, names_by_letter)

    # Print each row's size and the cats in it
    for cat_row in cat_grid:
        print(len(cat_row))
        for cat in cat_row:
            print(cat.name, cat.index)


if __name__ == "__main__":
    main()