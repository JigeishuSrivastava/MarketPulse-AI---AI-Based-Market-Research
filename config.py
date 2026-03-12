import os
from groq import Groq
from dotenv import load_dotenv

# .env file se variables load karein
load_dotenv()

# Environment variable se key lein
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)