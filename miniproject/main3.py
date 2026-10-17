def add_contact(contacts):
    name = input("Name: ")
    number = input("Number: ")
    contacts[name] = number

def find_contact(contacts):
    name = input("Find which name?")
    if name in contacts:
        print( name + ": " + contacts[name])
    else:
        print("No contacts with that name")

def remove_contact(contacts):
    name = input("Which name do you want to remove")
    if name in contacts:
        contacts.pop(name)
        print("Removed")
    else:
        print("No contacts with that name")

def main():
    contacts = {}
    while True:
        print("1 = add, 2 = show, 3 = remove, 4 = quit")
        choice = int(input("Choice:"))
        if choice == 1:
            add_contact(contacts)
        if choice == 2:
            find_contact(contacts)
        if choice == 3:
            remove_contact(contacts)
        if choice == 4:
            break
        else:
            print("WRONG NUMBER")

main()