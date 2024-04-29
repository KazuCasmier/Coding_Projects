import itertools
import random


class Blackjack:

    def __init__(self, amount):
        self.amount = amount
        self.suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

    @staticmethod
    def player_math(p_hand, p_count):
        for i in range(0, len(p_hand)):
            if type(p_hand[i][0]) is int:
                p_count += p_hand[i][0]
            else:
                if p_hand[i][0] == 'Ace':
                    if p_count > 11:
                        p_count += 1
                    else:
                        p_count += 11
                else:
                    p_count += 10
        return p_count

    @staticmethod
    def dealer_math(d_hand, d_count):
        for d in range(0, len(d_hand)):
            if type(d_hand[d][0]) is int:
                d_count += d_hand[d][0]
            else:
                if d_hand[d][0] == 'Ace':
                    if d_count > 11:
                        d_count += 1
                    else:
                        d_count += 11
                else:
                    d_count += 10
        return d_count

    def create_deck(self):

        deck = list(itertools.product(self.cards, self.suits))
        random.shuffle(deck)
        p_hand = [deck.pop(), deck.pop()]
        d_hand = [deck.pop(), deck.pop()]
        p_count = 0
        d_count = 0
        p_count = Blackjack.player_math(p_hand, p_count)
        d_count = Blackjack.dealer_math(d_hand, d_count)

        new_card = 2
        bet = int(input('How much would you like to bet: '))

        print(f'''\nThe dealer begrudgingly deals you a hand.
\nYou receive the {p_hand[0][0]} of {p_hand[0][1]} and the {p_hand[1][0]} of {p_hand[1][1]}
\nThe dealer is showing a {d_hand[0][0]} of {d_hand[0][1]}''')

        while True:
            if d_count == 21:
                print(f'The dealer flips over the {d_hand[1][0]} of {d_hand[1][1]} and has blackjack you lose :(\n')
                self.amount -= bet
                input('press enter to continue\n')
                return self.amount

            print(f'\nYour current count is: {p_count} and dealer has a {d_hand[0][0]}')
            user_i = int(input('Would you like to:\n[0] Hit\n[1] Stand\n\n---> '))

            if user_i == 0:
                p_hand.append(deck.pop())
                p_count = 0
                print(f'''You drew the {p_hand[new_card][0]} of {p_hand[new_card][1]}
\nYour new count is {Blackjack.player_math(p_hand, p_count)}''')
                new_card += 1
                p_count = Blackjack.player_math(p_hand, p_count)
                if p_count > 21:
                    print("You busted!!! you lose :( ")
                    self.amount -= bet
                    print(f'you lost ${bet}\n')
                    input('press enter to continue\n')
                    return self.amount
            if user_i == 1:
                new_card = 2
                print(f"The dealer flipped over a {d_hand[1][0]} of {d_hand[1][1]} giving them a total of {d_count}")
                while d_count < 17:
                    d_count = 0
                    d_hand.append(deck.pop())
                    print(f'The dealer drew the {d_hand[new_card][0]} of {d_hand[new_card][1]}')
                    d_count += Blackjack.dealer_math(d_hand, d_count)
                    new_card += 1
                if d_count >= 17:
                    if d_count > 21:
                        print(f'The dealer busted you win ${bet}')
                        self.amount += bet
                        return self.amount
                    if d_count > p_count:
                        print(f'The dealer has a total of {d_count} compared to your measly {p_count}...\nYou lose!')
                        self.amount -= bet
                        return self.amount
                    if d_count == p_count:
                        print('You have the same value as the dealer you neither win nor lose :/')
                        return self.amount
                    if d_count < p_count:
                        print(f'You have the better hand beating out a total of {d_hand} with your {p_hand} you win!!')
                        self.amount += bet
                        return self.amount
