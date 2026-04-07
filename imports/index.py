from imports.services.calc_average_service import calc_homework 
from imports.services.useful_function_list import (
    calc_sum,
    calc_max,
    calc_min,
    calc_avg
)

homework_grades = {
    'hw_1':98,
    'hw_2':83,
    'hw_3':89,
    'hw_4':78,
    'hw_5':70
}

calc_homework(homework_grades)
calc_sum(homework_grades)
calc_max(homework_grades)
calc_min(homework_grades)
calc_avg(homework_grades)










# Randome
import random
types_of_drink = ['Soda','Coffee','Water','Tea']
print(random.choice(types_of_drink))
print(random.randint(1,100))

# import math
import math
square_root = math.sqrt(70)
print(square_root)
