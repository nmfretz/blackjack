import random
import os

def screen_clear():
  os.system('clear') # mac and linux
  os.system('cls') # windows

suits = ('♥', '♦', '♠', '♣')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
# Aces = 1 or 11 logic coded in def(hit) of Dealer class
values = {'Ace':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10}

# CLASSES

class Card():
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank
    self.value = values[self.rank]
  
  def __str__(self):
    return f'{self.rank} of {self.suit}'

class Deck():
  def __init__(self):
    self.all_cards = []

    for suit in suits:
      for rank in ranks:
        new_card = Card(suit, rank)
        self.all_cards.append(new_card)
  
  def shuffle_deck(self):
    random.shuffle(self.all_cards)

  def deal_a_card(self):
    return self.all_cards.pop()

class Dealer():
  def __init__(self):
    self.current_hand = []
    self.round_points = 0
    
  def new_round(self):
    self.current_hand = []
    self.round_points = 0

  def hit(self, new_card):
    self.current_hand.append(new_card)
    self.round_points = 0 # reset to 0 to count again with aces as 1
    for card in self.current_hand:
      self.round_points += card.value
   
    # logic for ace value
    aces = []
    for card in self.current_hand:
      if card.rank == 'Ace':
        aces.append(card)
        
    if len(aces) > 0:
      for ace in aces:
        if self.round_points + 10 <= 21:
          self.round_points += 10

  def __str__(self):
    string = ''
    for card in self.current_hand:
      string += f'[{card}] '
    return f'{string}'

class Player(Dealer):
# Seems a little weird to extend dealer since a player is not a dealer, but I wanted to practice inheritance for this project
  def __init__(self, name, money):
    Dealer.__init__(self)
    self.name = name
    self.money = money
    self.round_bet = 0
    # self.current_hand, self.round_points from Dealer()

  # def hit() and def __str__() from Dealer()

  def new_round(self):
    self.current_hand = []
    self.round_points = 0
    self.round_bet = 0 # new for Player, so rewrite entire method
        
  def win_round(self, bet_amount):
    self.money += bet_amount

  def lose_round(self, bet_amount):
    self.money -= bet_amount

# FUNCTIONS

def welcome_message():
  print('\nWelcome to the Blackjack table!')
  print('\nRead the rules here: https://www.blackjack.org/blackjack/how-to-play/')
  print('\nModifications to the rules are as follow:')
  print(' - No Insurance, Split, or Double Down')
  print(' - Dealer does not have to hit on a soft 17')
  print(" - No ties. Dealer must hit until their points are greater than the player's points")
  print(' - Player automatically wins with 21')
  print(' - Program automatically assigns a value of 1 or 11 to aces based on what gets player and dealer closest to 21')
  print(' - Bet payouts are 1:1')

  input('\nPress enter to continue...')
  screen_clear()

def create_player():
  player_name = input('\nWhat is your name? ')
  screen_clear()

  while True:
    try:
      starting_money = int(input(f'\nHow much money will you play with?: $'))
      break
    except:
      screen_clear()
      print('\nPlease enter a number.')

  screen_clear()
  print(f'\nGood luck, {player_name}. Make that ${starting_money} count!')
  input('\nPress enter to continue...')
  
  return Player(player_name, starting_money)

def game_over():
  print('\nYou are out of money. Thanks for playing.')

def set_player_bet(player):
  screen_clear()

  while True:
    try:
      bet_amount = int(input(f'\nYou have ${player.money}. How much will you bet this round? $'))
      if bet_amount > player.money:
        screen_clear()
        print('\nPlease bet a value <= to the amount of money you have.') 
      else:
        break
    except:
      screen_clear()
      print('\nPlease enter a valid number.') 

  return bet_amount

def deal_round_start(dealer, player, card_deck):
    for i in range(2):
      dealer.hit(card_deck.deal_a_card())

    for i in range(2):
      player.hit(card_deck.deal_a_card())

def display_round(round_count, dealer, player, is_dealer_turn):
  screen_clear()
  
  print(f'\nRound #{round_count}')
  print(f'Bet: ${player.round_bet}')
  print('-----------------------------')

  if is_dealer_turn:
    print(f'\n\nDealer Total: {dealer.round_points}')
    print(f'Dealer Cards: {dealer}')
  else:  
    print(f'\nDealer Cards: [{dealer.current_hand[0]}] [no peaking]') 

  print(f'\n\nPlayer Total: {player.round_points}')
  print(f'Player Cards: {player}')

def ask_player_next_move():
  answer = ''
  while answer.upper() != 'H' and answer.upper() != 'S':
    answer = input('\nHit or Stand (H/S): ')
  if answer.upper() == 'H':
    return True
  else:
    return False

def check_for_21(player):
  if player.round_points == 21:
    return True
  return False

def check_for_bust(player):
  if player.round_points > 21:
    return True
  return False

def ask_to_play_again():
  answer = ''
  while answer.upper() != 'Y' and answer.upper() != 'N':
    answer = input('Play another round? (Y/N) ')
  if answer.upper() == 'Y':
    return True
  else:
    return False

  
def play_blackjack():
# Main Game Logic
  welcome_message()
  player = create_player()
  dealer = Dealer()

  round_count = 1
  game_on = True

  while game_on:
    if player.money == 0:
      game_over()
      input('Press enter to exit game...')
      screen_clear()
      break

    card_deck = Deck()
    card_deck.shuffle_deck()
    dealer.new_round()
    player.new_round()
    
    hit = True
    is_bust = False
    is_21 = False

    player.round_bet = set_player_bet(player)
    deal_round_start(dealer, player, card_deck)
    display_round(round_count, dealer, player, False)
    
    is_21 = check_for_21(player)
    if is_21:
      player.win_round(player.round_bet)
      hit = False
      print('\nYou Win!')
      game_on = ask_to_play_again()
      if not game_on:
        input('\nThanks for playing! Press enter to exit game...')

    while hit:
      hit = ask_player_next_move()
      if hit:
        player.hit(card_deck.deal_a_card())
        display_round(round_count, dealer, player, False)
        is_21 = check_for_21(player)
        if is_21:
          player.win_round(player.round_bet)
          hit = False
          print('\nYou Win!')
          game_on = ask_to_play_again()
          if not game_on:
            input('\nThanks for playing! Press enter to exit game...')
        is_bust = check_for_bust(player)
        if is_bust:
          player.lose_round(player.round_bet)
          hit = False
          print('\nYou Busted :(')
          game_on = ask_to_play_again()
          if not game_on:
            input('\nThanks for playing! Press enter to exit game...')
            screen_clear()
      else:
        while dealer.round_points < 17:
          dealer.hit(card_deck.deal_a_card())
        display_round(round_count, dealer, player, True)
        if dealer.round_points > 21:
          print('\nYou Win!')
          player.win_round(player.round_bet)
        elif dealer.round_points > player.round_points:
          print('\nDealer Wins')
          player.lose_round(player.round_bet)
        elif dealer.round_points < player.round_points:
          print('\nYou Win!')
          player.win_round(player.round_bet)
        else:
          print("\nIt's a Tie!") # no money added or removed from player.money
        game_on = ask_to_play_again()
        if not game_on:
          input('\nThanks for playing! Press enter to exit game...')
          screen_clear()
    
    round_count += 1
  
if __name__ == '__main__': 
  play_blackjack()