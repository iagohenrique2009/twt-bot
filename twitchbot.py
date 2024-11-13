import asyncio
import aiohttp
from urllib.parse import quote
from twitchio.ext import commands
import os

# Configuração direta dos tokens e IDs
ACCESS_TOKEN = 'zw1zv7ltonhexc13m0r8b3rb13h5g5'
REFRESH_TOKEN = 'oc8g5j7yk8869aymsbtgtbghfs5awwzlkjfsgc7tam4r1oh6co'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'

# Inicialize o bot com o token e os canais
bot = commands.Bot(
    token=ACCESS_TOKEN,
    prefix='!',
    initial_channels=['nevertoolatel2', 'iagonumeros']  # Lista de canais para o bot
)

@bot.event
async def event_ready():
    print(f'Logged in as | {bot.nick}')

@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == bot.nick.lower():
        return

    await bot.handle_commands(ctx)

# Função para verificar se a imagem está disponível no endpoint /prompt
async def check_image_ready(img_name, max_attempts=12, delay=5):
    formatted_img_name = quote(img_name)
    image_url = f'https://image.pollinations.ai/prompt/{formatted_img_name}'
    
    async with aiohttp.ClientSession() as session:
        attempts = 0
        while attempts < max_attempts:
            async with session.get(image_url) as response:
                if response.status == 200:
                    return image_url
                elif response.status == 404:
                    print(f'A imagem "{img_name}" ainda não está disponível. Tentativa {attempts + 1}/{max_attempts}')
                else:
                    print(f'Erro ao tentar carregar a imagem "{img_name}", código de status: {response.status}')
            attempts += 1
            await asyncio.sleep(delay)
    return None

# Comando !imagem que gera o link da imagem
@bot.command(name='imagem')
async def imagem(ctx, *, img_name: str):
    await ctx.send("1 minuto, já farei sua imagem...")
    image_url = await check_image_ready(img_name)
    
    if image_url:
        encoded_image_url = f'https://image.pollinations.ai/prompt/{quote(img_name)}'
        await ctx.send(f'Aqui está o link para a imagem \"{img_name}\": {encoded_image_url}')
    else:
        await ctx.send(f"Desculpe, não foi possível gerar a imagem '{img_name}' no tempo esperado. Tente novamente mais tarde.")

# Inicie o bot da Twitch
if __name__ == "__main__":
    bot.run()
