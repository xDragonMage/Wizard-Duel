# Staff class which has staff name, staff damage, staff effect type, and duration of the effect
class Staff:
    def __init__(self, name: str, damage: int, effectType: str, duration: int) -> None:
        self.name = name
        self.damage = damage
        self.effectType = effectType
        self.duration = duration


# Premade staffs
basicStaff = Staff('Basic staff', 10, '', 0)

electricStaff = Staff('Electric staff', 12, 'electric', 2)

fireStaff = Staff('Fire staff', 12, 'fire', 2)

poisonStaff = Staff('Poison staff', 10, 'poison', 4)

iceStaff = Staff('Ice staff', 12, 'ice', 3)

# List of premade staffs
staffList = dict(basic=basicStaff, electric=electricStaff, fire=fireStaff, poison=poisonStaff, ice=iceStaff)
