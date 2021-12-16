import discord
from discord.utils import get
from pytz import timezone
import os

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Mark your Attendance!'))
    print("bot is ONLINE")

@client.event
async def on_message(message):
  
   if message.author == client.user:
     return

   if message.content == '!attendance':

        await message.delete()

        embed = discord.Embed(
            description = f'‎\nNew attendance list. **Mark your presence!**\n‎',
            color = 0xffffff)

        embed.set_author(name=message.created_at.astimezone(timezone('Europe/Warsaw')).strftime('ATTENDANCE %d.%m.%Y'))
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/706796095719866469/921016124500508682/attendance.png')

        embed.add_field(name='✅  PRESENT', value=f'React below to mark your presence!')
        embed.add_field(name='⛔  CLOSE THE LIST', value=f'Only authorized person closes the list.')

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
        embed.set_thumbnail(url= priorEmbed.thumbnail.url)

        embed.add_field(name='✅  ATTENDANCE LIST', value='\n'.join([f'{x.mention}' for x in closed]))
        embed.add_field(name='📊  ATTENDANCE COUNT', value=f'**{len(closed)}** participated in the meeting.')

        await message.clear_reactions()
        await message.edit(embed=embed)

client.run('BOT TOKEN HERE') 
