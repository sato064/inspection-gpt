from dotenv import load_dotenv
import os
load_dotenv()

print("Hello dev!!!")
print(os.getenv("OPENAI_KEY"))

hi