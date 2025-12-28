import discord
from discord.ext import commands
import logging
from datetime import datetime, timedelta
from config import Config

logger = logging.getLogger('ModerationCog')

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config
        
    @commands.command(name='kick', aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server"""
        try:
            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"**{member.display_name}** has been kicked from the server.",
                color=0xff0000
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.timestamp = datetime.utcnow()
            
            await member.kick(reason=reason)
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} kicked {member} for: {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick this member!")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to kick member: {e}")
    
    @commands.command(name='ban', aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server"""
        try:
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"**{member.display_name}** has been banned from the server.",
                color=0xff0000
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.timestamp = datetime.utcnow()
            
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} banned {member} for: {reason}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban this member!")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to ban member: {e}")
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban_member(self, ctx, user_id: int):
        """Unban a member by their ID"""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            
            embed = discord.Embed(
                title="✅ Member Unbanned",
                description=f"**{user.display_name}** has been unbanned from the server.",
                color=0x00ff00
            )
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.add_field(name="User ID", value=user.id, inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} unbanned {user}")
            
        except discord.NotFound:
            await ctx.send("❌ User not found in ban list!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unban this member!")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to unban member: {e}")
    
    @commands.command(name='timeout', aliases=['mute', 'silence'])
    @commands.has_permissions(moderate_members=True)
    async def timeout_member(self, ctx, member: discord.Member, duration: str, *, reason="No reason provided"):
        """Timeout a member (mute them)"""
        try:
            # Parse duration (e.g., "1h", "30m", "2d")
            duration_map = {
                's': 1,
                'm': 60,
                'h': 3600,
                'd': 86400
            }
            
            time_unit = duration[-1]
            time_value = int(duration[:-1])
            
            if time_unit not in duration_map:
                await ctx.send("❌ Invalid time format! Use: s (seconds), m (minutes), h (hours), d (days)")
                return
            
            duration_seconds = time_value * duration_map[time_unit]
            timeout_duration = timedelta(seconds=duration_seconds)
            
            await member.timeout(timeout_duration, reason=reason)
            
            embed = discord.Embed(
                title="🤫 Member Timed Out",
                description=f"**{member.display_name}** has been timed out for {duration}.",
                color=0xffa500
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.add_field(name="Duration", value=duration, inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} timed out {member} for {duration} for: {reason}")
            
        except ValueError:
            await ctx.send("❌ Invalid duration format! Use: 30m, 1h, 2d, etc.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to timeout this member!")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to timeout member: {e}")
    
    @commands.command(name='untimeout', aliases=['unmute', 'unsilence'])
    @commands.has_permissions(moderate_members=True)
    async def untimeout_member(self, ctx, member: discord.Member):
        """Remove timeout from a member"""
        try:
            await member.timeout(None)
            
            embed = discord.Embed(
                title="🔓 Timeout Removed",
                description=f"Timeout removed from **{member.display_name}**.",
                color=0x00ff00
            )
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} removed timeout from {member}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to remove timeout from this member!")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to remove timeout: {e}")
    
    @commands.command(name='clear', aliases=['purge', 'delete'])
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int = 5):
        """Clear a specified number of messages"""
        try:
            if amount < 1 or amount > 100:
                await ctx.send("❌ Amount must be between 1 and 100!")
                return
            
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
            
            embed = discord.Embed(
                title="🗑️ Messages Cleared",
                description=f"Deleted **{len(deleted) - 1}** messages.",
                color=0x808080
            )
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed, delete_after=5)
            logger.info(f"{ctx.author} cleared {len(deleted) - 1} messages in {ctx.channel}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to delete messages!")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to clear messages: {e}")
    
    @commands.command(name='warn', aliases=['w'])
    @commands.has_permissions(kick_members=True)
    async def warn_member(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member"""
        try:
            embed = discord.Embed(
                title="⚠️ Member Warned",
                description=f"**{member.display_name}** has been warned.",
                color=0xffa500
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.timestamp = datetime.utcnow()
            
            # Send warning to member
            try:
                await member.send(f"You have been warned in **{ctx.guild.name}**: {reason}")
            except discord.Forbidden:
                pass  # Can't DM user
            
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} warned {member} for: {reason}")
            
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to warn member: {e}")
    
    @commands.command(name='warnings', aliases=['warns'])
    @commands.has_permissions(kick_members=True)
    async def view_warnings(self, ctx, member: discord.Member = None):
        """View warnings for a member (currently basic implementation)"""
        if member is None:
            member = ctx.author
        
        # This would typically check a database for warnings
        embed = discord.Embed(
            title=f"⚠️ Warnings for {member.display_name}",
            description="Warning system is currently in development. Full warning history will be available soon!",
            color=0xffa500
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await ctx.send(embed=embed)
    
    # Auto-moderation features
    @commands.Cog.listener()
    async def on_message(self, message):
        """Auto-moderation for spam and bad words"""
        if message.author.bot:
            return
        
        # Check for spam
        if self.config.SPAM_PROTECTION:
            # Basic spam detection (this would be more sophisticated in a real implementation)
            if len(message.content) > self.config.MAX_MESSAGE_LENGTH:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Your message was too long!", delete_after=5)
        
        # Check for bad words
        if self.config.BAD_WORDS_FILTER:
            content_lower = message.content.lower()
            for bad_word in self.config.BAD_WORDS:
                if bad_word.lower() in content_lower:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Inappropriate language detected!", delete_after=5)
                    break

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
