from character import Character
from os import system


def main():
    clear()
    enemy = Character('Evil Wizard', 100, 30, 1.00, 20)

    name = input('What is your name? ')
    if type(name) is not str:
        name = input('Invalid input, try again: ')

    user = Character(name, 100, 30, 1.00, 20)

    while enemy.health > 0 and user.health > 0:
        print(f'The available actions are attack, charge, heal, and swap')
        action = input('What would you like to do? ')

        stamina = 1
        while stamina > 0:
            if action.lower() == 'attack':
                print(f'\n')
                user.attack(enemy)
                stamina -= 1
            elif action.lower() == 'charge':
                print(f'\n')
                user.charge()
                stamina -= 1
            elif action.lower() == 'heal':
                print(f'\n')
                user.heal()
                stamina -= 1
            elif action.lower() == 'swap':
                print(f'Swap to which staff? (Basic, Electric, Fire, Poison, Ice)')
                staff = input('--> ')
                while not user.swap(staff):
                    staff = input('--> ')
                stamina -= 1
            else:
                print('Invalid action')
                action = input('What would you like to do? ')

        enemy.ai(user)
        input('(Press Enter to continue)')
        clear()

        user.update(enemy)
        enemy.update(user)


def clear() -> None:
    system('cls')


if __name__ == '__main__':
    main()
