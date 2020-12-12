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
    id_string = f"#{user.id}"
    wins = 0
    losses = 0
    turns = []
    for match in matches:
        if id_string == match["winner"]:
            wins += 1
        elif match["winner"] != "":
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

def add_match(game):
    if game.red_player.id == game.yellow_player.id:
        return

    # Create match statistics
    match_stats = game.to_dict()

    # Add to json file
    stats = _get_dict()
    if str(game.red_player.id) not in stats:
        stats = add_user(game.red_player, stats)
    if str(game.yellow_player.id) not in stats:
        stats = add_user(game.yellow_player, stats)

    stats[str(game.red_player.id)]["matches"].append(match_stats)
    stats[str(game.yellow_player.id)]["matches"].append(match_stats)

    _save_dict(stats)


def add_user(user, stats):
    new_user = { "matches" : [] }
    stats[str(user.id)] = new_user
    return stats
