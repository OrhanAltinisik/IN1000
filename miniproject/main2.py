def add_task(tasks):
    add = input("New task=")
    tasks.append(add)

def show_task(tasks):
    number = 1
    for task in tasks:
        print(str(number) + "." + task)
        number += 1

def remove_task(tasks):
    number = int(input("Remove which number? "))
    index = number - 1
    if 0 <= index < len(tasks):
        tasks.pop(index)
        print("Removed")
    else:
        print("That number is wrong")

def main():
    tasks = []
    while True:
        print("1 = add", "2 = show", "3 = remove", "4 = quit")
        choice = input("choice:")
        if choice == 1:
            add_task(tasks)
        elif choice == 2:
            show_task(tasks)
        elif choice == 3:
            show_task(tasks)
            remove_task(tasks)
        elif choice == 4:
            print("Good bye motherfucker")
            break
        else:
            print("wrong number")
main()