#Players are of the form (name, rating, multiplier)
def new_player_rating(name):
	return (1200, 10)

#Sums the integers from a to b inclusive. Not needed in the current implementation.
def sum_ints(a, b):
	return (b-a) * (b-a+1) // 2

#game_result takes the form ({player_name: player_score}, #bags). player_dict takes the form {player_name: (player_rating, player_multiplier)}. This function assumes that all players in the game have already been initialized, i.e. they are already in player_dict. 
def rate_game(player_dict, game_result):
	total_rating = sum([player_dict[player][0] for player in game_result[0]])
	total_score = sum([game_result[0][player] for player in game_result[0]])
	new_ratings = {}
	bags = game_result[1]
	while bags > 0:
		for player in game_result[0]:
			new_ratings[player] = (player_dict[player][1] * 100 * (game_result[0][player] / total_score - player_dict[player][0] / total_rating), max(1, player_dict[player][1] - 1))
		for player in new_ratings:
			player_dict[player] = new_ratings[player]
		bags -= 1
