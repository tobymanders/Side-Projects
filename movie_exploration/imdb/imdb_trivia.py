from os import system
import requests
from collections import Counter
from random import randint
import string
import csv

cutoff = 1960

def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')

    return s.lower().strip()


# Extract film names from csv file and prepare for API calls.
movie_names = []
og_movie_names = []
with open('movies.csv', encoding = "ISO-8859-1") as csv_file:
    for row in csv_file:
        movie_raw = row[:-8]
        movie_name = movie_raw.replace(" ", "+")
        movie_names.append(movie_name)
        og_movie_names.append(movie_raw)


def print_scores(scores, num):
    for result in scores.most_common(num):
        print(result[0], ':', result[1])

def get_answer(og_movie_name):
    # Get guess and compare
    guess = input("What's the film?\n")

    # Render a verdict
    correct = normalize(guess) == normalize(og_movie_name)

    if correct:
        return True
    else:
        return False

def trivia_question(used, names, playercount, scores, player):
    num = len(movie_names)

    # Randomly select film
    while True:
        film_id = randint(0, num - 1)
        if film_id not in used:
            movie_name = movie_names[film_id]
            og_movie_name = og_movie_names[film_id]
            # Make the API call
            url = ('http://www.omdbapi.com/?apikey=a6a6cd3d&t=' + movie_name)
            r = requests.get(url)
            movie_dicts = r.json()
            used.append(film_id)
            # Reselect if film is older than cutoff year
            if int(movie_dicts['Year']) > cutoff:
                break

    # Display summary
    summary = movie_dicts['Plot']
    year = movie_dicts['Year']
    director = movie_dicts['Director']
    actors = movie_dicts['Actors']
    clean_name = og_movie_name.replace('the', '')
    edited_summary = summary.replace(clean_name, "____")
    print(edited_summary)

    correct = get_answer(og_movie_name)

    if correct:
        print('Correct!')
        print("%s (%s), directed by %s, starring %s\n" % (og_movie_name, year, director, actors))
        scores[player] += 1
        return True
    else:
        print("Incorrect.")
        if playercount > 1:
            reattempt = input('Does another player want a try? (y/n)\n')
            if reattempt == 'y':
                if playercount > 2:
                    while True:
                        who = input('Who?')
                        if who not in scores:
                            print('Player not recognized. Try again.')
                        break
                # 2 players
                else:
                    player_index = names.index(player)
                    who = (player_index + 1) % 2
                print(names[who],':\n')
                correct = get_answer(og_movie_name)
                if correct:
                    print('Correct!')
                    scores[who] += 1
                else:
                    print('Incorrect.')
                    scores[who] -= 1
                print("%s (%s), directed by %s, starring %s\n" % (og_movie_name, year, director, actors))
            else:
                print("%s (%s), directed by %s, starring %s\n" % (og_movie_name, year, director, actors))

# Main loop
def main():
    used = []
    round = 1
    playercount = input('How many players?\n')
    num = int(playercount)
    names = []
    scores = Counter()

    for player in range(int(playercount)):
        name = input('Player %d name?\n' % (player + 1))
        names.append(name)

    while True:
        system('clear')
        print('Round %i.\n' % round)
        for player in names:
            print(player, ':\n')
            trivia_question(used, names, num, scores, player)

        while True:
            query = input("Continue? (y/n) ('s' for scoreboard)\n")
            if query == 'n':
                print('\n\nFinal Scores:')
                print_scores(scores, num)
                return 0
            elif query == 's':
                print('\nCurrent Scores:')
                print_scores(scores, num)
            elif query == 'y':
                round += 1
                break


if __name__ == '__main__':
    main()
