from random import randint


def think(self, user):
    weight = []
    shieldRatio = -((self.shield + 0.01) / self.maxShield) // 0.25 + 5
    healthRatio = -((self.health + 0.01) / self.maxHealth) // 0.25 + 5
    userShieldRatio = -((user.shield + 0.01) / user.maxShield) // 0.2 + 7
    userHealthRatio = -((user.health + 0.01) / user.maxHealth) // 0.2 + 7

    # Add attack weight depending on user's shield depletion
    while userShieldRatio > 0:
        weight.append('attack')
        userShieldRatio -= 1

    # Adds attack weight depending on user's health depletion
    while userHealthRatio > 0:
        weight.append('attack')
        userHealthRatio -= 1

    # Adds charge weight depending on shield missing
    while shieldRatio > 0:
        weight.append('charge')
        shieldRatio -= 1

    # Adds heal weight depending on health missing
    while healthRatio > 0:
        weight.append('heal')
        healthRatio -= 1

    # Adds/removes action weights depending on debuffs
    for debuff, stack in self.effect.items():
        if stack > 0:
            if debuff == 'electric':
                if weight.count('charge') > 0:
                    weight.remove('charge')
            if debuff == 'fire':
                if weight.count('heal') > 0:
                    weight.remove('heal')
                    weight.append('charge')
            if debuff == 'poison':
                weight.append('heal')

    # Sorts weights and randomly chooses one
    weight.sort()
    action = weight[randint(0, len(weight) - 1)]
    if action == 'attack':
        self.attack(user)
    elif action == 'charge':
        self.charge()
    elif action == 'heal':
        self.heal()
