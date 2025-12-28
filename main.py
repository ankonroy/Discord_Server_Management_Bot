import discord
from discord.ext import commands, tasks
import logging
import asyncio
import sys
from datetime import datetime
from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('DiscordBot')

class GamingCommunityBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.guild_messages = True
        intents.guild_reactions = True
        
        super().__init__(
            command_prefix=Config.BOT_PREFIX,
            case_insensitive=True,
            intents=intents,
            help_command=None
        )
        
        self.start_time = datetime.now()
        
    async def setup_hook(self):
        """Setup the bot when it starts"""
        logger.info("Setting up bot...")
        
        # Load all cogs
        cogs = [
            'cogs.moderation',
            'cogs.fun',
            'cogs.utils',
            'cogs.server_mgmt',
            'cogs.help'
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")
        
        # Start background tasks
        if not self.cleanup_task.is_running():
            self.cleanup_task.start()
            
        logger.info("Bot setup complete!")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'Bot is ready! Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        logger.info(f'Prefix: {Config.BOT_PREFIX}')
        
        # Update bot activity
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | {Config.BOT_PREFIX}help"
            )
        )
    
    async def on_guild_join(self, guild):
        """Called when bot joins a new guild"""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Send welcome message to general channel if available
        general_channel = discord.utils.get(guild.channels, name='general')
        if general_channel:
            embed = discord.Embed(
                title="🎮 Gaming Community Bot Joined!",
                description="Thanks for adding me to your server! I'm here to help moderate, add fun commands, and manage your gaming community.",
                color=0x00ff00
            )
            embed.add_field(
                name="Getting Started",
                value=f"Use `{Config.BOT_PREFIX}help` to see all available commands!",
                inline=False
            )
            embed.add_field(
                name="Features",
                value="• Moderation tools\n• Fun gaming commands\n• Server management\n• Utility features",
                inline=False
            )
            await general_channel.send(embed=embed)
    
    async def on_member_join(self, member):
        """Called when a new member joins"""
        if Config.WELCOME_CHANNEL_ID:
            channel = self.get_channel(Config.WELCOME_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title="🎉 Welcome to the server!",
                    description=f"Welcome {member.mention} to **{member.guild.name}**! We're excited to have you join our gaming community!",
                    color=0x00ff00
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
                embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)
                
                await channel.send(embed=embed)
        
        # Auto-assign newcomer role if exists
        if Config.NEW_MEMBER_ROLE_NAME:
            role = discord.utils.get(member.guild.roles, name=Config.NEW_MEMBER_ROLE_NAME)
            if role:
                try:
                    await member.add_roles(role)
                    logger.info(f"Added {Config.NEW_MEMBER_ROLE_NAME} role to {member}")
                except discord.Forbidden:
                    logger.warning(f"Could not add role to {member}")
    
    async def on_member_remove(self, member):
        """Called when a member leaves"""
        if Config.GOODBYE_CHANNEL_ID:
            channel = self.get_channel(Config.GOODBYE_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title="👋 Member Left",
                    description=f"**{member.display_name}** has left the server. We'll miss you!",
                    color=0xff0000
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)
                
                await channel.send(embed=embed)
    
    @tasks.loop(minutes=30)
    async def cleanup_task(self):
        """Background task for cleanup operations"""
        logger.info("Running cleanup task...")
        # Add any cleanup operations here
        # For example: clean old database records, reset daily counters, etc.
    
    @cleanup_task.before_loop
    async def before_cleanup_task(self):
        await self.wait_until_ready()
    
    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command!")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ Command on cooldown. Try again in {error.retry_after:.1f} seconds!")
        else:
            logger.error(f"Command error in {ctx.command}: {error}")
            await ctx.send("❌ An error occurred while executing the command!")
    
    async def get_uptime(self):
        """Get bot uptime"""
        return datetime.now() - self.start_time

async def main():
    """Main function to run the bot"""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    # Create and run bot
    bot = GamingCommunityBot()
    
    try:
        await bot.start(Config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid Discord token. Please check your .env file!")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutting down...")
