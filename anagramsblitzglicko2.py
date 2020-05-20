from math import pi, e
from pe.pefuncs import Memoize

#Given a player in the ("outward-facing") form ( (mu, phi, sigma) ) described in Step 1 of the Glicko-2 paper, computes their Glicko-2 ("under the hood") rating.
def glickoize(player):
	return ((player[0]-1500) / 173.7178, player[1] / 173.7178, player[2])

def g(phi):
	return (1 + 3 * phi**2 / pi**2) ^ (-1/2)

g = Memoize(g)

def E(mu, mu_j, phi_j):
	return (1 + e ** (-g(phi_j)(mu - mu_j)))

E = Memoize(E)

#game datatype: ({player: score}, number of bags)

def glicko_update(game_list, player_dict):
	player_variances = {player: 0 for player in player_dict}
	player_deltas = {player: 0 for player in player_dict}
	for game in game_list:
		game_weight = game[1] / (len(game[0])-1)
		for player1 in game[0]:
			for player2 in game[0]:
				if player1 != player2:
					E_val = E(player1[0], player2[0], player2[1])
					player_variances[player1] += g(player2[1])**2 * E_val * (1-E_val)
					player_deltas[player] += g(player2[1]) * (game[player1] / (game[player1] + game[player2]) - E_val)
	
	for player in player_variances:
		player_variances[player] = 1/player_variances[player]

	for player in player_deltas:
		player_deltas[player] *= player_variances[player]