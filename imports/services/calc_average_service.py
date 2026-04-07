def calc_homework(homework_assignment_arg):
    sum_of_grades = 0
    for x in homework_assignment_arg.values():
        sum_of_grades += x
    final_grade = round(sum_of_grades/len(homework_assignment_arg),2)
    print("Final Grade: ",final_grade)   


