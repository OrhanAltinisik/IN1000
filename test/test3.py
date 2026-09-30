
print("-" * 80)
#If you want to print multiple words on the same line, you can use the end parameter:
print("Hello World!", end=" ")
print("I will print on the same line.")

print("-" * 80)
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
a = b = c = "Orange"
print(a)
print(b)
print(c)

print("-" * 80)
x = 5
y = "hello"
# Print the type of x
print(type(x))
print(type(y))

print("-" * 80)
x = 3.5
print(x + 1)        # 4.5
print(float("3.5")) # 3.5, turns a str into a float
print(type(x))
print(int(x))     # 3, int() cuts off the decimals
print(type(x))

print("-" * 80)
tekst = "123"
tall = int(tekst)
print(tall + 1)   # 124

print("-" * 80)
print("\033[31mThis text is red!\033[0m")
print("\x1b[1m\x1b[32mBold green text!\x1b[0m")
print("\u001b[4mThis is underline\u001b[0m")
print("hey")