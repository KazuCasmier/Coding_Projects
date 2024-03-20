class VendingMachine:

    def __init__(self, amount, key=False):
        self.amount = amount
        self._stock = {'Potato Chip Bag': 5, 'Coca-Cola': 3, 'Granola Bar': 4, 'Bag of Candy': 3, '???': 1}
        self.prices = {0: 1, 1: 2, 2: 1, 3: 2, 4: 1000}
        self.key = key

    @property
    def get_stock(self):
        if self.key:
            print(self._stock)
            while True:
                user_i = input("Would you like to add items (y/n): ")

                if user_i == 'y':
                    item = input('What item would you like to add: ')
                    am = int(input('How many of that item would you like to add: '))
                    self._stock[item] = am
                    print(self._stock)

                elif user_i == 'n':
                    return f'Goodbye'

                else:
                    print('Not a valid input try again')
        else:
            return f'You do not have the key!!!'

    def buy_item(self):
        print(f'You waltz up to the vending machine with ${self.amount} in you hand.\n')
        while True:
            user_i = input('Would you like to purchase an item from the vending machine (y/n): ')
            if user_i == 'y':
                print(f'\nWhat would you like to purchase?\n')
                for i in range(0, len(self._stock)):
                    print(f'[{i}] {list(self._stock)[i]} ${self.prices[i]}')
                while True:
                    item = int(input('\n---> '))
                    if item in range(0, len(self._stock)):
                        print('Dispensing item...')
                        print(f'You have obtained one {list(self._stock)[item]}')
                        new_am = self.amount - self.prices[item]
                        print(f'You now have ${new_am}\n')
                        return list(self._stock)[item], new_am
                    else:
                        print('Invalid item try again')
            if user_i == 'n':
                print(f'\nYou leave the vending machine wondering why you even went there in the first place')
                return 'Cobweb'
