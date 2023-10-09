import discord
from discord.ext import commands

import config

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} online!')

    channel_id = ID_DO_CANAL
    user_id = ID_DO_USUARIO

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(f'Estou Online <@{user_id}>!')

    user = await bot.fetch_user(user_id)
    if user:
        await user.send('Estou Online!') 
    
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if 'oi' in message.content.lower():
        await message.channel.send('Olá!')

    if "entre bot" in message.content.lower():
        # Verifica se o autor da mensagem está em um canal de voz
        if message.author.voice:
            voice_channel = message.author.voice.channel
            try:
                voice_client = await voice_channel.connect()
                print(f'Bot entrou no canal de voz {voice_channel.name}')

                # Reproduza um arquivo de áudio MP3 quando o bot entrar
                audio_source = discord.FFmpegPCMAudio('CAMINHO_DO_ARQUIVO.MP3')
                voice_client.play(audio_source)

            except discord.ClientException:
                print('O bot já está em um canal de voz')
            except Exception as e:
                print(f'Ocorreu um erro: {e}')
        else:
            await message.channel.send('Você precisa estar em um canal de voz para que o bot entre.')
            
    if isinstance(message.channel, discord.DMChannel): 
        # Envia no canal do servidor a mensagem recebida no DM
        channel_id = ID_DO_CANAL 
        server_channel = bot.get_channel(channel_id)
        if server_channel:
            await server_channel.send(f'Mensagem de {message.author.display_name} em DM: {message.content}')
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    # impede alguém de entrar no canal de voz
    user_id_to_remove = ID_DO_USUARIO
    ativado = True 
    if member.id == user_id_to_remove and ativado == True:
        if after.channel:
            await member.move_to(None) 

bot.run(config.TOKEN)
