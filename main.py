import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# إعداد نوايا البوت
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# إعداد خادم ويب للحفاظ على البوت نشطًا
app = Flask('')


@app.route('/')
def home():
    return "Bot is running"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# عندما يكون البوت جاهزًا
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


# أمر للحصول على مواقيت الصلاة
@bot.command()
async def praytimes(ctx):
    url = 'https://almanar.com.lb/salat.php'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            times_divs = soup.find_all('div', class_='m-left')
            prayer_type_divs = soup.find_all('div', class_='m-right')

            if len(times_divs) == len(prayer_type_divs):
                message = "**مواقيت الصلاة:**\n"
                for time_div, type_div in zip(times_divs, prayer_type_divs):
                    prayer_time = time_div.get_text(strip=True)
                    prayer_type = type_div.get_text(strip=True)
                    message += f"{prayer_type}: {prayer_time}\n"

                await ctx.send(message)
            else:
                await ctx.send(
                    "لم يتم العثور على مواقيت الصلاة بشكل صحيح. يرجى التحقق من الصفحة أو المحاولة مرة أخرى في وقت لاحق."
                )
        else:
            await ctx.send(
                "فشل في جلب مواقيت الصلاة. يرجى المحاولة مرة أخرى في وقت لاحق."
            )
    except Exception as e:
        await ctx.send(f"حدث خطأ: {e}")


# استدعاء دالة keep_alive للحفاظ على البوت نشطًا
keep_alive()
bot.run(
    'MTI0MzYxODg0MzAwODQzNDI2OA.GQPD6a.TdF7nneWj2puW5zLEGVRk94PYPFC1ulz794ZbQ')
