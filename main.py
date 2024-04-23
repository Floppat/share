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

    def petis(self) -> bool:
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


    def can_buy(self, money) -> bool:
        return self.coins >= money
    def buy(self, coin, defens):
        self.coins -= coin
        self.defense = defens
pet = Pet()
class Enemy:
    def __init__(self, target_pet):
        self.damage = random.randint(target_pet.minlvl, target_pet.maxlvl)
        self.health = random.randint(50, 100)
        self.defense = random.randint(target_pet.floor, target_pet. minlvl)

    def __repr__(self) -> str:
        return (f'<Здоровье врага {self.health}, '
                f'сила врага {self.damage}, защита врага {self.defense}>')
    def enemyis(self) -> bool:
        return self.health > 0
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
    enemy = Enemy(target_pet=pet)
    await message.send('вы атакуете врага')
    pet.stamina -= 60
    while True:
        enemy.attack(target_pet=pet)
        pet.attack(target_pet=enemy)
        await message.send(f'ваш питомец: {pet}\n'
                           f'ваш враг: {enemy}')

        if not pet.petis():
            await message.send('вы проиграли!')
            return

        if not enemy.enemyis():
            pet.coins += 100
            pet.minlvl += 2
            pet.maxlvl += 2
            pet.floor += 1
            await message.send('вы выиграли. противник стал посильнее.\n'
                               'вы заработали 100 монет\n'
                               f'итого монет: {pet.coins}')
            return       
@bot.command('guide')
async def guide(message):
    await message.send('каждый день (до использования команды /sleep) вы можете 2 раза потренироватся, затем 1 раз поесть.')
    await message.send('за день можно 2 раза потренироватся, или 1 раз потренироватся и 1 раз подратся')
    await message.send('совет: лучше перед боем не тренероватся, ведь будет меньше здоровья, а поесть вы не сможете')
    await message.send('тактика про: каждый день 2 раза тренироваться и 1 раз есть, после того как набралось 10 атаки на следущий день идти в бой')
    await message.send('также противник сильнеет не по дням, а по боям, так что покупайте артефакты, ведь они повышают защиту')
@bot.command('cmd')
async def cmd(message):
    await message.send('попробуйте /train  (+сила; -здоровье; -выносливость)')
    await message.send('попробуйте /feed  (+здоровье; +выносливость)')
    await message.send('попробуйте /attack  (-здоровье (ведь это же битва))')
    await message.send('попробуйте /sleep  (полное восстановление выносливости)')
    await message.send('попробуйте /cmd')
    await message.send('попробуйте /guide  (ввод в игру)')
    await message.send('попробуйте /shop  (покупка артефактов)')
@bot.command('shop')
async def shop(message):
    await message.send('/s400;   400 монет    5 защиты')   
    await message.send('/s800;   800 монет   10 защиты') 
    await message.send('/s1200;  1200 монет  15 защиты')
    await message.send('/s1600;  1600 монет  20 защиты')
    await message.send('/s2000;  2000 монет  25 защиты')
@bot.command('s400')
async def s400(message):
    if not pet.can_buy(400):
        await message.send('денег не хватает')
        await message.send(f'ваш питомец: {pet}')  
        return     
    pet.buy(400, 5)
    await message.send(f'ваш питомец: {pet}')
@bot.command('s800')
async def s800(message):
    if not pet.can_buy(800):
        await message.send('денег не хватает')
        await message.send(f'ваш питомец: {pet}')  
        return     
    pet.buy(800, 10)
    await message.send(f'ваш питомец: {pet}')
@bot.command('s1200')
async def s1200(message):
    if not pet.can_buy(1200):
        await message.send('денег не хватает')
        await message.send(f'ваш питомец: {pet}')  
        return     
    pet.buy(1200, 15)
    await message.send(f'ваш питомец: {pet}')
@bot.command('s1600')
async def s1600(message):
    if not pet.can_buy(1600):
        await message.send('денег не хватает')
        await message.send(f'ваш питомец: {pet}')  
        return     
    pet.buy(1600, 20)
    await message.send(f'ваш питомец: {pet}')
@bot.command('s2000')
async def s2000(message):
    if not pet.can_buy(2000):
        await message.send('денег не хватает')
        await message.send(f'ваш питомец: {pet}')  
        return     
    pet.buy(2000, 25)
    await message.send(f'ваш питомец: {pet}')
bot.run('')
