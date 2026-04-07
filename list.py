""" Lists are collection of Data , and they are mutable ."""

my_list = [10,20,30,40,50]
print(my_list)

my_str_list = ["alex","Jambo","Rambo","Thanos","Rominos"]
print(my_str_list)
print(f"last index print {my_str_list[-1]} ")
print(f"1st index print {my_str_list[1]} ")

# slicing
print(my_str_list[2:4]) # start from index 2 and end 4 - 1.

print(my_str_list[0:]) # start from index 0 and print till whole string ends
my_str_list.append("Jack") # appending element 
print(my_str_list)
my_str_list.insert(0,"Alpha_x") # insertion at index
print(my_str_list)
my_str_list.remove("Alpha_x") # delete element with val
print(my_str_list)
my_str_list.pop(0) # pops element [index one]
print(my_str_list)
my_str_list.sort() # pops element [index one]
print(my_str_list)

my_str_list[0] = "Jack:Slayer"
print(my_str_list) # list are mutable
print(len(my_str_list)) 


