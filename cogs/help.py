import discord
from discord.ext import commands
from datetime import datetime
from config import Config

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config
    
    @commands.command(name='help', aliases=['h', 'commands'])
    async def help_command(self, ctx, command_name: str = None):
        """Show help information for commands"""
        if command_name:
            await self.show_command_help(ctx, command_name)
        else:
            await self.show_general_help(ctx)
    
    async def show_general_help(self, ctx):
        """Show general help embed"""
        embed = discord.Embed(
            title="🎮 Gaming Community Bot Help",
            description=f"Welcome to {ctx.guild.name}! I'm your gaming community bot.",
            color=0x1e90ff
        )
        embed.add_field(
            name="🚀 Getting Started",
            value=f"Use `{self.config.BOT_PREFIX}help <command>` for detailed help on a specific command.",
            inline=False
        )
        embed.add_field(
            name="📖 Command Categories",
            value="**Moderation**: Server management and moderation tools\n"
                  "**Fun**: Gaming commands and entertainment\n"
                  "**Utilities**: Helpful utility commands\n"
                  "**Server Mgmt**: Server setup and management",
            inline=False
        )
        embed.add_field(
            name="🎯 Quick Commands",
            value=f"`{self.config.BOT_PREFIX}ping` - Check bot latency\n"
                  f"`{self.config.BOT_PREFIX}roll` - Roll dice\n"
                  f"`{self.config.BOT_PREFIX}8ball` - Ask magic 8-ball\n"
                  f"`{self.config.BOT_PREFIX}serverinfo` - Server information\n"
                  f"`{self.config.BOT_PREFIX}verify` - Get verified role",
            inline=False
        )
        embed.set_footer(text=f"Prefix: {self.config.BOT_PREFIX} | Bot Version 1.0")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    async def show_command_help(self, ctx, command_name):
        """Show help for a specific command"""
        command = self.bot.get_command(command_name.lower())
        
        if not command:
            embed = discord.Embed(
                title="❌ Command Not Found",
                description=f"Command '{command_name}' not found!",
                color=0xff0000
            )
            embed.add_field(name="Tip", value=f"Use `{self.config.BOT_PREFIX}help` to see all commands", inline=False)
            await ctx.send(embed=embed)
            return
        
        # Get command category
        if command.cog:
            cog_name = command.cog.qualified_name
        else:
            cog_name = "General"
        
        # Build description
        description = command.help or "No description available"
        
        embed = discord.Embed(
            title=f"📖 Help: {command.name}",
            description=description,
            color=0x1e90ff
        )
        
        # Add aliases
        if command.aliases:
            aliases_str = ", ".join(f"`{alias}`" for alias in command.aliases)
            embed.add_field(name="Aliases", value=aliases_str, inline=True)
        
        # Add usage
        usage = f"{self.config.BOT_PREFIX}{command.name}"
        if command.signature:
            usage += f" {command.signature}"
        embed.add_field(name="Usage", value=f"`{usage}`", inline=False)
        
        # Add category
        embed.add_field(name="Category", value=cog_name, inline=True)
        
        embed.set_footer(text="<> = required, [] = optional")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
