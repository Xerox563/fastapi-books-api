from models.Zombie import *
from models.Ogre import *
zombie = Zombie(10,1)
ogre = Ogre(100,5)
print("-----------------------------------------------------")

print(f"{zombie.get_type_of_enemy()} has {zombie.health_points} health points and can do Attack of {zombie.attack_damage} ")
print(f"{ogre.get_type_of_enemy()} has {ogre.health_points} health points and can do Attack of {ogre.attack_damage} ")

print(zombie.talk())
print(ogre.talk())

print("-----------------------------------------------------")
# zombie = Enemy()
# zombie.type_of_enemy = 'Zoombie'
# print(f"{zombie.type_of_enemy} has {zombie.health_points} health points and can do Attack of {zombie.attack_damage} ")
# zombie.talk()
# zombie.walk_forward()
# zombie.attack()
# print("-----------------------------------------------------")
# Zombie = Enemy("Zombie")
# Zombie.set_type_of_enemy('Orc')
# print(Zombie.get_type_of_enemy())
# Zombie.type_of_enemy = 'Orc'
# Zombie.talk()


























# Abstraction
'''
Abstraction : Hide the implementation Details and show only the necessary details to the user .

🔹 1. What is Abstraction?

- Hide how things work inside
- Show only what user needs

🔹 2. Flashlight Example : User just sees two buttons : ON/OFF on which cliciking behaviour of beam chnages
- You press button → light ON
- You press again → light OFF

You dont know:
- wiring
- battery flow
- circuit
- internal working
✔ That hidden part = abstraction

'''

# Encapsulation + Method Overrding
'''
Encapsulation:
- Helps keep related fields abd methods together
- Makes our code cleaner and easier to read.
- Provides more flexibility to the code.
- Provides more reusability to the code .

Method Overriding:
 - Method overriding is when the child class has its own method already present in the parent class : child class method runs
 - When the child class does not have the same method, it will default to the parent class .
'''

# self 
'''
-use of self [refers to current object]
 Access object variables
 Call methods inside same class

'''

# super keyword
'''
super() : To reuse code from parent class instead of rewriting it 
class TRex:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

class Zombie(Enemy):
    def __init__(self):
        self.name = "Zombie"
        self.health = 100
        self.damage = 10

Problems:
- Code repetition 
- If parent changes → you must update everywhere
- Not scalable

----------------------------------------------

solution : 
class Zombie(Enemy):
    def __init__(self):
        super().__init__("Zombie", 100, 10)

Now:
- Reuses parent logic 
- Cleaner 
- Easier to maintain 
'''
