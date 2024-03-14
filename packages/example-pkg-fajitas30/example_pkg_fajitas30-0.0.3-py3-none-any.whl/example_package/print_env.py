from dotenv import load_dotenv
import os 

load_dotenv()
word =  os.getenv("TXT")
print(word)