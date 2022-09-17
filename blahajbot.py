# Import packages
import os
import random
import signal
import discord
import requests
from config import config
from discord.ext import commands, tasks

# SIGINT handler
def signal_handler(signal, frame):
	# Log out the bot
	print("\nStopping Blahajbot")
	client.logout()
	client.close()

	# Save the comms variable
	with open("comms.txt", "w") as f:
		f.write(str(comms))

	# Exit
	exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Function to get the current amount of messages sent
def get_comms():
	# Create the file if it doesn't exist
	if not os.path.exists("comms.txt"):
		with open("comms.txt", "w") as f:
			f.write("0")

	# Get the amount of messages sent
	with open("comms.txt", "r+") as f:
		comms = f.read()
		if not comms:
			comms = 0
		else:
			comms = int(comms)

	# Return the amount of messages sent
	return comms

# Initialise variables
comms = get_comms()
Blahajfoto = os.path.join(os.getcwd(), "Blahaphotos")

# Initialise bot
client = commands.Bot(command_prefix=config["prefix"])
client.remove_command("help")


@client.event
async def on_ready():
	print("Started Blahajbot")


@client.command()
async def blahaj(ctx):
	filenames = os.listdir(Blahajfoto)
	selected_file = os.path.join(Blahajfoto, random.choice(filenames))
	embed = discord.Embed(title="Blåhaj!", description="Here is your Blåhaj", color=0x5866ef)
	embed.set_image(url="attachment://blahaj.png")
	await ctx.send(file=discord.File(selected_file, "blahaj.png"), embed=embed)




@client.command()
async def quote(ctx):
	global comms
	await ctx.send(random.choice(requests.get("https://raw.githubusercontent.com/PoggerCat/ignore/main/uselessquotes").text.split("\n")))

@client.command()
async def compliment(ctx):
	await ctx.send(random.choice(requests.get("https://raw.githubusercontent.com/PoggerCat/ignore/main/Compliments").text.split("\n")))



@client.command()
async def help(ctx):
	embed = discord.Embed(title="Help", colour=0x5866ef)

	embed.add_field(name="blahaj", value="Sends a random photo of Blåhaj")
	embed.add_field(name="quote", value="Makes Blåhaj pick a random useless quote from a list")
	embed.add_field(name="uses", value="Shows how many commands have been used in total!")
	embed.add_field(name="cheese", value="Send a random photo of cheese (I hate you hoiboi)")
	embed.add_field(name="compliment", value="says a random compliment")
	embed.add_field(name="invlink", value="sends the inv link")
	await ctx.send(embed=embed)




@client.command()
async def uses(ctx):
	global comms
	await ctx.send(f"{comms} commands have been used!")
	await ctx.send(f"I'm in {len(client.guilds)} servers!")




@client.command()
async def invlink(ctx):
	await ctx.send(config["invlink"])


@client.command()
async def cheese(ctx):
	global comms
	comms += 1
	r = requests.get("https://cheesepics.xyz/api")
	if (r.status_code == 200):
		cheese_id = r.json()["ID"]
		cheese_author = r.json()["author"]
		cheese_license = r.json()["license"]
		cheese_embed = discord.Embed(
		title="Cheese ", color=discord.Color.gold())
		cheese_embed.set_image(url=f"https://cheesepics.xyz/images/cheese/{cheese_id}")
		cheese_embed.set_footer(text=f"The person that made it was: {cheese_author}, Licenced by: {cheese_license}")
		await ctx.send(embed=cheese_embed)
	else:
		await ctx.send("Failed to load")

@client.event
async def on_command_completion(ctx):
	global comms
	comms += 1

@tasks.loop(minutes=10)
async def save_comms():
 	# Save the comms variable
 	with open("comms.txt", "w") as f:
 		f.write(str(comms))

# Start the bot
client.run(config["token"])