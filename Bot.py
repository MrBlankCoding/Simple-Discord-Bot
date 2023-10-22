
import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

COMMAND_PREFIX = '/'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

TOKEN = "Your Bot token"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{COMMAND_PREFIX}help'))

@bot.command()
async def ping(ctx):
    """Check if the bot is online."""
    await ctx.send('Pong')

@bot.command()
async def delete_messages(ctx, amount=5):
    """Delete your own messages in the current channel."""
    def is_user_msg(msg):
        return msg.author == ctx.author

    await ctx.message.delete()
    await ctx.channel.purge(limit=amount, check=is_user_msg)

@bot.command()
async def set_nickname(ctx, *, nickname):
    """Set your nickname on the server."""
    member = ctx.author
    await member.edit(nick=nickname)
    await ctx.send(f"Your nickname has been changed to {nickname}.")

@bot.command()
async def mute(ctx, member: discord.Member):
    """Mute a user in the voice channel."""
    channel = ctx.author.voice.channel
    if channel:
        await member.edit(mute=True)
        await ctx.send(f"{member.display_name} has been muted in {channel.name}.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    """Unmute a user in the voice channel."""
    channel = ctx.author.voice.channel
    if channel:
        await member.edit(mute=False)
        await ctx.send(f"{member.display_name} has been unmuted in {channel.name}.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def example_commands(ctx):
    """Provide examples of how to use all available commands."""
    examples = [
        "/ping - Check if the bot is online.",
        "/show_e_file - Display the contents of the 'e.txt' file.",
        "/server_info - Get information about the server.",
        "/welcome_message [message] - Set a welcome message for new members.",
        "/list_commands - List all available commands.",
        "/create_poll <question> <option1> <option2> ... - Create a poll with a question and multiple options.",
        "/delete_messages [amount] - Delete your own messages in the current channel.",
        "/set_nickname <nickname> - Set your nickname on the server.",
        "/mute <user_mention> - Mute a user in the voice channel.",
        "/unmute <user_mention> - Unmute a user in the voice channel.",
        "/say <message> - Make the bot say something.", 
    ]

    examples_text = "\n".join(examples)
    embed = discord.Embed(
        title="Example Commands",
        description=examples_text,
        color=0x3498db
    )

    await ctx.send(embed=embed)

@bot.command()
async def color_text(ctx, color, *, message):
    """Send a colored message using an embed."""
    color = color.lower()
    colors = {
        "red": discord.Color.red(),
        "green": discord.Color.green(),
        "blue": discord.Color.blue(),
        "yellow": discord.Color.gold(),
    }

    if color not in colors:
        await ctx.send("Unsupported color. Choose from: " + ", ".join(colors.keys()))
        return

    embed = discord.Embed(
        description=message,
        color=colors[color]
    )

    await ctx.send(embed=embed)

@bot.command()
async def formatted_text(ctx, *, message):
    """Send a message with bold, italics, and underlined text."""
    formatted_message = f"***__{message}__***"
    await ctx.send(formatted_message)

@bot.command()
async def show_e_file(ctx):
    """Display the contents of the 'e.txt' file."""
    filename = "e.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        await ctx.send(f"Here's what's in {filename}:\n```\n{file_contents}```")
    except FileNotFoundError:
        await ctx.send(f"{filename} not found.")
    except Exception as e:
        await ctx.send(f"Oops, something went wrong: {str(e)}")

@bot.command()
async def server_info(ctx):
    """Get information about the server."""
    server = ctx.guild
    owner = server.owner
    member_count = server.member_count

    embed = discord.Embed(
        title=f"Server Info - {server.name}",
        color=0x00ff00 
    )
    embed.add_field(name="Server Owner", value=owner, inline=True)
    embed.add_field(name="Total Members", value=member_count, inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def welcome_message(ctx, *, message="Welcome to the server!"):
    """Set a welcome message for new members."""
    await ctx.send(f"New members will see this message: {message}")

@bot.command()
async def list_commands(ctx):
    """List all available commands."""
    command_list = [command for command in bot.commands if not command.hidden]
    command_list.sort(key=lambda c: c.name)

    if not command_list:
        await ctx.send("No available commands.")
        return

    commands_text = "\n".join([f"/{cmd.name} - {cmd.help}" for cmd in command_list])
    embed = discord.Embed(
        title="Available Commands",
        description=commands_text,
        color=0x3498db
    )

    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, question, *options):
    if len(options) < 2 or len(options) > 10:
        await ctx.send('You must provide between 2 and 10 options for the poll.')
        return

    formatted_options = [f"{index + 1}. {option}" for index, option in enumerate(options)]
    poll_message = f"**{question}**\n\n" + "\n".join(formatted_options)
    poll = await ctx.send(poll_message)

    for i in range(len(options)):
        await poll.add_reaction(f"{i + 1}\N{COMBINING ENCLOSING KEYCAP}")



@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: /poll "Question" Option1 Option2 ...')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Invalid argument format. Usage: /poll "Question" Option1 Option2 ...')


@bot.command()
async def say(ctx, *, message):
    """Make the bot say something."""
    await ctx.send(message)  

  
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if "hehe" in content:
        await message.add_reaction("😂")
    elif "kewl" in content:
        await message.add_reaction("🆒")
    elif "bye" in content:
        await message.add_reaction("🏄‍♀️")
    elif "hello" in content:
        await message.add_reaction("👋")
    elif "awesome" in content:
        await message.add_reaction("🌟")
    elif "thanks" in content:
        await message.add_reaction("🙏")
    elif "oops" in content:
        await message.add_reaction("😅")
    elif "lol" in content:
        await message.add_reaction("😆")
    #elif "e" in content:
        #await message.delete()
        #await message.channel.send("e is not allowed")

    await bot.process_commands(message)






keep_alive()
bot.run(TOKEN)
