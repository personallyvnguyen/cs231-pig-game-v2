# pig.py
#
# A231 Python 2 Spring 2021
# Credit: 
#  - Cabrera, James
#  - Nguyen, Van 
# In-class activity: Game of Pig Version 2


import random   
import sys



class Pig():
    '''
    Runs a command line game of pig for two players.
    Players take turns choosing to pass or roll. 
    Rolls have a weighted chance of getting different results.
    The game ends if a player wins by hitting the target score or 
    loses by rolling a "piggyback".
    '''

    _BORDER = '.' * 20


    # Weights chosen semi-arbitrarily. The pigs will be most likely be
    # touching, sometimes touch, and very rarely piggyback.
    #
    # * Index 0: Not Touching
    # * Index 1: Oinker - Reset to 0
    # * Index 2: Piggyback - Instant Lose
    _TOUCH_WEIGHTS = (80, 19, 1)


    # Weights chosen by adding 13 to each singles' score. As a result,
    # the converted scores add up to 100. Single/Double points.
    #
    # * Index 0: Sider - 0/1 pts
    # * Index 1: Razorback - 5/20 pts
    # * Index 2: Trotter - 5/20 pts
    # * Index 3: Snouter - 10/40 pts
    # * Index 4: Leaning Jowler - 15/60 pts
    _ROLL_WEIGHTS = (13, 18, 18, 23, 28)


    _ROLL_TYPES = (
        ('Sider', 0, 1),
        ('Razorback', 5, 20),
        ('Trotter', 5, 20),
        ('Snouter', 10, 40),
        ('Leaning Jowler', 15, 60),
    )


    def __init__(self, player_1: str, player_2: str, win_score: int) -> None:
        'Initiates class attributes.'

        self._players = [
            {
                'name': player_1,
                'score': 0,
            },
            {
                'name': player_2,
                'score': 0,
            },
        ]
        self._win_score = int(win_score)

        self._game_active = True
        self._turn_state = 0
        

    def execute(self) -> None:
        'Runs the code to start the game.'

        self._start_game()


    def _start_game(self) -> None: 
        'Starts the game. Endlessly loops until the game ends.'

        print(f'Competitors: {self._players[0]["name"]}' 
              f' vs {self._players[1]["name"]}')
        self._print_score()
        
        while self._game_active:
            self._start_turn()

        self._end_game()


    def _start_turn(self) -> None:
        'Starts a turn. Endlessly loops until the turn ends.'

        turn_active = True

        while turn_active:
            print(f'Your turn, {self._players[self._turn_state]["name"]}\n')

            turn_choice = input(INDENT + 'ROLL, PASS, or YOLO? ').lower()
            
            if turn_choice == 'roll':
                turn_active = self._roll_choice()
            elif turn_choice == 'pass':
                turn_active = self._pass_choice()
            elif turn_choice == 'yolo':
                turn_active = self._yolo_choice()

            self._print_score()

    
    def _roll_choice(self) -> bool:
        '''
        Executes the logic for a roll and updates the player score
        accordingly. Returns a bool value whether or not the turn is
        still active.
        '''

        touch_result = random.choices(range(3), weights=Pig._TOUCH_WEIGHTS)[0]

        if touch_result == 0:
            # Not Touching Roll
            roll_1 = self._individual_roll()
            roll_2 = self._individual_roll()

            pointsEarned = 0           

            if roll_1 == roll_2:
                pointsEarned += Pig._ROLL_TYPES[roll_1][2]
                print_indented('You rolled a Double ' 
                    f'{Pig._ROLL_TYPES[roll_1][0]}')

            else:
                pointsEarned += (Pig._ROLL_TYPES[roll_1][1] 
                               + Pig._ROLL_TYPES[roll_2][1])   
                print_indented('You rolled a Mixed Combo: '
                    f'{Pig._ROLL_TYPES[roll_1][0]} and '
                    f'{Pig._ROLL_TYPES[roll_2][0]}')

            self._players[self._turn_state]['score'] += pointsEarned
            print_indented(f'You earned {pointsEarned} points')
            
            return True

        elif touch_result == 1:
            # Oinker Roll
            self._players[self._turn_state]['score'] = 0

            print_indented('You rolled an Oinker!')
            print_indented('You lose all your points')

            self._next_player()
            return False

        elif touch_result == 2:
            # Piggyback Roll
            self._players[self._turn_state]['score'] = 'LOST'

            print_indented('You rolled a Piggyback!')
            print_indented('You are out of the game')

            self._next_player()
            return False

    
    def _pass_choice(self) -> bool:
        '''
        Executes the logic for a pass. Checks whether or not if the
        current player has won. Always returns a bool value of False
        indicating that the turn is no longer active.
        '''

        if (self._players[self._turn_state]['score'] >= self._win_score):
            self._game_active = False
        else:
            self._next_player()
        
        return False


    def _yolo_choice(self) -> bool:
        '''
        Executes the logic for a YOLO. The player gets a 50/50 chance
        of getting exactly the amount of points they need to win or
        getting kicked out of the game.
        '''

        yolo_result = random.choices(range(2), weights=(50, 50))[0]

        if yolo_result == 0:
            self._players[self._turn_state]['score'] = self._win_score
            print_indented(
                f'Your YOLO paid off! You now have {self._win_score} points')
                
            return True
        else:
            self._players[self._turn_state]['score'] = 'LOST'
            print_indented(
                f'Your YOLO failed! You are out of the game')

            self._next_player()
            return False
        

    def _end_game(self) -> None:
        'Prints the end score and the winner of the game.'

        print('GAME OVER')
        
        winner_exists = False

        for player in self._players:
            if player['score'] == 'LOST':
                continue
            elif player['score'] >= self._win_score:
                winner_exists = True
                print(f'{player["name"]} wins with {player["score"]} out of '
                      f'{self._win_score} points required to win!')
                break
        
        if not winner_exists:
            print('No one wins.')


    def _print_score(self) -> None:
        'Prints the score of the players.'

        print('\n' + Pig._BORDER)
        print(f'{self._players[0]["name"]}: {self._players[0]["score"]}, '
              f'{self._players[1]["name"]}: {self._players[1]["score"]}')
        print(Pig._BORDER + '\n')


    def _individual_roll(self) -> int:
        '''
        Randomly chooses a value from 0 - 4 based on the defined
        weights.
        '''

        return random.choices(range(5), weights=Pig._ROLL_WEIGHTS)[0]

    
    def _next_player(self) -> None:
        '''
        Flips the _turn_state from 0 to 1 and vice-versa.
        If both players have lost, it ends the game.
        '''

        if (self._players[0]['score'] == 'LOST' and 
            self._players[1]['score'] == 'LOST'):
            self._game_active = False
        elif self._players[0]['score'] == 'LOST':
            self._turn_state = 1
        elif self._players[1]['score'] == 'LOST':
            self._turn_state = 0
        else:
            self._turn_state = 1 if self._turn_state == 0 else 0



INDENT = ' ' * 5



def print_indented(text: str) -> None:
    'Adds an indentation before printing the text.'

    print(INDENT + text)



if __name__ == '__main__':
    Pig(sys.argv[1], sys.argv[2], sys.argv[3]).execute()

