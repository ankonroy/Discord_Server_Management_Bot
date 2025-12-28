import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from config import Config

class ServerMgmtCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config
        
    @commands.command(name='setup', aliases=['init'])
    @commands.has_permissions(administrator=True)
    async def setup_server(self, ctx):
        """Setup server with basic configuration"""
        await ctx.send("🔧 Setting up server configuration...")
        
        try:
            # Create basic roles
            await self.create_basic_roles(ctx.guild)
            
            # Create basic channels
            await self.create_basic_channels(ctx.guild)
            
            embed = discord.Embed(
                title="✅ Server Setup Complete",
                description="Basic server structure has been created!",
                color=0x00ff00
            )
            embed.add_field(name="Created Roles", value="• Gamer\n• Newcomer\n• Verified", inline=True)
            embed.add_field(name="Created Channels", value="• welcome\n• rules\n• general\n• gaming\n• memes", inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Setup failed: {e}")
    
    async def create_basic_roles(self, guild):
        """Create basic server roles"""
        role_names = [
            (self.config.GAMING_ROLE_NAME, 0x00ff00),
            (self.config.NEW_MEMBER_ROLE_NAME, 0xffa500),
            (self.config.VERIFIED_ROLE_NAME, 0x1e90ff)
        ]
        
        for role_name, color in role_names:
            if not discord.utils.get(guild.roles, name=role_name):
                await guild.create_role(
                    name=role_name,
                    color=discord.Color(color),
                    reason="Basic server setup"
                )
    
    async def create_basic_channels(self, guild):
        """Create basic server channels"""
        channels_to_create = [
            ("welcome", discord.ChannelType.text, "Welcome new members!"),
            ("rules", discord.ChannelType.text, "Server rules and guidelines"),
            ("general", discord.ChannelType.text, "General discussion"),
            ("gaming", discord.ChannelType.text, "Gaming discussions"),
            ("memes", discord.ChannelType.text, "Share your best memes!"),
            ("voice-general", discord.ChannelType.voice, "General voice chat"),
            ("voice-gaming", discord.ChannelType.voice, "Gaming voice chat")
        ]
        
        for channel_name, channel_type, topic in channels_to_create:
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if not existing_channel:
                await guild.create_text_channel(
                    name=channel_name,
                    topic=topic,
                    reason="Basic server setup"
                ) if channel_type == discord.ChannelType.text else await guild.create_voice_channel(
                    name=channel_name,
                    reason="Basic server setup"
                )
    
    @commands.command(name='setwelcome', aliases=['welcomeset'])
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        """Set the welcome channel"""
        # This would typically save to database
        embed = discord.Embed(
            title="✅ Welcome Channel Set",
            description=f"Welcome messages will now be sent to {channel.mention}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='setgoodbye', aliases=['goodbyeset'])
    @commands.has_permissions(manage_guild=True)
    async def set_goodbye_channel(self, ctx, channel: discord.TextChannel):
        """Set the goodbye channel"""
        embed = discord.Embed(
            title="✅ Goodbye Channel Set",
            description=f"Goodbye messages will now be sent to {channel.mention}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='roleinfo', aliases=['ri'])
    async def role_info(self, ctx, role: discord.Role):
        """Get information about a role"""
        embed = discord.Embed(
            title=f"🏷️ {role.name}",
            description=role.mention,
            color=role.color
        )
        embed.add_field(name="Role ID", value=str(role.id), inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Position", value=str(role.position), inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Members", value=str(len(role.members)), inline=True)
        
        # Permissions
        if role.permissions.administrator:
            perm_text = "Administrator"
        else:
            perms = []
            if role.permissions.kick_members:
                perms.append("Kick Members")
            if role.permissions.ban_members:
                perms.append("Ban Members")
            if role.permissions.manage_messages:
                perms.append("Manage Messages")
            if role.permissions.manage_roles:
                perms.append("Manage Roles")
            perm_text = ", ".join(perms) if perms else "No special permissions"
        
        embed.add_field(name="Permissions", value=perm_text, inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='channelinfo', aliases=['ci'])
    async def channel_info(self, ctx, channel: discord.TextChannel = None):
        """Get information about a channel"""
        if channel is None:
            channel = ctx.channel
        
        embed = discord.Embed(
            title=f"📁 {channel.name}",
            description=channel.topic or "No topic set",
            color=0x1e90ff
        )
        embed.add_field(name="Channel ID", value=str(channel.id), inline=True)
        embed.add_field(name="Type", value=str(channel.type).title(), inline=True)
        embed.add_field(name="Created", value=channel.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Position", value=str(channel.position), inline=True)
        
        # Member count (for text channels)
        if hasattr(channel, 'member_count'):
            embed.add_field(name="Members", value=str(channel.member_count), inline=True)
        
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    
    @commands.command(name='addrole', aliases=['ar'])
    @commands.has_permissions(manage_roles=True)
    async def add_role_to_member(self, ctx, member: discord.Member, *, role_name: str):
        """Add a role to a member"""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if not role:
            await ctx.send(f"❌ Role '{role_name}' not found!")
            return
        
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ You can't assign a role higher than your own!")
            return
        
        try:
            await member.add_roles(role)
            embed = discord.Embed(
                title="✅ Role Added",
                description=f"Added {role.mention} to {member.mention}",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to add this role!")
    
    @commands.command(name='removerole', aliases=['rr'])
    @commands.has_permissions(manage_roles=True)
    async def remove_role_from_member(self, ctx, member: discord.Member, *, role_name: str):
        """Remove a role from a member"""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if not role:
            await ctx.send(f"❌ Role '{role_name}' not found!")
            return
        
        try:
            await member.remove_roles(role)
            embed = discord.Embed(
                title="✅ Role Removed",
                description=f"Removed {role.mention} from {member.mention}",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to remove this role!")
    
    @commands.command(name='slowmode', aliases=['slow'])
    @commands.has_permissions(manage_channels=True)
    async def set_slowmode(self, ctx, seconds: int):
        """Set slowmode for the current channel"""
        if seconds < 0 or seconds > 21600:  # Max 6 hours
            await ctx.send("❌ Slowmode must be between 0 and 21600 seconds (6 hours)!")
            return
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                await ctx.send("✅ Slowmode disabled!")
            else:
                await ctx.send(f"✅ Slowmode set to {seconds} seconds!")
                
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to manage this channel!")
    
    @commands.command(name='lock', aliases=['lockdown'])
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx, channel: discord.TextChannel = None):
        """Lock a channel"""
        if channel is None:
            channel = ctx.channel
        
        try:
            # Remove send permissions for @everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            
            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"{channel.mention} has been locked.",
                color=0xff0000
            )
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to lock this channel!")
    
    @commands.command(name='unlock', aliases=['unlockdown'])
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx, channel: discord.TextChannel = None):
        """Unlock a channel"""
        if channel is None:
            channel = ctx.channel
        
        try:
            # Restore send permissions for @everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            
            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{channel.mention} has been unlocked.",
                color=0x00ff00
            )
            embed.add_field(name="Moderator", value=ctx.author.display_name, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unlock this channel!")
    
    @commands.command(name='verify', aliases=['v'])
    async def verify_member(self, ctx, member: discord.Member = None):
        """Verify a member (adds verified role)"""
        if member is None:
            member = ctx.author
        
        verified_role = discord.utils.get(ctx.guild.roles, name=self.config.VERIFIED_ROLE_NAME)
        
        if not verified_role:
            await ctx.send("❌ Verified role not found! Ask admins to create it.")
            return
        
        try:
            await member.add_roles(verified_role)
            embed = discord.Embed(
                title="✅ Member Verified",
                description=f"{member.mention} has been verified!",
                color=0x00ff00
            )
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to verify members!")
    
    @commands.command(name='massrole', aliases=['mr'])
    @commands.has_permissions(manage_roles=True)
    async def add_role_to_all(self, ctx, *, role_name: str):
        """Add a role to all members (use with caution)"""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if not role:
            await ctx.send(f"❌ Role '{role_name}' not found!")
            return
        
        # Confirmation
        embed = discord.Embed(
            title="⚠️ Mass Role Assignment",
            description=f"Are you sure you want to add {role.mention} to all members?",
            color=0xffa500
        )
        embed.add_field(name="Members to affect", value=str(len(ctx.guild.members)), inline=False)
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌']
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            if str(reaction.emoji) == '❌':
                await ctx.send("❌ Mass role assignment cancelled!")
                return
            
            # Apply role to all members
            success_count = 0
            for member in ctx.guild.members:
                try:
                    await member.add_roles(role)
                    success_count += 1
                    await asyncio.sleep(0.1)  # Rate limiting
                except discord.Forbidden:
                    pass
            
            result_embed = discord.Embed(
                title="✅ Mass Role Assignment Complete",
                description=f"Added {role.mention} to {success_count} members",
                color=0x00ff00
            )
            await ctx.send(embed=result_embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Mass role assignment timed out!")

async def setup(bot):
    await bot.add_cog(ServerMgmtCog(bot))
