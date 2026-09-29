import random

class Cat:
    def __init__(self, name, row, column):
        self.name = name
        self.index = row*column + row

cat_list = [
    [Cat("a",0,0), Cat("b",0,1), Cat("c",0,2)],
    [Cat("d",1,0), Cat("e",1,1), Cat("f",1,2)]    
           ]

lst = []

names_by_letter = {}

# end up with {"A": ["Ash", "Apricot", "Angus"], "B": [...], ...}
with open("cat_names.txt") as f:
    for line in f:
        letter, names = line.strip().split(": ")
        names_by_letter[letter] = names.split(", ") 

def make_cat_table(row, col):
    skips_allowed = 26 - row*col

    names = []

    for letter in names_by_letter:
        if skips_allowed != 0:
            if random.random() < 0.5:
                names.append(random.choice(names_by_letter[letter]))
            else: 
                skips_allowed - 1
                continue


    for i in  range (row):
        for j in range (col):
            # TO-DO 




def find_neighbors(matrix, row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    neighbors = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_r, new_c = row + dr, col + dc
        
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbors.append(matrix[new_r][new_c])
            
    return neighbors


