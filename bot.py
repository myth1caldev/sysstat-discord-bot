import discord
from discord.ext import commands, tasks
import psutil
from PIL import Image, ImageDraw
from io import BytesIO

TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command("help")

STATUS_CHANNEL_ID = STATUS_CHANNEL_ID_HERE
STATUS_MESSAGE_ID = None

def get_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    net = psutil.net_io_counters()
    network_mbps = (net.bytes_sent + net.bytes_recv) / 1024 / 1024
    return cpu, ram, disk, round(network_mbps, 2)

def draw_bar(draw, x, y, width, height, value, label):
    radius = 10
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius,
        fill=(30, 30, 50),
        outline=(50, 50, 70),
        width=1
    )
    fill_width = int(width * (value / 100))
    draw.rounded_rectangle(
        [x, y, x + fill_width, y + height],
        radius,
        fill=(20, 135, 234)
    )
    draw.text(
        (x, y - 22),
        label,
        fill="white"
    )

def create_status_image(cpu, ram, disk, network):
    width = 800
    height = 300
    img = Image.new("RGB", (width, height), (20, 20, 35))
    draw = ImageDraw.Draw(img)

    bar_width = 700
    bar_height = 32
    x = (width - bar_width) // 2

    total_bars_height = 3 * bar_height + 2 * 32
    start_y = (height - total_bars_height) // 2

    y_positions = [
        start_y,
        start_y + bar_height + 32,
        start_y + 2 * (bar_height + 32)
    ]

    draw_bar(draw, x, y_positions[0], bar_width, bar_height, cpu, f"CPU LOAD {cpu}%")
    draw_bar(draw, x, y_positions[1], bar_width, bar_height, ram, f"RAM LOAD {ram}%")
    draw_bar(draw, x, y_positions[2], bar_width, bar_height, disk, f"DISK LOAD {disk}%")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def create_embed(cpu, ram, disk, network):
    embed = discord.Embed(
        title="System Status",
        description="> Real-time system monitoring.\n> Auto-updates every 30 seconds.",
        color=0x1487EA
    )
    embed.add_field(
        name="**__Current Values__**",
        value=(
            f"> **CPU:** `{cpu}%`\n"
            f"> **RAM:** `{ram}%`\n"
            f"> **DISK:** `{disk}%`\n"
            f"> **NETWORK:** `{network} Mbps`"
        ),
        inline=False
    )
    embed.add_field(
        name="**__Status__**",
        value="> System Online",
        inline=False
    )
    embed.set_image(url="attachment://status.png")
    return embed

@tasks.loop(seconds=30)
async def update_status():
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if channel is None:
        return

    cpu, ram, disk, network = get_stats()
    image = create_status_image(cpu, ram, disk, network)
    file = discord.File(image, filename="status.png")
    embed = create_embed(cpu, ram, disk, network)

    global STATUS_MESSAGE_ID
    try:
        if STATUS_MESSAGE_ID:
            msg = await channel.fetch_message(STATUS_MESSAGE_ID)
            await msg.edit(embed=embed, attachments=[file])
        else:
            msg = await channel.send(embed=embed, file=file)
            STATUS_MESSAGE_ID = msg.id
    except Exception as e:
        print(e)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="System Status: Online"))
    if not update_status.is_running():
        update_status.start()

bot.run(TOKEN)
