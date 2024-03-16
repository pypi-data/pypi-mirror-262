class Human:
    def __init__(self, name) -> None:
        self.name = name
        self.coins = []

    def add_coin(self, coin):
        self.coins.append(coin)

    def remove_coin(self, coin):
        if coin in self.coins:
            self.coins.remove(coin)
        else:
            print(f"{self.name} does not own {coin}.")

    def display_coins(self):
        if self.coins:
            print(f"{self.name}'s coins: {', '.join(self.coins)}")
        else:
            print(f"{self.name} does not own any coins.")