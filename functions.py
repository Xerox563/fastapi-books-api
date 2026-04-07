def my_fun(name,age):
    print(f"Hey Function !! My name is {name} and I am {age} years old developer.")


my_fun("eric",19)

def print_Numbers(highest_num,lowest_num):
    print("highest_num: ",highest_num)
    print("lowest_num: ",lowest_num)

print_Numbers(2,19) # confusing  
print("\nafter Debugging \n")  
print_Numbers(lowest_num=3,highest_num=10)

def print_list(arr):
    print("List of Numbers: ",arr)
    p = 1
    for x in arr:
        p*=x
    print("Product of Numbers: ",p)

arr = [1,2,3,4,5,8]
print_list(arr)        
