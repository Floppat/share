import random
class Pet:
    def __init__(
        self,
        damage: int = 2, 
        health: int = 100, 
        stamina: int = 100, 
        defense: int = 1,
        minlvl: int = 1,
        maxlvl: int = 5,
        floor: int = 1 
     ):
        self.damage = damage
        self.max_health, self.health = health, health
        self.max_stamina, self.stamina = stamina, stamina
        self.defense = defense
        self.minlvl = minlvl
        self.maxlvl = maxlvl
        self.floor = floor

    def __repr__(self) -> str:
        return (f'<Здоровье питомца: {self.health}/{self.max_health}, '
                f'выносливость: {self.stamina}/{self.max_stamina}, сила: {self.damage}, защита: {self.defense}>')
    
    def __bool__(self) -> bool:
        return self.health > 0

    def can_attack(self) -> bool:
        return self.stamina >= 60
    def attack(self, target_pet):
        damage_dealt = self.damage - target_pet.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        target_pet.health -= damage_dealt


    def can_feed(self) -> bool:
        return self.health <= 80
    def feed(self):
        self.health += 20
    

    def can_sleep(self) -> bool:
        return self.stamina < 40
    def sleep(self):
        self.stamina = 100
    

    def can_train(self) -> bool:
        return self.health >= 20 and self.stamina >= 40
    def train(self):
        self.health -= 10
        self.stamina -= 40
        self.damage += 2

     
class Enemy:
    def __init__(self, target_pet):
        self.damage = random.randint(target_pet.minlvl, target_pet.maxlvl)
        self.health = random.randint(50, 100)
        self.defense = random.randint(target_pet.floor, target_pet. minlvl)

    def __repr__(self) -> str:
        return (f'<Здоровье врага {self.health}, '
                f'сила врага {self.damage}, защита врага {self.defense}>')
    
    def __bool__(self) -> bool:
        return self.health > 0

    def attack(self, target_pet):
        damage_dealt = self.damage - target_pet.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        target_pet.health -= damage_dealt
