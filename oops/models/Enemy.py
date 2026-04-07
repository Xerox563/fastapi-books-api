'''
Enemy Object:
- Name / Type of Enemey
- Health Points
- Attack Damage
'''

class Enemy:
    # type_of_enemy: str
    # health_points: int = 10
    # attack_damage: int = 1

    def __init__(self,type_of_enemy,health_points=10,attack_damage=1):
     self.__type_of_enemy = type_of_enemy
     self.health_points = health_points
     self.attack_damage = attack_damage


    # getter : to get the value of a private variable
    def get_type_of_enemy(self):
       return self.__type_of_enemy 
    
    # setter : to set/change the value of a private variable
    def set_type_of_enemy(self,val):
       self.__type_of_enemy = val; 
    
    def talk(self): # self points to the current object
        print(f"I am a {self.__type_of_enemy}. Be Prepared to Fight !!")

    def walk_forward(self): # self points to the current object
        print(f"{self.__type_of_enemy}. Moves closer to you !!")

    def attack(self): # self points to the current object
        print(f"{self.__type_of_enemy} attacks for {self.attack_damage} damage !!")




# Constructor: are used to create and initialize an object of a class with or without starting values .
# - Default/Empty Constructor: 
'''
class Enemy1:
  type_of_enemy: str
  health_points: int = 10
  attack_damage: int = 1

  def __init__(self): # python automatically creates this for you if no constrcutor is found !!
    pass

  def talk(self):
    print("I am an Enemy !!")  

# - No arguement Constructor: 
class Enemy2:
  type_of_enemy: str
  health_points: int = 10
  attack_damage: int = 1

  def __init__(self):
    print("New Enemy created with no stating values !!") 

  def talk(self):
    print("I am an Enemy !!")  

# - Paramterised Constructor: 
class Enemy3:
  type_of_enemy: str
  health_points: int = 10
  attack_damage: int = 1

   def __init__(self,type_of_enemy,health_points=10,attack_damage=1):
    self.type_of_enemy = type_of_enemy
    self.health_poins = health_points
    self.attack_damage = attack_damage

  def talk(self):
    print("I am an Enemy !!")  WWWW
  
# object creation    
enemy = Enemy("Zoombie")
'''



