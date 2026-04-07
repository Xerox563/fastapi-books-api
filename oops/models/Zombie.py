from models.Enemy import *

class Zombie(Enemy):
    # inheriting enemy to have all its properties here 
    def __init__(self,health_points,attack_damage): # When we kick off our zombie constructor after then
        # kick off the enemy constructor
        super().__init__(
            type_of_enemy='Zombie',
            health_points=health_points,
            attack_damage=attack_damage)
        
    def talk(self):
            print('Grumbling')

    def spread_diseases(self):
         print("The Zombie is trying to spread infection !!")        
         