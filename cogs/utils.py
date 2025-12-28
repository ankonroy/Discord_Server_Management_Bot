import discord
from discord.ext import commands
import asyncio
import json
import requests
from datetime import datetime, timedelta
from config import Config

class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config
        self.reminders = {}  # Simple in-memory storage for reminders
        
    @commands.command(name='serverinfo', aliases=['si', 'guildinfo'])
    async def server_info(self, ctx):
        """Get server information"""
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            description=guild.description or "No description set",
            color=0x00ff00
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        # Basic info
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Region", value=str(guild.preferred_locale), inline=True)
        
        # Member stats
        total_members = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humans = total_members - bots
        
        embed.add_field(name="👥 Total Members", value=str(total_members), inline=True)
        embed.add_field(name="🤖 Bots", value=str(bots), inline=True)
        embed.add_field(name="👤 Humans", value=str(humans), inline=True)
        
        # Channel stats
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        embed.add_field(name="📝 Text Channels", value=str(text_channels), inline=True)
        embed.add_field(name="🔊 Voice Channels", value=str(voice_channels), inline=True)
        embed.add_field(name="📁 Categories", value=str(categories), inline=True)
        
        # Role stats
        roles = len(guild.roles)
        embed.add_field(name="🏷️ Roles", value=str(roles), inline=True)
        
        # Boost info
        boost_level = guild.premium_subscription_count
        if boost_level > 0:
            embed.add_field(name="⭐ Nitro Boosts", value=f"Level {boost_level}", inline=True)
        
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', aliases=['ui', 'whois'])
    async def user_info(self, ctx, member: discord.Member = None):
        """Get user information"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            description=member.mention,
            color=member.color
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Basic info
        embed.add_field(name="User ID", value=str(member.id), inline=True)
        embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        
        # Account creation
        embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        # Join date
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        
        # Roles
        if len(member.roles) > 1:
            roles = [role.mention for role in member.roles[1:]]  # Exclude @everyone
            role_str = " ".join(roles[:10])  # Show first 10 roles
            if len(roles) > 10:
                role_str += f"\n... and {len(roles) - 10} more"
            embed.add_field(name="Roles", value=role_str, inline=False)
        
        # Permissions
        permissions = []
        if member.guild_permissions.administrator:
            permissions.append("Administrator")
        elif member.guild_permissions.manage_guild:
            permissions.append("Manage Server")
        elif member.guild_permissions.kick_members:
            permissions.append("Kick Members")
        elif member.guild_permissions.ban_members:
            permissions.append("Ban Members")
        elif member.guild_permissions.manage_messages:
            permissions.append("Manage Messages")
        
        if permissions:
            embed.add_field(name="Key Permissions", value=", ".join(permissions), inline=True)
        
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    
    @commands.command(name='poll', aliases=['vote'])
    @commands.has_permissions(manage_messages=True)
    async def create_poll(self, ctx, question: str, *options):
        """Create a poll with multiple choice options"""
        if len(options) < 2:
            await ctx.send("❌ Please provide at least 2 options!")
            return
        
        if len(options) > 10:
            await ctx.send("❌ Maximum 10 options allowed!")
            return
        
        # Create embed
        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=0x1e90ff
        )
        
        # Add options
        option_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        options_text = ""
        for i, option in enumerate(options):
            options_text += f"{option_emojis[i]} {option}\n"
        
        embed.add_field(name="Options", value=options_text, inline=False)
        embed.add_field(name="React with", value="Choose your option above!", inline=False)
        embed.set_footer(text=f"Poll created by {ctx.author.display_name}")
        embed.timestamp = datetime.utcnow()
        
        # Send poll
        message = await ctx.send(embed=embed)
        
        # Add reactions
        for i in range(len(options)):
            await message.add_reaction(option_emojis[i])
        
        # Delete command message
        await ctx.message.delete()
    
    @commands.command(name='remind', aliases=['reminder'])
    async def set_reminder(self, ctx, time: str, *, message):
        """Set a reminder (format: 1m, 1h, 1d)"""
        # Parse time
        time_map = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }
        
        try:
            time_unit = time[-1]
            time_value = int(time[:-1])
            
            if time_unit not in time_map:
                await ctx.send("❌ Invalid time format! Use: 30s, 5m, 1h, 2d")
                return
            
            duration_seconds = time_value * time_map[time_unit]
            
            if duration_seconds > 86400 * 7:  # Max 7 days
                await ctx.send("❌ Maximum reminder time is 7 days!")
                return
            
            # Store reminder (simplified - in production use a database)
            reminder_time = datetime.utcnow() + timedelta(seconds=duration_seconds)
            self.reminders[ctx.author.id] = {
                'message': message,
                'time': reminder_time,
                'channel': ctx.channel.id
            }
            
            embed = discord.Embed(
                title="⏰ Reminder Set",
                description=f"I'll remind you in **{time}**!",
                color=0x00ff00
            )
            embed.add_field(name="Reminder", value=message, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
            # Schedule reminder (simplified)
            await asyncio.sleep(duration_seconds)
            
            # Check if reminder still exists
            if ctx.author.id in self.reminders:
                channel = self.bot.get_channel(self.reminders[ctx.author.id]['channel'])
                if channel:
                    embed = discord.Embed(
                        title="⏰ Reminder!",
                        description=f"Hey {ctx.author.mention}!",
                        color=0xffa500
                    )
                    embed.add_field(name="You asked me to remind you:", value=message, inline=False)
                    embed.timestamp = datetime.utcnow()
                    
                    await channel.send(embed=embed)
                
                # Remove from memory
                del self.reminders[ctx.author.id]
        
        except ValueError:
            await ctx.send("❌ Invalid time format! Use: 30s, 5m, 1h, 2d")
    
    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Latency:** {latency}ms",
            color=0x00ff00
        )
        embed.add_field(name="Bot Uptime", value=f"<t:{int(self.bot.start_time.timestamp())}:R>", inline=True)
        embed.add_field(name="Discord API", value=f"{latency}ms", inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='uptime', aliases=['up'])
    async def uptime(self, ctx):
        """Check bot uptime"""
        uptime = datetime.now() - self.bot.start_time
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
        embed = discord.Embed(
            title="⏱️ Bot Uptime",
            description=f"**{uptime_str}**",
            color=0x00ff00
        )
        embed.add_field(name="Started", value=f"<t:{int(self.bot.start_time.timestamp())}:F>", inline=True)
        embed.add_field(name="Current Time", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='weather', aliases=['temp'])
    async def weather(self, ctx, city: str):
        """Get weather info (requires API key in .env)"""
        if not self.config.WEATHER_API_KEY:
            await ctx.send("❌ Weather API key not configured!")
            return
        
        try:
            # This is a simplified weather call - you'd need to use a real weather API
            # For example: OpenWeatherMap, WeatherAPI, etc.
            # This is just a placeholder
            
            embed = discord.Embed(
                title=f"🌤️ Weather for {city.title()}",
                description="Weather feature requires proper API integration",
                color=0x1e90ff
            )
            embed.add_field(name="Temperature", value="22°C", inline=True)
            embed.add_field(name="Condition", value="Sunny", inline=True)
            embed.add_field(name="Humidity", value="65%", inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error getting weather: {e}")
    
    @commands.command(name='steam', aliases=['steamprofile'])
    async def steam_profile(self, ctx, steam_id: str):
        """Get Steam profile info (requires Steam API key)"""
        if not self.config.STEAM_API_KEY:
            await ctx.send("❌ Steam API key not configured!")
            return
        
        try:
            # Simplified Steam API call - requires real API integration
            embed = discord.Embed(
                title=f"🎮 Steam Profile",
                description=f"Profile ID: {steam_id}",
                color=0x1e90ff
            )
            embed.add_field(name="Level", value="42", inline=True)
            embed.add_field(name="Games Owned", value="156", inline=True)
            embed.add_field(name="Hours Played", value="1,234h", inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error getting Steam profile: {e}")
    
    @commands.command(name='invite', aliases=['botinvite'])
    async def invite_me(self, ctx):
        """Get bot invite link"""
        embed = discord.Embed(
            title="🔗 Bot Invite",
            description="Use this link to invite me to your server!",
            color=0x00ff00
        )
        
        # Get client ID from config
        client_id = self.config.DISCORD_CLIENT_ID
        if client_id:
            invite_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot%20applications.commands"
            embed.add_field(name="Bot Invite Link", value=f"[Click here]({invite_url})", inline=False)
        else:
            embed.add_field(name="⚠️ Note", value="Client ID not configured. Please set DISCORD_CLIENT_ID in .env", inline=False)
        
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    
    @commands.command(name='support', aliases=['helpme'])
    async def support(self, ctx):
        """Get support information"""
        embed = discord.Embed(
            title="🆘 Support",
            description="Need help with the bot? Here's how to get support!",
            color=0xffa500
        )
        embed.add_field(name="Commands Help", value=f"Use `{self.config.BOT_PREFIX}help` for all commands", inline=False)
        embed.add_field(name="Report Issues", value="Contact server administrators", inline=False)
        embed.add_field(name="Feature Requests", value="Suggest new features to moderators", inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))
