from dotenv import load_dotenv
import os 

def return_secret(word):
    return word

load_dotenv()
word =  os.getenv("TXT")
return_secret(word)
print(word)


