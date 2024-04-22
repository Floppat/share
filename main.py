import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())

class Pet:
    def __init__(self, health, damage, stamina, defense, coins, minlvl, maxlvl, floor):
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
    def attack(self):
        self.stamina -= 60
        damage_dealt = self.damage - Enemy.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        Enemy.health -= damage_dealt


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

pet = Pet(100, 2, 100, 1, 0, 1, 10, 1)
class Enemy:
    def __init__(self):
        self.damage = random.randint(Pet.minlvl, Pet.maxlvl)
        self.max_health, self.health = random.randint(50, 100)
        self.defense = random.randint(Pet.floor, Pet. minlvl)

    def __repr__(self) -> str:
        return (f'<Здоровье врага {self.health}/{self.max_health}, '
                f'сила врага {self.damage}, защита врага {self.defense}>')
    def attack(self):
        damage_dealt = self.damage - Pet.defense
        damage_dealt = damage_dealt if damage_dealt > 0 else 0
        Pet.health -= damage_dealt

@bot.command('train')
async def train(self, message):
    if not self.Pet.can_train():
        await message.send('сперва вашему питомцу следует восстановить силы')
        return
    await message.send('питомец прошёл изнурительные тренеровки')
    self.Pet.train()
    await message.send(pet)
    return
        
@bot.command('feed')
async def feed(self, message):
    if not self.Pet.can_feed():
        await message.send('Ваш питомец не голоден')
        return
    await message.send('питомец сытно поел')
    Pet.feed()
    await message.send(pet)
    return
@bot.command('sleep')
async def sleep(self, message):
    if not self.Pet.can_sleep():
        await message.send('Ваш питомец ещё не устал')
        return
    await message.send('питомец выспался')
    Pet.sleep()
    await message.send(pet)
    return

@bot.command('attack')
async def attack(self, message):
    if not self.Pet.can_train():
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
            Pet.coins += 100
            Pet.minlvl += 2
            Pet.maxlvl += 2
            Pet.floor += 1
            await message.send('вы выиграли. противник стал посильнее.\n'
                               'вы заработали 100 монет\n'
                               f'итого монет: {Pet.coins}')
            return       
bot.run('')
