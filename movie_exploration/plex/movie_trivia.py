from random import randint
from plexapi.myplex import MyPlexAccount
from collections import Counter 
import string

# For string comparison
def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')
 
    return s.lower().strip()

print('Connecting to Plex server...')

# Credentials
account = MyPlexAccount('yadingus', 'N7PJgLYhg')
plex = account.resource('spergmaster').connect()

# Get movies from Plex server
movies = plex.library.section('Movies').search()
num = len(movies)

print('Connected successfully.')

def print_scores(scores, num):
	for result in scores.most_common(num):
		print(result[0], ':', result[1])

def trivia_question():
    
    # Randomly select film
    film_id = randint(0, num-1)
    title = movies[film_id].title
    
    # Display summary
    print(movies[film_id].summary)
    
    # Get guess and compare
    guess = input("What's the film?\n")
    
    # Render a verdict
    correct = normalize(guess) == normalize(title)
    if correct:
    	print('Correct!\n')
    	return True
    else:
    	print('Incorrect. The answer is %s\n' % title)
    	return False

# Main loop
def main():
	round = 1
	playercount = input('How many players?\n')
	num = int(playercount)
	names = []
	scores = Counter()

	for player in range(int(playercount)):
		name = input('Player %d name?\n' % (player + 1))
		names.append(name)

	while True:
		
		print('Round %i.\n' % round)

		for player in names:
			print(player, ':\n')
			if trivia_question():
				scores[player] += 1
		
		query = input("Continue? ('s' for scoreboard)\n")
		if query == 'n':
			print('\n\nFinal Scores:')
			print_scores(scores, num)
			
			break
		elif query == 's':
			print('\nCurrent Scores:')
			print_scores(scores, num)

		round += 1

if __name__ == '__main__':
	main()