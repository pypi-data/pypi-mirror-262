import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from halo import Halo
import click
import requests
import json
from requests import get
from uuid import uuid4
from re import findall
from requests.exceptions import RequestException
from curl_cffi.requests import get, RequestsError
import g4f
from random import randint
from PIL import Image
import io

#------------------------------------------------------phind--------------------------------------------------------   
class PhindSearch:
    def __init__(self, query):
        self.query = query
        self.url = "https://www.phind.com/search?q=" + self.query
        self.chrome_options = Options()
        self.chrome_options.add_argument("--log-level=3")  # Fatal errors only
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def search(self):
        try:
            spinner = Halo("Getting Answer from Phind...\n\n\n\n\n\n\n \n", spinner="dots")
            spinner.start()

            self.driver.get(self.url)

            WebDriverWait(self.driver, timeout=50).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(15)
            answer_elements = self.driver.find_elements(By.CSS_SELECTOR, "main div.fs-5")

            paragraph_texts = [answer_element.text.strip() for answer_element in answer_elements]

            for text in paragraph_texts:
                spinner.stop()
                return text

        finally:
            self.driver.quit()

    def close(self):
        self.driver.quit()

    @staticmethod
    def search_cli(query):
        """Use webscout.AI."""
        search_instance = PhindSearch(query)
        search_instance.search()
#------------------------------------------------------yep.com--------------------------------------------------------   
class YepChat:
    def __init__(self, message="hello"):
        self.url = "https://api.yep.com/v1/chat/completions"
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/json; charset=utf-8",
            "Origin": "https://yep.com",
            "Referer": "https://yep.com/",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT   10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0.0.0 Safari/537.36"
        }
        self.payload = {
            "stream": True,
            "max_tokens":   1280,
            "top_p":   0.7,
            "temperature":   0.6,
            "messages": [{
                "content": message,
                "role": "user"
            }],
            "model": "Mixtral-8x7B-Instruct-v0.1"
        }

    def send_request(self):
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.payload), stream=True)
        print(response.status_code)
        return response

    def process_response(self, response):
        myset = ""
        for line in response.iter_lines():
            if line:
                myline = line.decode('utf-8').removeprefix("data: ").replace(" null", "False")
                try:
                    myval = eval(myline)
                    if "choices" in myval and "delta" in myval["choices"][0] and "content" in myval["choices"][0]["delta"]:
                        myset += myval["choices"][0]["delta"]["content"]
                except:
                    continue
        return myset

    @staticmethod
    def chat_cli(message):
        """Sends a request to the Yep API and processes the response."""
        yep_chat = YepChat(message=message)
        response = yep_chat.send_request()
        processed_response = yep_chat.process_response(response)
        print(processed_response)
#------------------------------------------------------youchat--------------------------------------------------------   
class youChat:
    """
    This class provides methods for generating completions based on prompts.
    """
    def create(self, prompt):
        """
        Generate a completion based on the provided prompt.

        Args:
            prompt (str): The input prompt to generate a completion from.

        Returns:
            str: The generated completion as a text string.

        Raises:
            Exception: If the response does not contain the expected "youChatToken".
        """
        resp = get(
            "https://you.com/api/streamingSearch",
            headers={
                "cache-control": "no-cache",
                "referer": "https://you.com/search?q=gpt4&tbm=youchat",
                "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            },
            params={
                "q": prompt,
                "page": 1,
                "count": 10,
                "safeSearch": "Off",
                "onShoppingPage": False,
                "mkt": "",
                "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
                "domain": "youchat",
                "queryTraceId": str(uuid4()),
                "chat": [],
            },
            impersonate="chrome107",
        )
        if "youChatToken" not in resp.text:
            raise RequestsError("Unable to fetch the response.")
        return (
            "".join(
                findall(
                    r"{\"youChatToken\": \"(.*?)\"}",
                    resp.content.decode("unicode-escape"),
                )
            )
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
        )

    @staticmethod
    def chat_cli(prompt):
        """Generate completion based on the provided prompt"""
        you_chat = youChat()
        completion = you_chat.create(prompt)
        print(completion)
#------------------------------------------------------Gemini--------------------------------------------------------        
class Gemini:
    def __init__(self):
        self.messages = []

    def chat(self, *args):
        assert args != ()

        message = " ".join(args)
        self.messages.append({"role": "user", "content": message})

        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            provider=g4f.Provider.Gemini,
            messages=self.messages,
            stream=True,
        )
        ms = ""
        for message in response:
            ms += message
        self.messages.append({"role": "assistant", "content": ms.strip()}) # Strip whitespace from the message content
        return ms.strip() # Return the message without trailing whitespace

    @staticmethod
    def chat_cli(message):
        """Generate completion based on the provided message"""
        gemini = Gemini()
        return gemini.chat(message)
#------------------------------------------------Prodia-------------------------------------------------------------------------
class Prodia:
    """
    This class provides methods for generating images based on prompts.
    """

    def create(self, prompt):
        """
        Create a new image generation based on the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            resp: The generated image content
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
        }
        try:
            resp = get(
                "https://api.prodia.com/generate",
                params={
                    "new": "true",
                    "prompt": prompt,
                    "model": "dreamshaper_6BakedVae.safetensors [114c8abb]",
                    "negative_prompt": "(nsfw:1.5),verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.5),cross-eyed,sketches, (worst quality:2), (low quality:2.1), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry, bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, extra arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers, missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, repeating hair",
                    "steps": "50",
                    "cfg": "9.5",
                    "seed": randint(1, 10000),
                    "sampler": "Euler",
                    "aspect_ratio": "square",
                },
                headers=headers,
                timeout=30,
            )
            data = resp.json()
            while True:
                resp = get(f"https://api.prodia.com/job/{data['job']}", headers=headers)
                json = resp.json()
                if json["status"] == "succeeded":
                    return get(
                        f"https://images.prodia.xyz/{data['job']}.png?download=1",
                        headers=headers,
                    ).content
        except RequestException as exc:
            raise RequestException("Unable to fetch the response.") from exc

    @staticmethod
    def prodia_cli(prompt):
        """Generate an image based on the provided prompt."""
        generator = Prodia()
        try:
            image_content = generator.create(prompt)
            # Save the image content to a file
            with open('generated_image.png', 'wb') as f:
                f.write(image_content)
            print("Image generated successfully and saved as generated_image.png")
            
            # Open the image file and display it
            image = Image.open('generated_image.png')
            image.show()
        except Exception as e:
            print(f"An error occurred: {e}")
#-------------------------------------------------------Pollination--------------------------------------------------------------------------------------
class Pollinations:
    """
    This class provides methods for generating images based on prompts.
    """

    def create(self, prompt):
        """
        Create a new image generation based on the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            resp: The generated image content
        """
        try:
            return get(
                url=f"https://image.pollinations.ai/prompt/{prompt}{randint(1, 10000)}",
                timeout=30,
            ).content
        except RequestException as exc:
            raise RequestException("Unable to fetch the response.") from exc

    @staticmethod
    def pollinations_cli(prompt):
        """Generate an image based on the provided prompt."""
        generator = Pollinations()
        try:
            image_content = generator.create(prompt)
            # Save the image content to a file
            with open('generated_image.png', 'wb') as f:
                f.write(image_content)
            print("Image generated successfully and saved as generated_image.png")
            
            # Open the image file and display it
            image = Image.open('generated_image.png')
            image.show()
        except Exception as e:
            print(f"An error occurred: {e}")

@click.group()
def cli():
    pass

@cli.command()
@click.option('--query', prompt='Enter your search query', help='The query to search.')
def phindsearch(query):
    PhindSearch.search_cli(query)

@cli.command()
@click.option('--message', prompt='Enter your message', help='The message to send.')
def yepchat(message):
    YepChat.chat_cli(message)

@cli.command()
@click.option('--prompt', prompt='Enter your prompt', help='The prompt to generate a completion from.')
def youchat(prompt):
    youChat.chat_cli(prompt)

@cli.command()
@click.option('--message', prompt='Enter your message', help='The message to send.')
def gemini(message):
    Gemini.chat_cli(message)
@cli.command()
@click.option('--prompt', prompt='Enter your prompt', help='The prompt for generating the image.')
def prodia(prompt):
    """Generate an image based on the provided prompt."""
    Prodia.prodia_cli(prompt)
@cli.command()
@click.option('--prompt', prompt='Enter your prompt', help='The prompt for generating the image.')
def pollinations(prompt):
    """Generate an image based on the provided prompt."""
    Pollinations.pollinations_cli(prompt)
if __name__ == '__main__':
    cli()
