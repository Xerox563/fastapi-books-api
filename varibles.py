f_name = "eric"
l_name= "Jeffrey"

# string formatting
# sentence = "Hi {} {} How r uu ??"
# print(sentence.format(f_name,l_name))

# print(f"Hi {f_name} {l_name} I Hope You are Learning !!")

# user input
name = input("Enter Your first Name: ")
#print(name)
days = input("How may Days Before your birthday:")
#print(days)
print(f"Hi {name} only {days} days"
       f" before your birthday ..")

print(type(days))
weeks = round(int(days)/7,2)
print(type(days))
print(type(weeks))
print(f"Hi {name} only {weeks} weeks"
       f" before your birthday ..")


