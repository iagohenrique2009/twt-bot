import asyncio
import aiohttp
from twitchio.ext import commands

# Configuração direta dos tokens e IDs
ACCESS_TOKEN = 'zw1zv7ltonhexc13m0r8b3rb13h5g5'
REFRESH_TOKEN = 'oc8g5j7yk8869aymsbtgtbghfs5awwzlkjfsgc7tam4r1oh6co'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'

# Inicialize o bot com o token e o canal
bot = commands.Bot(
    token=ACCESS_TOKEN,  # Token de acesso direto no código
    prefix='!',  # Prefixo para comandos
    initial_channels=['nevertoolatel2']  # Substitua com o nome do seu canal
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
async def check_image_ready(img_name):
    # Substitui espaços por %20 no nome da imagem para construir a URL corretamente
    formatted_img_name = img_name.replace(" ", "%20")
    image_url = f'https://image.pollinations.ai/prompt/{formatted_img_name}'
    
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(image_url) as response:
                if response.status == 200:
                    return image_url  # A imagem está pronta e o link pode ser usado
                elif response.status == 404:
                    print(f'A imagem "{img_name}" ainda não está disponível.')
                else:
                    print(f'Erro ao tentar carregar a imagem "{img_name}", código de status: {response.status}')

                # Espera 5 segundos antes de tentar novamente
                await asyncio.sleep(5)

# Comando !imagem que gera o link da imagem
@bot.command(name='imagem')
async def imagem(ctx, *, img_name: str):
    # Mensagem inicial informando que a imagem está em processamento
    await ctx.send("1 minuto, já farei sua imagem...")

    # Aguarda até que a imagem esteja pronta
    image_url = await check_image_ready(img_name)
    
    if image_url:
        # Envia a mensagem final com o link para a imagem
        await ctx.send(f'Aqui está o link para a imagem \"{img_name}\": {image_url}')
    else:
        await ctx.send(f"Desculpe, não foi possível gerar a imagem '{img_name}'. Verifique o nome ou tente novamente mais tarde.")

# Inicie o bot
if __name__ == "__main__":
    bot.run()
