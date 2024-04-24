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
        await interaction.response.send_message('питомец прошёл изнурительные тренеровки')
        self.pet.train()
        await interaction.response.send_message(self.pet)
        return

    async def feed(self, interaction: Interaction ):
        if not self.pet.can_feed():
            await interaction.response.send_message('Ваш питомец не голоден')
            return
        await interaction.response.send_message('питомец сытно поел')
        self.pet.feed()
        await interaction.response.send_message(self.pet)
        return

    async def attack(self, interaction: Interaction ):
        if not self.pet.can_train():
            await interaction.response.send_message('сперва вашему питомцу следует восстановить силы')
            return
        enemy = Enemy(target_pet=self.pet)
        await interaction.response.send_message('вы атакуете врага')
        self.pet.stamina -= 60
        while True:
            enemy.attack(target_pet=self.pet)
            self.pet.attack(target_pet=enemy)
            await interaction.response.send_message(f'ваш питомец: {self.pet}\n'
                            f'ваш враг: {enemy}')

            if not self.pet:
                await interaction.response.send_message('вы проиграли!')
                return

            if not enemy:
                self.coins += 100
                self.pet.minlvl += 2
                self.pet.maxlvl += 2
                self.pet.floor += 1
                await interaction.response.send_message('вы выиграли. противник стал посильнее.\n'
                                'вы заработали 100 монет\n'
                                f'итого монет: {self.pet.coins}')
                return       
    async def sleep(self, interaction: Interaction ):
        if not self.pet.can_sleep():
            await interaction.response.send_message('Ваш питомец ещё не устал')
            return
        await interaction.response.send_message('питомец выспался')
        self.pet.sleep()
        await interaction.response.send_message(self.pet)
        return
    async def shop(self, interaction: Interaction, item ):
        await interaction.response.send_message('item=1;  400 монет')   
        await interaction.response.send_message('item=2;  800 монет') 
        await interaction.response.send_message('item=3;  1200 монет')
        await interaction.response.send_message('item=4;  1600 монет')
        await interaction.response.send_message('item=5;  2000 монет')

        if item not in ('1', '2', '3', '4', '5'):
            await interaction.response.send_message('Неправильный item, выберите из списка (1 2 3 4 5)')
            return

        shop_pets = {
            '1': Pet(health=110, stamina=125, defense=5, shop_cost=400),
            '2': Pet(health=130, stamina=140, defense=10, shop_cost=800),
            '3': Pet(health=160, stamina=160, defense=15, shop_cost=1200),
            '4': Pet(health=225, stamina=200, defense=15, shop_cost=1600),
            '5': Pet(health=300, stamina=220, defense=20, shop_cost=2000)
        }

        if self.coins < shop_pets[item].shop_cost:
            await interaction.response.send_message(f'Недостаточно денег: чтобы купить этого пета, нужно {shop_pets[item].shop_cost} денег')
            return

        self.coins -= shop_pets[item].shop_cost
        self.pet = deepcopy(shop_pets[item])
        await interaction.response.send_message(f'Ваш новый пет: {self.pet}')
