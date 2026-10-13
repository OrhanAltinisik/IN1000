import random

solution = False
number = random.randint(1, 20)
print("guess a number")



while solution == False:
    guess = int(input())
    if guess == number:
        print("Correct!")
        solution = True
    elif guess > number:
        print("Too Hight")
    elif guess < number:
        print("Too low")