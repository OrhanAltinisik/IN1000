class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades) / len(self.grades)

    def show(self):
        print(self.name + ": " + str(self.grades) + " average = " + str(round(self.average(), 1)))


def add_student(students):
    name = input("Name: ")
    if name in students:
        print("That student already exists")
    else:
        students[name] = Student(name)
        print("Added")

def add_grade(students):
    name = input("Which student? ")
    if name in students:
        grade = int(input("Grade (1-6): "))
        if 1 <= grade <= 6:
            students[name].add_grade(grade)
            print("Grade added")
        else:
            print("Grade must be between 1 and 6")
    else:
        print("No student with that name")

def show_students(students):
    if len(students) == 0:
        print("No students yet")
    for student in students.values():
        student.show()

def best_student(students):
    best = None
    for student in students.values():
        if best == None or student.average() > best.average():
            best = student
    if best == None:
        print("No students yet")
    else:
        print("Best student is " + best.name + " with average " + str(round(best.average(), 1)))

def main():
    students = {}
    while True:
        print("1 = add student, 2 = add grade, 3 = show all, 4 = best student, 5 = quit")
        choice = int(input("Choice: "))
        if choice == 1:
            add_student(students)
        elif choice == 2:
            add_grade(students)
        elif choice == 3:
            show_students(students)
        elif choice == 4:
            best_student(students)
        elif choice == 5:
            break
        else:
            print("Wrong choice")

main()
