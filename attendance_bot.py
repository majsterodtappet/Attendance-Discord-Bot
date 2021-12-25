import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Mark your Attendance!'))
    print("bot is ONLINE")

@client.command()
async def attendance(message):

        await message.message.delete()

        embed = discord.Embed(
            description = f'New attendance list. **Mark your presence!**\n‎',
            color = 0xffffff)

        embed.set_author(name=datetime.now().strftime('MEETING %d.%m.%Y'))
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/706796095719866469/924434268552314900/attendanceM.png')

        embed.add_field(name='✅  PRESENT', value=f'React below to mark your presence!')
        embed.add_field(name='⛔  CLOSE THE LIST', value=f'Only authorized user closes the list.')

        msg = await message.channel.send(embed=embed)

        await msg.add_reaction("✅")
        await msg.add_reaction("⛔")

@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = get(message.reactions, emoji=emoji.name)

    if channel.type == discord.ChannelType.private:
      return

    priorEmbed = message.embeds[0]

    if emoji.name == "⛔" and reaction.count == 2:

        closed = await message.reactions[0].users().flatten()
        closed.remove(client.user)

        embed = discord.Embed(
            title= priorEmbed.title,
            description= "Meeting is over. Attendance list is **closed.**\n‎",
            color=0x62b546)

        embed.set_author(name= priorEmbed.author.name)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/706796095719866469/921016124500508682/attendance.png')

        embed.add_field(name='✅  ATTENDANCE LIST', value='\n'.join([f'{x.mention}' for x in closed]))
        embed.add_field(name='📊  ATTENDANCE COUNT', value=f'**{len(closed)}** participated in the meeting.')

        await message.clear_reactions()
        await message.edit(embed=embed)

client.run('BOT TOKEN HERE') 
