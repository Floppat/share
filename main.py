import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())

class Pet:
    def __init__(
        self,
        damage: int = 2, 
        health: int = 100, 
        stamina: int = 100, 
        defense: int = 1,
        coins: int = 0,
        minlvl: int = 1,
        maxlvl: int = 5,
        floor: int = 1 
     ):
        self.damage = damage
        self.max_health, self.health = health, health
        self.max_stamina, self.stamina = stamina, stamina
        self.defense = defense
        self.coins = coins
        self.minlvl = minlvl
        self.maxlvl = maxlvl
        self.floor = floor

    def __repr__(self) -> str:
        return (f'<Здоровье питомца: {self.health}/{self.max_health}, '
                f'выносливость: {self.stamina}/{self.max_stamina}, сила: {self.damage}, защита: {self.defense}>')


    def can_attack(self) -> bool:
        return self.stamina >= 60
    def attack(self, target_pet):
        self.stamina -= 60
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

pet = Pet()
class Enemy:
    def __init__(self, target_pet):
        self.damage = random.randint(target_pet.minlvl, target_pet.maxlvl)
        self.max_health, self.health = random.randint(50, 100)
        self.defense = random.randint(target_pet.floor, target_pet. minlvl)

    def __repr__(self) -> str:
        return (f'<Здоровье врага {self.health}/{self.max_health}, '
                f'сила врага {self.damage}, защита врага {self.defense}>')
    def attack(self, target_pet):
        damage_dealt = self.damage - target_pet.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        target_pet.health -= damage_dealt

@bot.command('train')
async def train(message):
    if not pet.can_train():
        await message.send('сперва вашему питомцу следует восстановить силы')
        return
    await message.send('питомец прошёл изнурительные тренеровки')
    pet.train()
    await message.send(pet)
    return
        
@bot.command('feed')
async def feed(message):
    if not pet.can_feed():
        await message.send('Ваш питомец не голоден')
        return
    await message.send('питомец сытно поел')
    pet.feed()
    await message.send(pet)
    return
@bot.command('sleep')
async def sleep(message):
    if not pet.can_sleep():
        await message.send('Ваш питомец ещё не устал')
        return
    await message.send('питомец выспался')
    pet.sleep()
    await message.send(pet)
    return

@bot.command('attack')
async def attack(message):
    if not pet.can_train():
        await message.send('сперва вашему питомцу следует восстановить силы')
        return
    enemy = Enemy()
    await message.send('вы атакуете врага')
    while True:
        enemy.attack(pet)
        pet.attack(enemy)
        await message.send(f'ваш питомец: {pet}\n'
                           f'ваш враг: {enemy}')

        if not pet:
            await message.send('вы проиграли!')
            return

        if not enemy:
            pet.coins += 100
            pet.minlvl += 2
            pet.maxlvl += 2
            pet.floor += 1
            await message.send('вы выиграли. противник стал посильнее.\n'
                               'вы заработали 100 монет\n'
                               f'итого монет: {pet.coins}')
            return       
bot.run('')
