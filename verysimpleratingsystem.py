from copy import deepcopy

#Players are of the form (name, rating, multiplier)
def new_player_rating():
	return (1200, 3)

#Sums the integers from a to b inclusive. Not needed in the current implementation.
def sum_ints(a, b):
	return (b-a) * (b-a+1) // 2

#game_result takes the form ({player_name: player_score}, #bags). player_dict takes the form {player_name: (player_rating, player_multiplier)}. This function assumes that all players in the game have already been initialized, i.e. they are already in player_dict. 
def rate_game(player_dict, game_result, mpr_reducer = 0.5):
	total_rating = sum([player_dict[player][0] for player in game_result[0]])
	total_score = sum([game_result[0][player] for player in game_result[0]])
	new_ratings = {}
	bags = game_result[1]
	while bags > 0:
		for player in game_result[0]:
			new_ratings[player] = (player_dict[player][0] + player_dict[player][1] * 100 * (game_result[0][player] / total_score - player_dict[player][0] / total_rating), max(1, player_dict[player][1] - mpr_reducer))
		for player in new_ratings:
			player_dict[player] = new_ratings[player]
		bags -= 1

def elo_winrate(r1, r2):
	return 1 / (1 + 10**((r1-r2)/400))

#K is the Elo "K value" (e.g. K = 20 for players who aren't rated too high in Scrabble. For simplicity, we are just using K = 20 for everyone at the moment)
def elo_rate_game(player_dict, game_result, K = 20, mpr_reducer = 0.25):
	old_ratings = {p: player_dict[p] for p in game_result[0]}
	new_ratings = {p: player_dict[p] for p in game_result[0]}
	bags = game_result[1]
	player_names = list(game_result[0])
	while bags > 0:
		for (p1ind, p1) in enumerate(player_names):
			for p2 in player_names[p1ind+1:]:
				total_score = game_result[0][p1] + game_result[0][p2]
				p1_dev_from_exp = game_result[0][p1] / total_score - elo_winrate(old_ratings[p1][0], old_ratings[p2][0])
				new_ratings[p1] = (new_ratings[p1][0] + p1_dev_from_exp * K * new_ratings[p1][1], new_ratings[p1][1])
				new_ratings[p2] = (new_ratings[p2][0] - p1_dev_from_exp * K * new_ratings[p2][1], new_ratings[p1][1])
				#print(old_ratings[p1], new_ratings[p1], old_ratings[p2], new_ratings[p2])
			new_ratings[p1] = (new_ratings[p1][0], max(1, new_ratings[p1][1] - mpr_reducer))
		old_ratings = deepcopy(new_ratings)
		bags -= 1
	for p in new_ratings:
		player_dict[p] = new_ratings[p]



