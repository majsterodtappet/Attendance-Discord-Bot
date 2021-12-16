import discord
from discord.utils import get
from pytz import timezone
import os
#from keep_alive import keep_alive

client = discord.Client()

raport = 'https://docs.google.com/document/d/1865-IBRF_5Z6GWNk5JnmZERrbtJBKBHJU18ner8-sx8/edit'

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='SUSTAINABLES'))
    print("bot is ONLINE")

@client.event
async def on_message(message):
  
   if message.author == client.user:
     return

   if message.content == '!spotkanie':

        await message.delete()

        embed = discord.Embed(
            description = f'‎\nLista obecności ze spotkania projektu Zrównoważonego Osiedla dołączana do raportu. **Zaznacz swoją obecność!**\n‎',
            color = 0x89CFF0)

        embed.set_author(name=message.created_at.astimezone(timezone('Europe/Warsaw')).strftime('SPOTKANIE %d.%m.%Y'),icon_url='https://media.discordapp.net/attachments/706796095719866469/920727301791027220/sus.png')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/706796095719866469/920643774349205564/Bezowy_i_Szary_Minimalistyczny_Cytat_Post_na_Instagram.png')

        embed.add_field(name='📄  RAPORT ZE SPOTKANIA', value=f'Raport ze spotkania znajduje się w tym [pliku]({raport}). \n ‎\n', inline=False)

        embed.add_field(name='✅  OBECNY/A', value=f'Zareaguj poniżej!')
        embed.add_field(name='⛔  ZAMKNIJ LISTĘ', value=f'Listę zamyka koordynator projektu.')

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
            description= "Lista obecności ze spotkania projektu Zrównoważonego Osiedla dołączana do raportu. **Lista zamknięta.**\n‎",
            color=0x62b546)

        embed.set_author(name= priorEmbed.author.name, icon_url= priorEmbed.author.icon_url)
        embed.set_thumbnail(url= priorEmbed.thumbnail.url)

        embed.add_field(name= priorEmbed.fields[0].name, value= priorEmbed.fields[0].value, inline=False)
        embed.add_field(name='✅  LISTA OBECNYCH', value='\n'.join([f'{x.mention}' for x in closed]))
        embed.add_field(name='📊  ILOŚĆ OBECNYCH', value=f'W spotkaniu wzięło udział **{len(closed)}** osób.')

        await reaction.remove(payload.member)
        await message.edit(embed=embed)
        await message.clear_reactions()


#keep_alive()
client.run('OTIwNjEwMzAwNzMzMDYzMjA5.Ybm3Jw._sjCyvqiylIzzuO6d6WY2ERR_IY')