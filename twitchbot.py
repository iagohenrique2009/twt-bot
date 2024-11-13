import asyncio
import aiohttp
from urllib.parse import quote
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
async def check_image_ready(img_name, max_attempts=12, delay=5):
    # Manter o nome da imagem sem codificar na verificação de status
    image_url = f'https://image.pollinations.ai/prompt/{img_name}'
    print(f"Verificando URL: {image_url}")  # Log para verificar a URL

    async with aiohttp.ClientSession() as session:
        attempts = 0
        while attempts < max_attempts:
            async with session.get(image_url) as response:
                if response.status == 200:
                    return image_url  # A imagem está pronta e o link pode ser usado
                elif response.status == 404:
                    print(f'A imagem "{img_name}" ainda não está disponível. Tentativa {attempts + 1}/{max_attempts}')
                else:
                    print(f'Erro ao tentar carregar a imagem "{img_name}", código de status: {response.status}')

            # Incrementa o número de tentativas e espera antes de tentar novamente
            attempts += 1
            await asyncio.sleep(delay)

    # Retorna None se o número máximo de tentativas for alcançado
    return None

# Comando !imagem que gera o link da imagem
@bot.command(name='imagem')
async def imagem(ctx, *, img_name: str):
    # Mensagem inicial informando que a imagem está em processamento
    await ctx.send("1 minuto, já farei sua imagem...")

    # Aguarda até que a imagem esteja pronta ou que o número máximo de tentativas seja alcançado
    image_url = await check_image_ready(img_name)
    
    if image_url:
        # Codifica a URL para o link de retorno, garantindo %20 no lugar de espaços
        encoded_image_url = f'https://image.pollinations.ai/prompt/{quote(img_name)}'
        # Envia a mensagem final com o link para a imagem
        await ctx.send(f'Aqui está o link para a imagem \"{img_name}\": {encoded_image_url}')
    else:
        await ctx.send(f"Desculpe, não foi possível gerar a imagem '{img_name}' no tempo esperado. Tente novamente mais tarde.")

# Inicie o bot
if __name__ == "__main__":
    bot.run()
