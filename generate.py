from dotenv import load_dotenv
import os
import requests
from google import genai
from google.genai import types
import io
import hashlib

TEMPERATURE = 0.3
GEMINI_TEXT_MODEL = "gemini-2.5-flash-lite" 
GEMINI_IMAGE_MODEL = "imagen-3.0-generate-002"
IMAGE_PATH = "./images/"

load_dotenv()
PROMPTLAYER_API_KEY = os.environ["PROMPTLAYER_API_KEY"]
PROMPT_TEMPLATE_IDENTIFIER = os.environ["PROMPT_TEMPLATE_IDENTIFIER"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["REGION"]

client = genai.Client(api_key = GEMINI_API_KEY)

def get_prompt():
  
    url = f"https://api.promptlayer.com/prompt-templates/{PROMPT_TEMPLATE_IDENTIFIER}"
    headers = {
        "X-API-KEY": PROMPTLAYER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers = headers)
    response.raise_for_status()
    data = response.json()
    
    messages = data.get("prompt_template", {}).get("messages", {})

    system_prompt = ""
    user_prompt = ""
    for m in messages:
        if m.get("role", {}) == "system":
            system_prompt = m.get("content", [])[0].get("text", "")
        if m.get("role", {}) == "user":
            user_prompt = m.get("content", [])[0].get("text", "")

    if not system_prompt or not user_prompt:
        raise ValueError("System or User prompt not found in the PromptLayer response.")

    return system_prompt, user_prompt

def create_image_prompt_with_LLM(user_prompt, system_prompt):

    try:
        response = client.models.generate_content(
            model = GEMINI_TEXT_MODEL,
            contents = user_prompt,
            config = types.GenerateContentConfig(
            system_instruction = system_prompt,
            temperature = TEMPERATURE, 
        )
    )

        return response.text
    except Exception as e:
        print(f"Error: {e}")

        return

def generate_image_prompt(details, category):

    system_prompt, user_prompt = get_prompt()
    user_prompt_updated = user_prompt.format(details = details, category = category)
    image_prompt = create_image_prompt_with_LLM(user_prompt_updated, system_prompt)

    return image_prompt

def generate_image_with_LLM(details, category):

    try:
        prompt = generate_image_prompt(details, category)
        print(prompt)
        client = genai.Client(
            vertexai = True, project = PROJECT_ID, location = LOCATION
        )

        response = client.models.generate_images(
            model = GEMINI_IMAGE_MODEL,
            prompt = prompt,
            config = types.GenerateImagesConfig(
                number_of_images = 1,
                aspect_ratio = "1:1",
                output_mime_type='image/jpeg',
            )
        )
      
        return response.generated_images
    except Exception as e:
        print(f"Error: {e}")

        return

def save_image(image, unique_id):

    try:
        image_bytes_io = io.BytesIO()
        image_bytes_io.write(image.image.image_bytes)
        image_bytes_io.seek(0)
        raw_bytes = image_bytes_io.getvalue()
        path = os.path.join(IMAGE_PATH, f'{unique_id}.jpg')

        with open(path, "wb") as f:
            f.write(raw_bytes)
    except Exception as e:
        print(f"Error: {e}")

        return

def create_hash_for_image(details):
    """Unique identifier for each image based on details"""

    hasher = hashlib.sha256()
    hasher.update(details.encode('utf-8'))
    unique_id = hasher.hexdigest()

    return unique_id

def run_generate_pipeline(details, category, unique_id):
    
    images = generate_image_with_LLM(details, category)
    save_image(images[0], unique_id)

    return images[0]