import os
import time
from rich.console import Console
from rich.markdown import Markdown
from google.generativeai import GenerativeModel, configure
from dotenv import load_dotenv

# config
load_dotenv()
key = os.getenv('GOOGLE_API_KEY')
configure(api_key=key)


def to_markdown(text):
    console = Console()
    console.print(Markdown(text))


model = GenerativeModel('gemini-pro')
print(to_markdown(model.generate_content("Present yourself as Gemini AI in 20 words").text))
while True:
    user_input = str(input("Write 0 or press Ctrl + C to exit.\nPrompt:"))
    if user_input == '0':
        print('Bye.')
        break
    else:
        start = time.time()
        response = model.generate_content(user_input)
        print(to_markdown(response.text))
        print(f'Total time of response: {time.time() - start}\n')
