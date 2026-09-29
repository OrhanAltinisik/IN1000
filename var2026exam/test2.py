liste = [1, 2, 3, 4]
print(liste[0])        # first item
print(liste[-2])       # last item
liste.append(2)        # duplicates are allowed
print(liste)
index = len(liste) - 1 - liste[::-1].index(2)
liste.pop(index)

print(liste)