import discord
from discord.ext import commands
import random
import os
import requests


intents = discord.Intents.default() # botun sunucudaki üyelere erişebilmesi ve gönderilen mesajları okuyabilmesi için verilen ayrıcalıklar/ izinler.
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents) # bot komutları için ön takı "?" dir

@bot.event
async def on_ready():# botun hazır olduğunu belirtir
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

def get_duck_image_url(): # ördek fotoğraflarını kullandığımız site linki 
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

# Mem nadirlik değeri ekleme
mem_images = {
    'mem1.png': 0.6,  # Daha sık gönderilecek
    'mem2.png': 0.3,  # Orta nadirlikte gönderilecek
    'mem3.png': 0.1,  # Çok nadir gönderilecek
    'mem4.jpg': 0.2   # Nadir gönderilecek
}

@bot.command('duck') # ?duck komutu ile rastgele ördek fotografları gönderir
async def duck(ctx):
    
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command()
async def el_isi(ctx): # ?el_isi komutu ile evde yapılabilecek geri dönüşüm etkinlikleri örneği verir
    
    ideas = [
        "Plastik şişelerden çiçek saksısı yapabilirsiniz.",
        "Eski plastik kapakları kullanarak mozaik tablo yapabilirsiniz.",
        "Pet şişelerden kalemlik yapabilirsiniz.",

        "Kağıt tüplerden (tuvalet kağıdı veya mutfak kağıdı) çocuklar için oyuncak yapabilirsiniz.",
        "Eski karton kutuları kullanarak dekoratif kutular veya organizatörler tasarlayabilirsiniz.",
        "Kağıt artıklarıyla kolaj yaparak sanat eseri oluşturabilirsiniz.",

        "Boş cam şişeleri boyayarak dekoratif vazo yapabilirsiniz.",
        "Eski cam kavanozları kullanarak mumluk veya ışıklandırma yapmak için kullanabilirsiniz.",
        "Cam şişeleri kullanarak bahçe için su verme sistemi tasarlayabilirsiniz.",

        "Eski teneke kutuları kullanarak saksı veya kalemlik yapabilirsiniz.",
        "Alüminyum folyo ile çeşitli sanat projeleri tasarlayabilirsiniz.",
        "Metal kapakları kullanarak birçok yaratıcı takı veya anahtarlık yapabilirsiniz.",

        "Eski tahtalardan raf veya dekoratif tablalar yapabilirsiniz.",
        "Kullanılmayan ahşap çerçevelerden resim çerçeveleri oluşturabilirsiniz.",
        "Küçük ahşap parçalarıyla çocuklar için eğitici oyuncaklar yapabilirsiniz."
    ]
    idea = random.choice(ideas)
    await ctx.send(idea)


@bot.command()
async def donusum(ctx, item: str): #?donusum komutu ile atık malzemelerin nasıl geri dönüştürülebileceği hakkında bilgi verir
    
    recycling_guide = {
        "plastik şişe": "geri dönüştürülebilir",
        "kağıt": "geri dönüştürülebilir",
        "cam şişe": "geri dönüştürülebilir",
        "pil": "geri dönüşüm merkezine götürülmeli",
        "yiyecek artıkları": "sokak hayvanlarına verilebilir",
        "alüminyum kutu": "geri dönüştürülebilir"
    }

    normalized_item = item.lower().strip()
    result = recycling_guide.get(normalized_item, "Bu eşya hakkında bilgim yok.")
    await ctx.send(f"{item.capitalize()} {result}.")


@bot.command() # ?add komutu ile iki tamsayıyı toplayan komut
async def add(ctx, left: int, right: int):
    # iki sayı birlikte verilmelidir 
    await ctx.send(left + right)

@bot.command() # ?mem komutu ile klasörde bulunan mem'leri ağırlık değerine göre gönderir
async def mem(ctx):
    
    img_name = random.choices(list(mem_images.keys()), weights=mem_images.values())[0]
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command() # ?roll komutu ile kaç adet ve kaç yüzlü olduğunu belirlediğimiz şekilde zar atar 
async def roll(ctx, dice: str):
    
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way') # ?choose komutu ile belirlediğimiz nesneler arasında seçim yapar
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))


@bot.command() # ?joined komutu ve seçtiğimiz kullanıcı adını etiketlediğimizde, kullanıcının sunucuya giriş yaptığı tarihi verir
async def joined(ctx, member: discord.Member):
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


bot.run('') # botumuzun gizli anahtarı 
