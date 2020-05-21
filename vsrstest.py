from verysimpleratingsystem import new_player_rating, rate_game, elo_rate_game

player_dict = {player: new_player_rating() for player in ["a","b","c","d","e","f"]}
game_result = ({"a": 2/3, "b": 1/6, "c": 1/12, "d": 1/24, "e": 1/24, "f": 0} , 8)
print(player_dict)
elo_rate_game(player_dict, game_result)
print(player_dict)
