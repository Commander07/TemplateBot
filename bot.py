import os

from dotenv import load_dotenv
from guilded.ext import commands

from jsonfile import jsonfile

load_dotenv()
bot = commands.Bot(command_prefix="!")
# Init database
db = jsonfile.jsonfile("data.json")
# If 'data.json' does not exist create it and set it to default
if db.data == Ellipsis:
    db.data = {"version": "v1.0.0", "guilds": {}}


async def ensure_guild(guild_id):
    if guild_id not in db.data["guilds"]:
        db.data["guilds"][guild_id] = {"users": {}}


async def ensure_user(guild_id, user_id):
    await ensure_guild(guild_id)
    if user_id not in db.data["guilds"][guild_id]:
        db.data["guilds"][guild_id]["users"][user_id] = {}


async def is_mod(ctx):
    if ctx.guild.id not in db.data["guilds"]:
        return False
    elif set(ctx.author._role_ids).intersection(
        set(db.data["guild"][ctx.guild.id]["mod_roles"])
    ):
        return True
    elif ctx.author.is_owner():
        return True
    return False


@bot.event
async def on_ready():
    print(f"Succesfully connected to guilded i am {bot.user.name}!")


@bot.command(name="setmodrole")
async def set_mod_role(ctx, roles: str):
    if not ctx.author.is_owner():
        await ctx.send("ERROR: Missing permissions!")
        return
    roles = ctx.message._mentions._roles
    mod_roles = [role["id"] for role in roles]
    # Make sure we have a guild object
    await ensure_guild(ctx.guild.id)
    db.data["guilds"][ctx.guild.id]["mod_roles"] = mod_roles
    await ctx.send("Succesfully set mod roles")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR: Missing required argument!")


# retrive 'token' from '.env' file created by the setup script
bot.run(os.getenv("token"))
