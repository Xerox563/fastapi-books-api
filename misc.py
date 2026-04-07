"""Boolean [for comparison and logical operation that requires something is true or false] and Operators"""

# like_coffee = True
# like_tea = False

# favorite_food = "Pizza"
# favorite_number = 13
# print(type(favorite_food))
# print(type(favorite_number))
# print(type(like_coffee))

# print(1 ==  2) # is 1 equals to 2
# print(1 !=  2) # is 1 not equals to 2
# print(1 > 2)
# print(1 >=  2)
# print(1 <=  2) 


# logical operators
# print(5 == 5 and 7 ==8)
# print(5 == 5 or 7 ==8)
# print(not(1 == 1)) # checking is (1 equals to 1) is not equal .

# if else

# x = 1
# age = 19
# if x == 1 and age >= 18:
#     print("x equals to 1 !!")
# else:
#     print("x is not equals to 1 !!")    
# print("Outside of if statement !!")   

# if else
age = 9
if age > 18:
    print("Age greater than 18")
elif age == 18:
    print("Age equal to 18")   
else:
    print("Age less than 18")    
print("Outside of if statement !!")    

user_dict = {
    'username':"Amit Gangwar",
    'password':"989767tghui",
    'age':23
}

print(user_dict)
print(user_dict.get('username'))
user_dict["married"] = True
user_dict.pop('age')
# user_dict.clear()
# del user_dict
print(user_dict,len(user_dict))
x = user_dict.values()
y = user_dict.items()
z = user_dict.keys()
print(x,y,z)
print(len(x))

# user_dict2 = user_dict
# user_dict2.pop('age') # this will delete the age from both of the dictionairies original also 
# to avoid this we use 
user_dict2 = user_dict.copy()
user_dict2.pop('age')