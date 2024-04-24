import discord
from pets import Pet, Enemy
from discord.ext import commands
from users import User

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())
users_database = list()

def get_user(user_id: int) -> User | None:
    for user in users_database:
        if user_id == user.user_id:
            return user
    return None

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

@bot.command('register')
async def register(message, nickname):
    if get_user(user_id=message.author.id):
        await message.send('Вы уже зарегистрированы')
        return

    users_database.append(
        User(user_id=message.author.id, user_nickname=nickname)
    )
    await message.send('Регистрация прошла успешно')

@bot.command('train')
async def train(message):
    user = get_user(user_id=message.author.id)

    if not user:
        await message.send('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return

    await user.train(message=message)

@bot.command('feed')
async def feed(message):
    user = get_user(user_id=message.author.id)

    if not user:
        await message.send('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return

    await user.feed(message=message)

@bot.command('attack')
async def attack(message):
    user = get_user(user_id=message.author.id)

    if not user:
        await message.send('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return

    await user.attack(message=message)

@bot.command('sleep')
async def sleep(message):
    user = get_user(user_id=message.author.id)

    if not user:
        await message.send('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return

    await user.sleep(message=message)

@bot.command('shop')
async def shop(message, item):
    user = get_user(user_id=message.author.id)

    if not user:
        await message.send('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return

    await user.shop(message=message)

bot.run('')
