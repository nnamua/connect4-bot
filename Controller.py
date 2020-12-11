#!/usr/bin/env python3

import os, discord, sys, asyncio, Stats

from dotenv import load_dotenv
from discord.ext import commands
from Game import Game

load_dotenv()
# Use DISCORD_TEST_TOKEN for testing!
token = os.getenv("DISCORD_TEST_TOKEN")

bot = commands.Bot(command_prefix="-")

number_emojis = [ "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣" ]
games = []

@bot.event
async def on_ready():
    print(f"Bot online with id={bot.user.id}.")

@bot.command(name="start", help="Starts a game of connect 4.")
async def start(ctx):
    msg = ctx.message
    author = msg.author
    channel = msg.channel
    mentions = msg.mentions
    if len(mentions) > 1:
        await ctx.send("```To start a game, type '-start'. To challenge someone, mention him: '-start @User'")
        return

    game = Game()
    game.yellow_player = author
    if len(mentions) == 1:
        game.red_player = mentions[0]
    game.channel = channel
    games.append(game)

    await draw_game(game)

@bot.command(name="stats", help="Retrieves stats for given user(s).")
async def stats(ctx):
    mentions = ctx.message.mentions
    if len(mentions) < 1:
        await ctx.send("```Please mention at least one user: '-stats @User1'```")
        return

    for mention in mentions:
        await ctx.send(Stats.get_stats(mention))

@bot.event
async def on_reaction_add(reaction, user):
    # Ignore own reactions
    if user.id == bot.user.id:
        return

    message = reaction.message
    game = get_game(message)
    num = get_input(reaction)
    # Check if reaction is valid and belongs to a valid game
    if game != None and num != -1:
        # Check if its the users turn, and if yes, place the stone
        if game.is_user_turn(user):
            game.place(num)
            if game.check_win():
                await draw_winscreen(game)
                try:
                    del games[games.index(game)]
                    Stats.add_match(game.red_player, game.yellow_player, game.get_winner(), game.turns)
                except:
                    pass
            elif game.check_draw():
                await draw_remisscreen(game)
                try:
                    del games[games.index(game)]
                    Stats.add_match(game.red_player, game.yellow_player, None, game.turns)
                except:
                    pass
            else:
                await draw_game(game)
        
    if message.author.id == bot.user.id:
        await reaction.remove(user)

async def draw_winscreen(game):
    msg = "Player " + game.get_winner().mention + " has won! :tada: (" + game.get_loser().mention + " has lost ... )\n\n"
    msg += game_string(game)

    await game.message.edit(content=msg)
    await game.message.clear_reactions()

async def draw_remisscreen(game):
    msg = "Draw between " + game.red_player.mention + " and " + game.yellow_player.mention + " :expressionless: !\n\n"
    msg += game_string(game)

    await game.message.edit(content=msg)
    await game.message.clear_reactions()

async def draw_game(game):
    msg = "Waiting for " + game.get_player() + "'s ("
    if game.is_red_turn():
        msg += ":red_circle:"
    else:
        msg += ":yellow_circle:"
    msg += ")move ...\n\n"
    msg += game_string(game)

    if game.message == None:
        message = await game.channel.send(msg)
        game.message = message
        for emoji in number_emojis:
            await message.add_reaction(emoji)
    else:
        await game.message.edit(content=msg)


def game_string(game):
    string = ""
    for y in range(game.height):
        line = ""
        for x in range(game.width):
            if game.is_red(x,y):
                line += ":red_circle:"
            elif game.is_yellow(x,y):
                line += ":yellow_circle:"
            else:
                line += ":white_circle:"
            line += " " * 7
        string += line + "\n"
    return string


def get_game(message):
    for game in games:
        if message.id == game.message.id:
            return game
    return None

def get_input(reaction):
    for i in range(len(number_emojis)):
        if number_emojis[i] == reaction.emoji:
            return i
    return -1


bot.run(token)

