import datetime
import time
import discord
import os
import sqlite3
from discord import app_commands
from typing import List
import json
from discord.ext import tasks


#### @-- Preload --@ ####
# Here we load the configuration and connect to the sql server.

debug = False

FailColor = 0xe60000
SuccessColor = 0x00e600
## @-- Config --@ ##
# Load the config from config.json.

path = 'config.json'

with open(path, "r") as jsonfile:
    data = json.load(jsonfile)  # Reading the file
    if debug != False:
        print("Read successful")
    jsonfile.close()

# - Variable Changing -
token = data["token"]

## Dont change shit ##
# This thing right here doesn't work cuz for now its not necessary.

## Discord Fancy stuff ##
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

## Just in case! ##
pfp = None
list_gen = []
categories = []
found = False

## SQLite3 thing ##

con = sqlite3.connect("Stock.db")
cur = con.cursor()

categories = set()
with sqlite3.connect("Stock.db") as con:
    cur = con.cursor()
    cur.execute("SELECT category FROM Stock")
    for row in cur:
        categories.add(row[0])

    query = "SELECT category, COUNT(data) FROM Stock GROUP BY category"
    cur.execute(query)
    for row in cur:
        categories.add(row[0])


print(categories)
## - - - - - - -  End Preload- - - - - - - - - - ##

# I'll only comment 'till here
# It's been an honour comrade.

#### @-- Main Script --@ ####


@client.event
async def on_ready():
    print("syncing !")
    await tree.sync()#guild=discord.Object(id=947887839511724093)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
    print("Ready!")


async def rps_autocomplete(ctx, current: str,) -> List[app_commands.Choice[str]]: # coolway for displaying gen categories
    category = categories
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in category if current.lower() in choice.lower()
    ]

@tree.command(name="stock", description="Gets you a list of all commands.")#, guild=discord.Object(id=947887839511724093))
async def stock(ctx):
    try:
        try:
            print(ctx.user)
            User = await client.fetch_user(ctx.user.id)
            pfp = User.avatar  # this will give the pfp
        except Exception as e:
            print("METHOD: 2 | Error: no pfp available | " + str(e))
            pfp = 'https://i.pinimg.com/474x/47/ba/71/47ba71f457434319819ac4a7cbd9988e.jpg' # error pfp

        embed = discord.Embed(title="**Stock:**", color=SuccessColor)
        embed.set_footer(
            text=ctx.user.name + "#" + ctx.user.discriminator + " • " + str(
                datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')),
            icon_url=pfp)
        query = "SELECT category, COUNT(data) FROM Stock GROUP BY category"
        for row in con.execute(query):
            embed.add_field(name=f"_{row[0]}_",
                            value=f"`Amount: {str(row[1])}`", inline=False)
        try:
            await ctx.response.send_message(embed=embed)
        except:
            try:
                await ctx.channel.send(embed=embed)
            except discord.errors.NotFound:
                # Handle the NotFound exception here
                print("Interaction not found")
            except discord.ext.commands.CommandInvokeError as error:
                if hasattr(error, 'original') and isinstance(error.original, discord.errors.NotFound):
                    # Handle the NotFound exception here
                    print("Interaction not found")
                    embed = discord.Embed(title="Error ", description="Something just went wrong right now. Try again in several minutes, if this error contains please open a ticket.", color=0xe60000)
    except Exception as e:
        print(e)
        embed = discord.Embed(title="Error ",
                              description="Something just went wrong right now. Try again in several minutes, if this error contains please open a ticket.",
                              color=0xe60000)
        embed.set_footer(
                        text=ctx.user.name + "#" + ctx.user.discriminator + " • " + str(
                            datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')),
                        icon_url=pfp)
        await ctx.response.send_message(embed=embed)

@tree.command(name="gen", description="Generates an account from a specific category.")    #guild=discord.Object(id=947887839511724093) # read the next iteration of this to see my comment, dont be lazy
@app_commands.autocomplete(category=rps_autocomplete)
#@app_commands.checks.cooldown(1, 300, key=lambda i: i.user.id) # cooldown system
async def gen(ctx, category: str):
    with open('whitelisted_channels.txt') as f:
        embed = discord.Embed(title="**Verifying**",
                                  description="_Checking if the channel is whitelisted:_ <a:Loading:1099353399880851526>", color=0xb3b3b3) # u should replace that emoji
        await ctx.response.send_message(embed=embed, delete_after=1)
        for line in f:
            time.sleep(2)
            if ctx.channel.id == int(line):
                try:
                    try:
                        print(ctx.user)
                        User = await client.fetch_user(ctx.user.id)
                        pfp = User.avatar  # Get that juicy pfp
                    except Exception as e:
                        print("METHOD: 2 | Error: no pfp available | " + str(e))
                        pfp = 'https://i.pinimg.com/474x/47/ba/71/47ba71f457434319819ac4a7cbd9988e.jpg'
                    print(list_gen)

                    embed = discord.Embed(title="**Account generated successfully!**",
                                          description="_Check your dm´s " + ctx.user.mention +
                                          ", if you did not received a message, please unlock your dm´s!_",
                                          color=SuccessColor)
                    embed.set_footer(
                        text=ctx.user.name + "#" + ctx.user.discriminator + " • " + str(
                            datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')),
                        icon_url=pfp)
                    await ctx.channel.send(embed=embed)
                    global found
                    found = True
                    import random
                    query = f"SELECT data FROM Stock WHERE category = '{category}'" # i swear this took a lot of time
                    result = cur.execute(query)
                    results = result.fetchone()
                    if results is not None:
                        # choose a random data from the results
                        found = True
                        random_data = ''.join(results)
                        cur.execute("DELETE FROM Stock WHERE data = ?", (random_data,))
                        con.commit()
                        print(
                            f"Random data from {category}: {random_data}")
                    else:
                        found = False
                        print(f"No data found for category: {category}")
                        await ctx.response.send_message("Couldn't find the category " + category + " !")
                        break
                    embed = discord.Embed(color=SuccessColor)
                    embed.add_field(
                        name="Service", value=f"```{category.capitalize()}```", inline=True)
                    embed.add_field(
                        name="Account", value=f"```{random_data}```", inline=True)
                    if found:
                        found = False
                    else:
                        await ctx.response.send_message("Couldn't find the category " + category + " !")
                        break
                    await ctx.user.send(embed=embed)
                    break

                except:
                    embed = discord.Embed(title="Error ",
                                          description="_Something just went wrong right now. Try again in several minutes, if this error contains please open a ticket._",
                                          color=FailColor)
                    embed.set_footer(
                        text=ctx.user.name + "#" + ctx.user.discriminator + " • " + str(
                            datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')),
                        icon_url=pfp)
                    await ctx.response.send_message(embed=embed)
                f.close()
                break
            else:
                embed = discord.Embed(
                    title="**Denied**", description="_Checking if the channel is whitelisted:_ ❌", color=0xe60000)
                await ctx.channel.send(embed=embed, delete_after=4)


@tree.command(name="help", description="Gets you a list of the stock.")#, guild=discord.Object(id=947887839511724093)) #Guild Lock in case of idk, Bot stealing?
async def help(ctx):
    try:
        try:
            print(ctx.user)
            User = await client.fetch_user(ctx.user.id)
            pfp = User.avatar  # Get that pfp
        except Exception as e:
            print("METHOD: 2 | Error: no pfp available | " + str(e))
            pfp = 'https://i.pinimg.com/474x/47/ba/71/47ba71f457434319819ac4a7cbd9988e.jpg'

        embed = discord.Embed(title="**Commands:**",
                              description="", color=SuccessColor)
        embed.add_field(
            name="", value="`/gen` _Generates a specified service if stocked._", inline=False)
        embed.add_field(
            name="", value="`/stock` _Displays the service stock._", inline=False)
        embed.add_field(
            name="", value="`/help` _Displays the currently available commands._", inline=False)
        embed.set_footer(
            text=ctx.user.name + "#" + ctx.user.discriminator + " • " + str(
                datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')),
            icon_url=pfp)
        await ctx.response.send_message(embed=embed)
    except:
        embed = discord.Embed(title="Error ",
                              description="_Something just went wrong right now. Try again in several minutes, if this error contains please open a ticket._",
                              color=0xe60000)
        embed.set_footer(
                        text=ctx.user.name + "#" + ctx.user.discriminator + " • " + str(
                            datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')),
                        icon_url=pfp)
        await ctx.response.send_message(embed=embed)


@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):

    embed = discord.Embed(title="Error", description="", color=0xe60000)
    embed.add_field(name="",
                    value=f"_If you think this is an error: Please, contact support._ `Error code: 401`",
                    inline=False)
    embed.set_footer(
        text=interaction.user.name + "#" + interaction.user.discriminator + " • " + str(
            datetime.datetime.utcnow().strftime('%d.%m.%Y at %H:%M')))
    await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(token)
## - - - - - - -  End Main script- - - - - - - - - - ##


