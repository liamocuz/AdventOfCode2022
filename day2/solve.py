from enum import Enum, auto

class RPS(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

# Points
LOSS_POINTS = 0
DRAW_POINTS = 3
WIN_POINTS = 6

ROCK_POINT = 1
PAPER_POINT = 2
SCISSORS_POINT = 3

# Letters
OPPONENT_ROCK = 'A'
OPPONENT_PAPER = 'B'
OPPONENT_SCISSORS = 'C'

YOU_ROCK = 'X'
YOU_PAPER = 'Y'
YOU_SCISSORS = 'Z'

if __name__ == "__main__":

    points = {
        YOU_ROCK: 1,
        YOU_PAPER: 2,
        YOU_SCISSORS: 3
    }

    letters = {
        OPPONENT_ROCK: RPS.ROCK,
        YOU_ROCK: RPS.ROCK,
        OPPONENT_PAPER: RPS.PAPER,
        YOU_PAPER: RPS.PAPER,
        OPPONENT_SCISSORS: RPS.SCISSORS,
        YOU_SCISSORS: RPS.SCISSORS
    }

    win_responses = {
        OPPONENT_ROCK: YOU_PAPER,
        OPPONENT_PAPER: YOU_SCISSORS,
        OPPONENT_SCISSORS: YOU_ROCK
    }

    file = open("./input.txt", "r")
    lines = file.read().splitlines()

    # Part 1
    score = 0
    for line in lines:
        Opponent_Choice, Your_Choice = line.split(' ')
        # Get the points from choosing
        score += points[Your_Choice]

        # Draw
        if letters[Your_Choice] == letters[Opponent_Choice]:
            score += DRAW_POINTS
        # Win
        elif win_responses[Opponent_Choice] == Your_Choice:
            score += WIN_POINTS
        # Lose means no adding any points
        

    print(score)


    # Part 2
    LOSE_STRAT = 'X'
    DRAW_STRAT = 'Y'
    WIN_STRAT = 'Z'


    end_strat_points = {
        LOSE_STRAT: LOSS_POINTS,
        DRAW_STRAT: DRAW_POINTS,
        WIN_STRAT: WIN_POINTS
    }

    end_strat_reponses = {
        LOSE_STRAT: {
            OPPONENT_ROCK: YOU_SCISSORS,
            OPPONENT_PAPER: YOU_ROCK,
            OPPONENT_SCISSORS: YOU_PAPER
        },
        DRAW_STRAT: {
            OPPONENT_ROCK: YOU_ROCK,
            OPPONENT_PAPER: YOU_PAPER,
            OPPONENT_SCISSORS: YOU_SCISSORS
        },
        WIN_STRAT: win_responses
    }

    new_score = 0
    for line in lines:
        Opponent_Choice, Outcome = line.split(' ')
        # Get the points from choosing
        new_score += points[end_strat_reponses[Outcome][Opponent_Choice]]
        new_score += end_strat_points[Outcome]

    print(new_score)
