th import pi, e, log, sqrt
from pe.pefuncs import Memoize

#Your first test can be on Glickman's example. :) :) (Thanks Glickman!)

tau = 0.4 #Glicko paper recommends testing tau.

def new_player():
	return (1500, 350, 0.06)

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

#Currently, this probably doesn't handle new players well.
#Operates on "glickoized" ratings, rather than "outward-facing" ones.
def glicko_update(game_list, player_dict):
	player_variances = {player: 0 for player in player_dict}
	player_deltas = {player: 0 for player in player_dict}
	for game in game_list:
		game_weight = game[1] / (len(game[0])-1)
		for player1 in game[0]:
			for player2 in game[0]:
				if player1 != player2:
					E_val = E(player1[0], player2[0], player2[1])
					#Am I wrong to include the factor of game_weight in the summands of the variance?
					player_variances[player1] += game_weight * g(player2[1])**2 * E_val * (1-E_val)
					player_deltas[player] += game_weight * g(player2[1]) * (game[player1] / (game[player1] + game[player2]) - E_val)
	
	for player in player_variances:
		player_variances[player] = 1/player_variances[player]

	for player in player_deltas:
		player_deltas[player] *= player_variances[player]

	player_dict_new = {}

	for player in player_variances:
		#Using variance == 0 as a proxy for not having played games during this play period. Is this wrong?
		if player_variances[player] != 0:
			delta, v = player_deltas[player], player_variances[player], 
			mu, phi, sigma = player_dict[player]
			
			a = log(sigma**2)
			def f(x):
				return e**x*(delta**2 - phi**2 - v - e**x) / (2*(phi**2 + v + e**x)**2) - (x-a) / tau**2
			epsilon = 10**-6
			
			A = a
			B = 0
			if delta**2 > phi**2 + v:
				B = log(delta**2 - phi**2 - v)
			else:
				k = 1
				while f(a-k*tau) < 0:
					k += 1
				B = a - k*tau

			f_A, f_B = f(A), f(B)
			
			while abs(B-A) > epsilon:
				C = A + (A-B)*f_A/(f_B-f_A)
				f_C = f(C)
				if f_C*f_B < 0:
					A, f_A = B, f_B
				else:
					f_A = f_A / 2
				B, f_B = C, f_C
			
			sigma_prime = e**(A/2)

			phi_star = sqrt(phi**2 + sigma_prime**2)

			phi_prime = (phi_star**-2 + v*-1)**(-1/2)
			mu_prime = mu + phi_prime**2 / v * delta

			player_dict_new[player] = (mu_prime, phi_prime, sigma_prime)
		
		else:
			player_dict_new[player] = (player_dict[player][0], sqrt(player_dict[player][1]**2 + player_dict[player][2]**2), player_dict[player][2])

	return player_dict_new




