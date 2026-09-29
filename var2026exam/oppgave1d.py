teller = 0
liste = [1, 2, 3, 4]
mengde = {1,1,1,2,2,3,0}
ordbok = {
        1:3,
        3:2,
        5:4
    }
for c in liste:
     if c in ordbok:
          teller += ordbok[c]
     elif c in liste:
          teller += 2
     else:
          teller = teller
print(teller)