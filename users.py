from pets import Enemy, Pet
from copy import deepcopy
from discord import Interaction
class User:
    def __init__(self, user_id: int, user_nickname: str):
        self.user_id = user_id
        self.nickname = user_nickname
        self.coins = 0
        self.pet = Pet()

    def __repr__(self):
        return (f'--- Информация об игроке {self.nickname} ---\n'
                f'    | ID: {self.user_id}\n'
                f'    | Coins: {self.coins}\n'
                f'    | Pet: {self.pet}')
    
    async def train(self, interaction: Interaction ):
        if not self.pet.can_train():
            await interaction.response.send_message('сперва вашему питомцу следует восстановить силы')
            return
        self.pet.train()
        await interaction.response.send_message(f'питомец прошёл изнурительные тренеровки{self.pet}')
        return

    async def feed(self, interaction: Interaction ):
        if not self.pet.can_feed():
            await interaction.response.send_message('Ваш питомец не голоден')
            return
        self.pet.feed()
        await interaction.response.send_message(f'питомец сытно поел{self.pet}')
        return

    async def attack(self, interaction: Interaction ):
        if not self.pet.can_train():
            await interaction.response.send_message('сперва вашему питомцу следует восстановить силы')
            return
        enemy = Enemy(target_pet=self.pet)
        self.pet.stamina -= 60
        while True:
            enemy.attack(target_pet=self.pet)
            self.pet.attack(target_pet=enemy)

            if not self.pet:
                await interaction.response.send_message(f'вы проиграли!, ваш враг был:{enemy}\n'
                                                        f'ваши характеристики:{self.pet}')
                return

            if not enemy:
                self.coins += 100
                self.pet.minlvl += 2
                self.pet.maxlvl += 2
                self.pet.floor += 1
                await interaction.response.send_message(f'вы выиграли. противник стал посильнее. ваш враг был:{enemy}\n'
                                'вы заработали 100 монет\n'
                                f'итого монет: {self.coins}\n'
                                f'ваши характеристики:{self.pet}')
                return       
    async def sleep(self, interaction: Interaction ):
        if not self.pet.can_sleep():
            await interaction.response.send_message('Ваш питомец ещё не устал')
            return
        self.pet.sleep()
        await interaction.response.send_message(f'питомец выспался{self.pet}')
        return

    async def shop(self, interaction: Interaction, item: str):
        shop_pets = {
            '1': Pet(health=100, stamina=120, defense=5, shop_cost=400),
            '2': Pet(health=100, stamina=140, defense=10, shop_cost=800),
            '3': Pet(health=100, stamina=160, defense=15, shop_cost=1200),
            '4': Pet(health=100, stamina=160, defense=15, shop_cost=1600),
            '5': Pet(health=100, stamina=160, defense=20, shop_cost=2000)
        }
        message_items = '\n'.join([f'{item=}; {shop_pets[item].shop_cost} монет; {shop_pets[item]}' for item in shop_pets])

        if item not in shop_pets or item in ('?', 'help', 'items'):
            await interaction.response.send_message(f'Доступные для покупки артефакты:\n{message_items}')
            return

        if self.coins < shop_pets[item].shop_cost:
            await interaction.response.send_message(f'Недостаточно денег: чтобы купить этот артефакт, нужно {shop_pets[item].shop_cost} денег')
            return

        self.coins -= shop_pets[item].shop_cost
        self.pet = deepcopy(shop_pets[item])
        await interaction.response.send_message(f'Ваш пет надел артефакт: {self.pet}')
