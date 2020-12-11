import os, json

def _get_dict(filename="stats.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except Exception as e:
        return dict()

def _save_dict(stats, filename="stats.json"):
    try:
        with open(filename, "w") as file:
            json.dump(stats, file, indent=4)
    except:
        if not os.path.isfile(filename):
            with open(filename, "w+") as file:
                json.dump(stats, file, indent=4)

def _format_stats(user, stats):
    string =  "Stats for player: *" + user.name + "*\n"
    string += "```\n"
    string += "| Wins | Losses | Win-Ratio | Avg. Turns |\n"
    string += "+------+--------+-----------+------------+\n"

    # Add values
    matches = stats["matches"]
    wins = 0
    losses = 0
    turns = []
    for match in matches:
        if match["win"]:
            wins += 1
        else:
            losses += 1
        turns.append(match["turns"])

    avg_turns = round(sum(turns) / len(turns))
    win_rate = round((wins / len(matches)) * 100)

    string += "| " + str(wins) + " " * (5 - len(str(wins)))
    string += "| " + str(losses) + " " * (7 - len(str(losses)))
    string += "| " + str(win_rate) + "%" + " " * (9 - len(str(win_rate)))
    string += "| " + str(avg_turns) + " " * (11 - len(str(avg_turns))) + "|\n"

    string += "```\n"
    return string

def get_stats(user):
    stats = _get_dict()
    if str(user.id) not in stats:
        return "No stats found for User '*" + user.name + "*'.\n"
    else:
        return _format_stats(user, stats[str(user.id)])

def add_match(player1, player2, winner, turns):
    if player1.id == player2.id:
        return

    # Create match statistics
    player1_match = { "win"      : player1.id == winner.id,
                      "turns"    : turns,
                      "opponent" : f"#{player2.id}" }

    player2_match = { "win"      : player2.id == winner.id,
                      "turns"    : turns,
                      "opponent" : f"#{player1.id}" }

    # Add to json file
    stats = _get_dict()
    if str(player1.id) not in stats:
        stats = add_user(player1, stats)
    if str(player2.id) not in stats:
        stats = add_user(player2, stats)

    stats[str(player1.id)]["matches"].append(player1_match)
    stats[str(player2.id)]["matches"].append(player2_match)

    _save_dict(stats)


def add_user(user, stats):
    new_user = { "matches" : [] }
    stats[str(user.id)] = new_user
    return stats

class Player():
    def __init__(self, id):
        self.id = id