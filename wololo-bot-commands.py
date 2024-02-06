import typing
import os

from discord import app_commands
from discord.ext import commands
import discord

description = "DK_Wololo"
TOKEN = 'MTE0NjExMDE2MDcyNTYyMjg0NQ.Gz4VjC.-VMX53nHhI6deUQl5QjpT5vtQ-dn4bDn-bVRG4'


def log(message):
    print(message)


class WololoCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_ranking(self, ctx, arg1=None, arg2=None):
        log("Comando add_ranking")
        if isinstance(ctx.message.channel,
                      discord.channel.DMChannel) or ctx.message.author.id == 401762141906141184 or ctx.message.author.id == 292314272640401409 or ctx.message.author.id == 407631373369737217 or ctx.message.author.id == 618398991700459520:
            print("Granted!")


bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e)


@bot.tree.command(name="add_ranking", description="Añadir miembro al ranking")
@app_commands.describe(profile_id="Profile id de aoe2.net", name="Nombre", discord_id="ID de discord")
async def add_ranking(interaction: discord.Interaction, profile_id: typing.Optional[str], name: typing.Optional[str], discord_id: typing.Optional[str], steam_id: typing.Optional[str]):
    log("Comando add_ranking")
    if interaction.user.id == 474968187637596160 or interaction.user.id == 401762141906141184 or interaction.user.id == 292314272640401409 or interaction.user.id == 618398991700459520 or interaction.user.id == 465513130559012865 or interaction.user.id == 184444242440093696:
        await interaction.response.defer()
        if profile_id is not None and name is not None and discord_id is not None:
            with open(os.path.realpath(os.path.dirname(__file__)) + "/watched.txt", 'a') as f:
                f.write(profile_id + "&&&" + discord_id + "&&&" + name + "&&&" + str(
                    0) + "&&&" + str(0) + "&&&" + str(steam_id) + "\n")
                await interaction.followup.send("Añadido " + name + " al ranking.")
                print("Añadiddo " + name + " al ranking.")
        else:
            await interaction.followup.send("No tienes permisos!")

bot.run(TOKEN)