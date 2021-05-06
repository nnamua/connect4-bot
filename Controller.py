#!/usr/bin/env python3

import os, discord, sys, asyncio, Stats

from dotenv import load_dotenv
from discord.ext import commands
from game import Game, BotGame, RANDOM, MINIMAX, MINIMAX_AB
from stones import Stone, Red, Yellow, Empty

load_dotenv()
# Use DISCORD_TEST_TOKEN for testing!
token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="-")

numberEmojis = [ "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣" ]
loadingEmoji = "<a:3859_Loading:787421781182120006>"
games = []

@bot.event
async def on_ready():
    print(f"Bot online with id={bot.user.id}.")

"""
    Main function, is used to start a game of connect 4.
    Can be used in 3 main ways:
        '-start' will start a match, so that any user can join as an opponent
        '-start @User' will start a match where the mentioned user is the opponent
        '-start @ThisBot' starts a match against the computer
"""
@bot.command(name="start", help="Starts a game of connect 4.")
async def start(ctx):
    message  = ctx.message
    author   = message.author
    channel  = message.channel
    mentions = message.mentions

    # Check if there is 0 or 1 mention
    if len(mentions) > 1:
        await ctx.send(monospace("To start a game, type '-start'. To challenge someone, mention him: '-start @User'"))
        await ctx.send(monospace("If you want to play against an AI, mention the bot instead."))

    # If there are no mentions, any user can join as the opponent
    opponent = mentions[0] if len(mentions) == 1 else None
    if opponent != None and opponent.id == bot.user.id:
        game = BotGame(mode=MINIMAX_AB)
    else:
        game = Game()

    game.yellowPlayer = author
    game.redPlayer = opponent
    game.channel = channel
    games.append(game)

    await drawGame(game)

"""
    This function will be called everytime a user reacts
    to a message on the channel. Ignore the reaction if it
    doesn't belong to a current game or the emoji is invalid.
    Otherwise, check if the user matches the current player,
    and if yes, try to place the stone.
"""
@bot.event
async def on_reaction_add(reaction, user):
    # Ignore own reactions
    if user.id == bot.user.id:
        return

    message = reaction.message
    game    = getGame(message)
    num     = getInput(reaction)

    # Check if the reaction is valid and belongs to a valid game
    if game != None and num != -1:
        # Check if its the users turn, and if yes, place the stone
        if game.isUserTurn(user):
            game.place(num)
            await afterMove(game)

    if message.author.id == bot.user.id:
        await reaction.remove(user)

"""
    This function is called after every move.
    If there is a winner (or a draw), the finishedGame function will be called, and the final screen displayed.
    If the game is against the computer, and the computers turn, a move is calculated.
    Otherwise, the game will simply be drawn, to await new input.
    
"""
async def afterMove(game):
    if game.state.winner() != None:
        await drawWinScreen(game)
        finishedGame(game)

    elif game.state.isDraw():
        await drawRemisScreen(game)
        finishedGame(game)

    else:
        # Its the computers turn to place
        if isinstance(game, BotGame) and game.isRedTurn():
            await drawGame(game, botTurn=True)
            game.botPlace()
            await afterMove(game)
        else:
            await drawGame(game)

"""
    This function is called after a win/draw of any player.
    It removes the game from the games list, and stores the information for later stat retrieval.
"""
def finishedGame(game):
    if game in games:
        del games[games.index(game)]
        # TODO: Add stats here

"""
    Draws a winscreen, and removes all reactions.
"""
async def drawWinScreen(game):
    msg = "Player " + game.getWinner().mention + " has won! :tada: (" + game.getLoser().mention + " has lost ... )\n\n"
    msg += gameString(game)

    await game.message.edit(content=msg)
    await game.message.clear_reactions()

"""
    Draws a remis screen, and removes all reactions.
"""
async def drawRemisScreen(game):
    msg = "Draw between " + game.redPlayer.mention + " and " + game.yellowPlayer.mention + " :expressionless: !\n\n"
    msg += gameString(game)

    await game.message.edit(content=msg)
    await game.message.clear_reactions()

"""
    Draws the game. It will try to edit game.message,
    and if that doesn't exist, it will create a new message
    and assign it. 
"""
async def drawGame(game, botTurn=False):
    if botTurn:
        msg = "Waiting for the computer to place " + loadingEmoji + "\n\n"
    else:
        msg = "Waiting for " + game.currentPlayerString() + "'s ("
        if game.state.currentPlayer == Red:
            msg += ":red_circle:"
        else:
            msg += ":yellow_circle:"
        msg += ") move ...\n\n"
    msg += gameString(game)

    if game.message == None:
        message = await game.channel.send(msg)
        game.message = message
        for emoji in numberEmojis:
            await message.add_reaction(emoji)
    else:
        await game.message.edit(content=msg)

"""
    Returns a string representation of the game's board.
"""
def gameString(game):
    string = ""
    for y in range(game.height()):
        line = ""
        for x in range(game.width()):
            if game.state.board[x][y] == Red:
                line += ":red_circle:"
            elif game.state.board[x][y] == Yellow:
                line += ":yellow_circle:"
            else:
                line += ":white_circle:"
            line += " " * 7
        string += line + "\n"
    return string

"""
    Looks up the given message in the games list. Return the 
    respective game or None if not found.
"""
def getGame(message):
    for game in games:
        if message.id == game.message.id:
            return game
    return None

"""
    Converts the reaction emoji into a number that can be used
    as an action. Returns -1 if the emoji is invalid.
"""
def getInput(reaction):
    for i in range(len(numberEmojis)):
        if numberEmojis[i] == reaction.emoji:
            return i
    return -1

"""
    Converts the given string to monospace for sending
    as a discord text message by adding ``` pre- and suffixes.
"""
def monospace(string: str):
    return "```" + string + "```"

# Run the bot
bot.run(token)