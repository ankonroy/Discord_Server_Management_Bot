import discord
from discord.ext import commands
import random
import asyncio
import json
from datetime import datetime
from config import Config

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config
        
    @commands.command(name='roll', aliases=['dice', 'r'])
    async def roll_dice(self, ctx, sides: int = 6):
        """Roll a dice with specified number of sides"""
        if sides < 2 or sides > 100:
            await ctx.send("❌ Dice must have between 2 and 100 sides!")
            return
        
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"**{ctx.author.display_name}** rolled a **{sides}-sided dice**!",
            color=0x00ff00
        )
        embed.add_field(name="Result", value=f"**{result}**", inline=False)
        embed.add_field(name="Sides", value=sides, inline=True)
        embed.set_thumbnail(url="https://i.imgur.com/8R6jEnQ.gif")
        embed.timestamp = datetime.utcnow()
        
        # Add some fun reactions
        if result == sides:
            embed.add_field(name="🎉 Jackpot!", value="Maximum roll! You're on fire!", inline=False)
        elif result == 1:
            embed.add_field(name="😢 Unlucky!", value="Better luck next time!", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='8ball', aliases=['8b', 'fortune'])
    async def eight_ball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
            "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
            "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Very doubtful."
        ]
        
        response = random.choice(responses)
        
        embed = discord.Embed(
            title="🔮 Magic 8-Ball",
            description=f"**Question:** {question}",
            color=0x4b0082
        )
        embed.add_field(name="Answer", value=f"**{response}**", inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/7AJf0sX.png")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='coinflip', aliases=['flip', 'coin'])
    async def coin_flip(self, ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙' if result == 'Heads' else '💰'
        
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"**{ctx.author.display_name}** flipped a coin!",
            color=0xffd700
        )
        embed.add_field(name="Result", value=f"{emoji} **{result}**", inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='randomuser', aliases=['randuser', 'pick'])
    async def random_user(self, ctx):
        """Pick a random online member"""
        online_members = [member for member in ctx.guild.members if member.status == discord.Status.online and not member.bot]
        
        if not online_members:
            await ctx.send("❌ No online members found!")
            return
        
        chosen_member = random.choice(online_members)
        
        embed = discord.Embed(
            title="🎯 Random User",
            description=f"**{chosen_member.mention}** has been chosen!",
            color=0x00ff00
        )
        embed.set_thumbnail(url=chosen_member.avatar.url if chosen_member.avatar else chosen_member.default_avatar.url)
        embed.add_field(name="User", value=chosen_member.display_name, inline=True)
        embed.add_field(name="Status", value=str(chosen_member.status).title(), inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='trivia', aliases=['quiz'])
    async def trivia(self, ctx, difficulty: str = 'easy'):
        """Start a trivia game"""
        difficulty = difficulty.lower()
        if difficulty not in ['easy', 'medium', 'hard']:
            await ctx.send("❌ Difficulty must be: easy, medium, or hard!")
            return
        
        # Get a random question
        question_data = random.choice(self.config.TRIVIA_QUESTIONS)
        question = question_data["question"]
        answer = question_data["answer"].lower()
        
        embed = discord.Embed(
            title="🧠 Trivia Time!",
            description=f"**Difficulty:** {difficulty.title()}",
            color=0x1e90ff
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="💡 Hint", value="React with ✅ when you think you know the answer!", inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/ZN3sZqX.png")
        embed.timestamp = datetime.utcnow()
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        
        def check(reaction, user):
            return (user == ctx.author and 
                    str(reaction.emoji) == '✅' and 
                    reaction.message.id == message.id)
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            # Ask for answer
            await ctx.send(f"{ctx.author.mention} What is your answer?")
            
            def answer_check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            try:
                answer_msg = await self.bot.wait_for('message', timeout=30.0, check=answer_check)
                user_answer = answer_msg.content.lower().strip()
                
                if user_answer in answer or answer in user_answer:
                    result_embed = discord.Embed(
                        title="🎉 Correct!",
                        description=f"**{ctx.author.display_name}** got it right!",
                        color=0x00ff00
                    )
                    result_embed.add_field(name="Answer", value=question_data["answer"], inline=False)
                else:
                    result_embed = discord.Embed(
                        title="❌ Incorrect",
                        description=f"**{ctx.author.display_name}** got it wrong!",
                        color=0xff0000
                    )
                    result_embed.add_field(name="Correct Answer", value=question_data["answer"], inline=False)
                    result_embed.add_field(name="Your Answer", value=answer_msg.content, inline=False)
                
                await ctx.send(embed=result_embed)
                
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} Time's up! The answer was: **{question_data['answer']}**")
                
        except asyncio.TimeoutError:
            await ctx.send("⏰ Trivia timed out!")
    
    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rock_paper_scissors(self, ctx, choice: str):
        """Play rock, paper, scissors"""
        choice = choice.lower()
        valid_choices = ['rock', 'paper', 'scissors']
        
        if choice not in valid_choices:
            await ctx.send("❌ Please choose: rock, paper, or scissors!")
            return
        
        bot_choice = random.choice(valid_choices)
        
        # Determine winner
        if choice == bot_choice:
            result = "🤝 It's a tie!"
            color = 0xffa500
        elif (choice == 'rock' and bot_choice == 'scissors') or \
             (choice == 'paper' and bot_choice == 'rock') or \
             (choice == 'scissors' and bot_choice == 'paper'):
            result = "🎉 You win!"
            color = 0x00ff00
        else:
            result = "😢 You lose!"
            color = 0xff0000
        
        # Get emojis
        emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        
        embed = discord.Embed(
            title="✊✋✌️ Rock, Paper, Scissors",
            description=f"**{ctx.author.display_name}** vs **Bot**",
            color=color
        )
        embed.add_field(name=f"{ctx.author.display_name}", value=f"{emojis[choice]} {choice.title()}", inline=True)
        embed.add_field(name="Bot", value=f"{emojis[bot_choice]} {bot_choice.title()}", inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='meme', aliases=['funny'])
    async def meme(self, ctx):
        """Get a random gaming meme"""
        memes = [
            "When you finally beat that impossible boss after 50 attempts 😂",
            "Loading screens: where gaming goes to die",
            "That moment when your friend says 'It's just one more game'",
            "Me: Just one more level... 6 hours later:",
            "When the server crashes during a raid",
            "Gaming addiction level: Professional",
            "Me trying to explain to my mom why I need a $3000 PC",
            "When someone says console gaming is better",
            "That feeling when you find a legendary item",
            "Me pretending I know what I'm doing in ranked"
        ]
        
        meme = random.choice(memes)
        
        embed = discord.Embed(
            title="😂 Random Gaming Meme",
            description=meme,
            color=0xff69b4
        )
        embed.set_thumbnail(url="https://i.imgur.com/8Jm6nGx.gif")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='compliment', aliases=['praise'])
    async def compliment(self, ctx, member: discord.Member = None):
        """Give a random compliment"""
        if member is None:
            member = ctx.author
        
        compliments = [
            "You're an amazing gamer! 🎮",
            "Your skills are legendary! 🏆",
            "You bring joy to this server! 😊",
            "You're a fantastic friend! ❤️",
            "Your positive energy is contagious! ✨",
            "You're one of a kind! 🌟",
            "You make this community better! 🎯",
            "Your dedication is inspiring! 💪",
            "You're a true gaming champion! 👑",
            "You have great taste in games! 🎲"
        ]
        
        compliment = random.choice(compliments)
        
        embed = discord.Embed(
            title="💝 Compliment",
            description=f"{member.mention}, {compliment}",
            color=0xff1493
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='dicegame', aliases=['dg'])
    async def dice_game(self, ctx, bet: int = 100):
        """Play a dice game (virtual currency)"""
        # This is just for fun - no real gambling involved
        player_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)
        
        if player_roll > bot_roll:
            result = "🎉 You win!"
            color = 0x00ff00
        elif player_roll < bot_roll:
            result = "😢 You lose!"
            color = 0xff0000
        else:
            result = "🤝 It's a tie!"
            color = 0xffa500
        
        embed = discord.Embed(
            title="🎲 Dice Game",
            description=f"Bet: {bet} virtual points",
            color=color
        )
        embed.add_field(name=f"{ctx.author.display_name}", value=f"🎲 {player_roll}", inline=True)
        embed.add_field(name="Bot", value=f"🎲 {bot_roll}", inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='slots', aliases=['slotmachine'])
    async def slots(self, ctx, bet: int = 100):
        """Play a virtual slot machine"""
        symbols = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎']
        
        # Generate 3 spins
        spin1 = random.choice(symbols)
        spin2 = random.choice(symbols)
        spin3 = random.choice(symbols)
        
        # Determine payout
        if spin1 == spin2 == spin3:
            result = "🎉 JACKPOT!"
            color = 0xffd700
            payout = bet * 10
        elif spin1 == spin2 or spin2 == spin3 or spin1 == spin3:
            result = "🎊 Winner!"
            color = 0x00ff00
            payout = bet * 2
        else:
            result = "😢 No match!"
            color = 0xff0000
            payout = 0
        
        embed = discord.Embed(
            title="🎰 Slot Machine",
            description=f"Bet: {bet} virtual points",
            color=color
        )
        embed.add_field(name="Result", value=f"{spin1} {spin2} {spin3}", inline=False)
        embed.add_field(name="Outcome", value=result, inline=False)
        if payout > 0:
            embed.add_field(name="Payout", value=f"+{payout} points", inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar', aliases=['pfp'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Display user's avatar"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=0x00ff00
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCog(bot))
