import discord
from discord.ext import commands
import logging

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # 啟用消息內容意圖

bot = commands.Bot(command_prefix='!', intents=intents)

# 更新 SQL 的 discord_id 或拒絕重複使用的用戶
def update_status(member_data):
    # members = read_csv()
    updated = False

    # 檢查成員是否已經存在，並更新 discord_id
    result = data.search_user(member_data)
    # 資料庫出現錯誤
    if result == "error":
        return "error"
    # 有資料的話
    elif result:
        stored_email, stored_name, stored_discordId = result
        if stored_email == member_data['email'] and stored_name == member_data['name']:
            if not member['discord_id']:
                updated = True
            else:
                if stored_discordId == member_data['discord_id']:
                    return False
                else:
                    return "duplicate"
    # 找不到該資料
    else:
        return False

    # 如果找到並更新了用戶訊息，更新 SQL 資訊
    if updated:
        updated_result = data.update_user(member_data)
        if updated_result == 'error':
            return 'error'
        return updated_result

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    logging.info(f'New member joined: {member.name}')
    # 針對 channel name 更改
    welcome_channel = discord.utils.get(member.guild.text_channels, name="一般")
    unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
    
    if unverified_role:
        await member.add_roles(unverified_role)
        logging.info(f'Added Unverified role to {member.name}')
    else:
        logging.warning('Unverified role not found')
    
    if welcome_channel:
        await welcome_channel.send(f"歡迎 {member.mention}！請使用 `!verify 姓名 email` 命令來驗證您的身份。名字請輸入您在ccClub官網報名表的真實姓名和email。!verify、名字、email是空白鍵間隔開，!verify中間無空格")
        logging.info(f'Sent welcome message to {member.name}')
    else:
        logging.warning('Welcome channel not found')

def is_unverified():
    async def predicate(ctx):
        return discord.utils.get(ctx.author.roles, name="Unverified") is not None
    return commands.check(predicate)

@bot.command()
@is_unverified()
async def verify(ctx, name: str, email: str):
    # logging.info(f'Verify command used by {ctx.author.name}')
    logging.info(f'Verify command used by {ctx.author.name} with name: {name}, email: {email}')
    member = ctx.author
    member_data = {
        "name": name,
        "email": email,
        "discord_id": str(member.id)
    }

    result = update_status(member_data)
    if result == "error":
        await ctx.send(f"{member.mention}, 目前 Verify Bot 有狀況，請聯繫管理員處理。")
    elif result == "duplicate":
        await ctx.send(f"{member.mention}, 這個email已被另一個Discord ID使用。請聯繫管理員處理。")
        logging.warning(f'Duplicate email used by {member.name}')
    elif not result:
        await ctx.send(f"{member.mention}, 你已經註冊過了。")
        logging.info(f'{member.name} already registered')
    else:
        verified_role = discord.utils.get(member.guild.roles, name="2024fall")
        unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
        if verified_role:
            await member.add_roles(verified_role)
            logging.info(f'Added 2024fall role to {member.name}')
        else:
            logging.warning('2024fall role not found')
        if unverified_role:
            await member.remove_roles(unverified_role)
            logging.info(f'Removed Unverified role from {member.name}')
        await ctx.send(f"{member.mention}, 您已通過驗證並獲得存取權限！")

    # 刪除包含個人信息的消息
    await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("請提供正確的格式：`!verify 姓名 email`")
        logging.error(f'Missing argument error: {error}')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("只有未驗證的用戶可以使用此命令。")
        logging.error(f'Check failure error: {error}')
    else:
        logging.error(f'Unhandled error: {error}')

@bot.command()
async def ping(ctx):
    await ctx.send("pong")
