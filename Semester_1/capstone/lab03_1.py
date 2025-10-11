# 1 Two Highest Scores

"""
In a section in the notebook, implement a program that prompts the user to enter the
number of students and each student's name and score. Then, it displays the top two
students with their names and scores. To increase the memory efficiency of your
application, write your application with NO data structure like a list, array, etc. You
will learn these concepts in the following weeks.
"""

number_of_students = int(input("Enter the number of students: "))


def two_highest_scores(n_of_students: int):
    # Create variables to store our two happy students.
    first_highest_score = 0
    first_highest_score_student = None

    second_highest_score = 0
    second_highest_score_student = None

    # While loop to capture all the students according to the user specified number.
    n = 0
    while n < n_of_students:
        # Get name and student
        student_name = str(input("Enter a student name: "))
        student_score = float(input("Enter a student score: "))

        if student_score > first_highest_score:
            # If the new student has the highest score, make the old highest score the second heights
            second_highest_score_student = first_highest_score_student
            second_highest_score = first_highest_score

            # Then add the save the new highest score in the variable
            first_highest_score_student = student_name
            first_highest_score = student_score

        elif student_score > second_highest_score:
            # In case the student is not the highest, but the second heights, just replace the second heights
            second_highest_score_student = student_name
            second_highest_score = student_score
        # Iterate n to end the while loop
        n += 1

    # Print our best 2 students
    print(f"Top Two Students\n"
          f"{first_highest_score_student}'s score is {first_highest_score}\n"
          f"{second_highest_score_student}'s score is {second_highest_score}")


# Before running the function, verify that the user asked to enter more than 2 students
if number_of_students >= 2:
    two_highest_scores(number_of_students)
else:
    # Print this if its 2 or less
    print("You must introduce two or more students")

