import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration class"""
    
    # Discord Configuration
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN', '')
    DISCORD_CLIENT_ID: str = os.getenv('DISCORD_CLIENT_ID', '')
    BOT_PREFIX: str = os.getenv('BOT_PREFIX', '!')
    
    # Database Configuration
    MONGODB_URI: Optional[str] = os.getenv('MONGODB_URI')
    
    # API Keys
    STEAM_API_KEY: Optional[str] = os.getenv('STEAM_API_KEY')
    WEATHER_API_KEY: Optional[str] = os.getenv('WEATHER_API_KEY')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Gaming Configuration
    GAMING_ROLE_NAME: str = os.getenv('GAMING_ROLE_NAME', 'Gamer')
    NEW_MEMBER_ROLE_NAME: str = os.getenv('NEW_MEMBER_ROLE_NAME', 'Newcomer')
    VERIFIED_ROLE_NAME: str = os.getenv('VERIFIED_ROLE_NAME', 'Verified')
    
    # Moderation Settings
    AUTO_MODERATION: bool = os.getenv('AUTO_MODERATION', 'true').lower() == 'true'
    SPAM_PROTECTION: bool = os.getenv('SPAM_PROTECTION', 'true').lower() == 'true'
    BAD_WORDS_FILTER: bool = os.getenv('BAD_WORDS_FILTER', 'true').lower() == 'true'
    
    # Welcome/Goodbye Messages
    WELCOME_CHANNEL_ID: Optional[int] = int(os.getenv('WELCOME_CHANNEL_ID', '0')) if os.getenv('WELCOME_CHANNEL_ID') else None
    GOODBYE_CHANNEL_ID: Optional[int] = int(os.getenv('GOODBYE_CHANNEL_ID', '0')) if os.getenv('GOODBYE_CHANNEL_ID') else None
    
    # Bad words list for moderation
    BAD_WORDS = [
        # Add your server's specific bad words list here
        # This is just an example list
        'badword1', 'badword2', 'badword3', 'fuck', 'bitch', 'hore', 'swine'
    ]
    
    # Spam detection settings
    MAX_MESSAGES_PER_MINUTE: int = 10
    MAX_MESSAGE_LENGTH: int = 1000
    
    # Gaming commands settings
    DICE_SIDES: int = 6
    TRIVIA_QUESTIONS = [
        {"question": "What year was the first PlayStation released?", "answer": "1994"},
        {"question": "What is the most popular game of 2023?", "answer": "baldurs gate 3"},
        {"question": "Who created Minecraft?", "answer": "notch"},
        {"question": "What does RPG stand for?", "answer": "role playing game"},
        {"question": "What is the best selling game of all time?", "answer": "minecraft"},
    ]
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required in environment variables")
        return True
