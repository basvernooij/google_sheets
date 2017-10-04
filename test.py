class Fish():
    def __init__(self, swimming_speed=10, size=1):
        self.swimming_speed = swimming_speed
        self.size = size

    def can_eat_other_fish(self, other_fish):
        return True if self.size > other_fish.size and self.swimming_speed > other_fish.swimming_speed else False


salmon = Fish(swimming_speed=9, size=10)
tuna = Fish(swimming_speed=7, size=7)

print(salmon)


class LookUpError():
    pass