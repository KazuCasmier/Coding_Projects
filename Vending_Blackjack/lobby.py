from vending import VendingMachine
from blackjack import Blackjack

cash = 100
inventory = []

print('\nWelcome to the casino!\n')

while True:

    if cash <= 0:
        print("Wow... you're really broke, you should probably leave while you're ahead")
        quit()

    print(f'You have ${cash} would you like to:\n[0] Play Blackjack\n[1] Go to the vending machine\n[2] Leave\n')
    user_i = int(input('---> '))
    if user_i == 0:
        blackjack = Blackjack(cash)
        amount = blackjack.create_deck()
        cash = amount
    elif user_i == 1:
        if len(inventory) >= 1:
            for i in inventory:
                if i == '???':
                    mys = input('The mystery item you vended was the key to the machine! would you like to open it (y/n) ')
                    key = VendingMachine(cash, True)
                    if mys == 'y':
                        stock = key.get_stock
                    elif mys == 'n':
                        pass
        vending = VendingMachine(cash)
        update = vending.buy_item()
        inventory.append(update[0])
        cash = update[1]
    elif user_i == 2:
        print('Sayonara')
        break
