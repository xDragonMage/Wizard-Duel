from random import randint
from enemyAI import think
from staffs import staffList


class Character:

    def __init__(self, name: str, health: int, shield: int, power: float, dodge: int) -> None:
        self.name = name
        self.health = health
        self.maxHealth = health
        self.shield = shield
        self.maxShield = shield
        self.power = power
        self.dodge = dodge
        self.staff = staffList['basic']

        self.effectMultiplier = 0.25
        self.chargeMultiplier = 15
        self.healMultiplier = 20
        self.poisonMultiplier = 5
        self.chargeDebuff = 0.4
        self.healDebuff = 0.5

        self.effect = dict(electric=0, fire=0, poison=0, ice=0)
        self.effectDoT = dict(poison=5)

    # Attack action which checks staff type, effect status, dodge chance, and applies debuffs
    def attack(self, target) -> None:
        # Checks effect statuses and applies temporary debuffs
        if target.effect['ice'] > 0:
            tempDodge = max((target.dodge - 10), 0)
        else:
            tempDodge = target.dodge

        # Checks if target dodges, executes if hit
        if randint(1, 100) >= tempDodge:
            # Calculates base damage
            totalDamage = self.staff.damage * self.power
            # Checks target's shield
            if target.shield > 0:
                # Checks if effect type is effective against shield, applies multiplier
                if self.staff.effectType == 'electric':
                    totalDamage *= (1 + self.effectMultiplier)

                # Checks if damage done is greater than shield, then calculates and applies damage to health
                if target.shield > totalDamage:
                    target.shield -= totalDamage
                    target.shield = max(target.shield, 0)
                    self.displayAtk(targetName=target.name, overDamage=-1, damage=totalDamage, damaged='shield')
                else:
                    overDamage = totalDamage - target.shield
                    target.shield = 0
                    target.health -= overDamage
                    self.displayAtk(targetName=target.name, overDamage=overDamage)

            # Focuses on target's health since shield is depleted
            else:
                # Checks if type is effective against health, applies multiplier
                if self.staff.effectType == 'fire':
                    totalDamage *= (1 + self.effectMultiplier)

                # Calculates damage, reduces target health, and calls to print action
                target.health -= totalDamage
                target.health = max(target.health, 0)
                self.displayAtk(targetName=target.name, overDamage=-1, damage=totalDamage, damaged='health')

            # Applies status effects
            for staffEffect in target.effect:
                if self.staff.effectType == staffEffect:
                    target.effect[staffEffect] = self.staff.duration

        else:
            print(f'{target.name} has dodged the attack!\n')

    # Charge action which recharges shield by chargeMultiplier * power level
    def charge(self) -> None:
        totalCharge = self.chargeMultiplier * self.power
        # Checks if under electric debuff, reduces charge by chargeDebuff and prints status effect
        if self.effect['electric'] > 0:
            totalCharge *= (1 - self.chargeDebuff)
            print(f'{self.name} is under the electric debuff!')
        # Adds charge to shield, prevents overcharging, and prints charge text
        self.shield += totalCharge
        self.shield = min(self.shield, self.maxShield)
        print(f'{self.name} charged their shield for {totalCharge}')

    # Heal action which heals by healMultiplier * power level
    def heal(self) -> None:
        totalHeal = self.healMultiplier * self.power
        # Checks if under fire debuff, reduces heal by healDebuff and prints status effect
        if self.effect['fire'] > 0:
            totalHeal *= (1 - self.healDebuff)
            print(f'{self.name} is under the fire debuff!')
        # Adds health, prevents overhealing, and prints health text
        self.health += totalHeal
        self.health = min(self.health, self.maxHealth)
        print(f'{self.name} healed for {totalHeal}')

    # Swap action which changes users staff
    def swap(self, staff: str) -> bool:
        # Sets staff string to lowercase
        staff = staff.lower()
        # Checks if inputted name matches existing staff
        if staff in staffList:
            self.staff = staffList[staff]
            print(f'{self.name} has equipped the {staff} staff\n')
            return True
        else:
            print(staff + ' does not exist')

    # Prints action text
    def displayAtk(self, **action) -> None:
        if action['overDamage'] >= 0:
            if action['overDamage'] == 0:
                print(f'{self.name} destroyed {action["targetName"]}\'s shield!\n')
            else:
                print(f'{self.name} destroyed {action["targetName"]}\'s shield and dealt {action["overDamage"]}!\n')
        else:
            print(f'{self.name} dealt {action["damage"]} to {action["targetName"]}\'s {action["damaged"]}!\n')

    # Updates status, display current health and shield
    def update(self, target) -> None:
        for debuff, stack in self.effect.items():
            if stack > 0:
                # Checks if under damage debuff
                if debuff in self.effectDoT:
                    effectDamage = target.effectDoT[debuff] * target.power
                    self.health -= effectDamage
                    print(f'{self.name} has taken {effectDamage} from {debuff}!')
                # Reduces existing debuff durations by 1
                self.effect[debuff] -= 1
        # Prints current health and shield
        if self.health > 0:
            if self.shield > 0:
                print(f'{self.name}\'s shield is {self.shield}/{self.maxShield}')
            print(f'{self.name}\'s health is {self.health}/{self.maxHealth}\n')
        else:
            print(f'{self.name} has been defeated!')

    def ai(self, target):
        think(self, target)
