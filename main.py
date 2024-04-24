import discord
from discord.ext import commands
from users import User

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())
users_database = list()

def get_user(user_id: int) -> User | None:
    for user in users_database:
        if user_id == user.user_id:
            return user
    return None

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов.')
    synced = await bot.tree.sync()
    print(f'{len(synced)} / команды доступны.')

@bot.tree.command(name='guide', description='Отображает справку по игре')
async def guide(interaction: discord.Interaction):
    message =  ('каждый день (до использования команды /sleep) вы можете 2 раза потренироватся, затем 1 раз поесть.\n'
                'за день можно 2 раза потренироватся, или 1 раз потренироватся и 1 раз подратся\n'
                'совет: лучше перед боем не тренероватся, ведь будет меньше здоровья, а поесть вы не сможете\n'
                'тактика про: каждый день 2 раза тренироваться и 1 раз есть, после того как набралось 10 атаки на следущий день идти в бой\n' 
                'также противник сильнеет не по дням, а по боям, так что покупайте артефакты, ведь они повышают защиту\n')
    await interaction.response.send_message(message)

@bot.tree.command(name='cmd', description='Отображает команды бота')
async def cmd(interaction: discord.Interaction):
    message = ('попробуйте /register   (после регистрации доступны все команды)\n'
    'попробуйте /guide  (ввод в игру)\n'
    'попробуйте /train  (+сила; -здоровье; -выносливость)\n'
    'попробуйте /feed  (+здоровье; +выносливость)\n'
    'попробуйте /sleep  (полное восстановление выносливости)\n'
    'попробуйте /attack  (-здоровье (ведь это же битва))\n'
    'попробуйте /shop  (покупка артефактов)\n'
    'попробуйте /cmd\n')
    await interaction.response.send_message(message)

@bot.tree.command(name='register', description='Позволяет зарегистрироваться в игре')
async def register(interaction: discord.Interaction, nickname: str):
    if get_user(user_id=interaction.user.id):
        await interaction.response.send_message('Вы уже зарегистрированы')
        return
    users_database.append(
        User(user_id=interaction.user.id, user_nickname=nickname)
    )
    await interaction.response.send_message('Регистрация прошла успешно')

@bot.tree.command(name='train', description='Потренируйте питомца!')
async def train(interaction: discord.Interaction):
    user = get_user(user_id=interaction.user.id)
    if not user:
        await interaction.response.send_message('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return
    await user.train(interaction=interaction)

@bot.tree.command(name='feed', description='Покормите питомца!')
async def feed(interaction: discord.Interaction):
    user = get_user(user_id=interaction.user.id)
    if not user:
        await interaction.response.send_message('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return
    await user.feed(interaction=interaction)

@bot.tree.command(name='attack', description='Покормите питомца!')
async def attack(interaction: discord.Interaction):
    user = get_user(user_id=interaction.user.id)
    if not user:
        await interaction.response.send_message('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return
    await user.attack(interaction=interaction)

@bot.tree.command(name='sleep', description='Покормите питомца!')
async def sleep(interaction: discord.Interaction):
    user = get_user(user_id=interaction.user.id)
    if not user:
        await interaction.response.send_message('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return
    await user.sleep(interaction=interaction)

@bot.tree.command(name='shop', description='Покормите питомца!')
async def shop(interaction: discord.Interaction):
    user = get_user(user_id=interaction.user.id)
    if not user:
        await interaction.response.send_message('Вы не зарегистрированы, поэтому не можете использовать эту команду.')
        return
    await user.shop(interaction=interaction)

bot.run('')
