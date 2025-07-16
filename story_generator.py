# story_generator.py

from io import BytesIO
import os
import logging
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from gtts import gTTS


def configure_api():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API Key not configured.")
    genai.configure(api_key=api_key)



def create_advanced_prompt(style: str) -> str:

    # --- Base prompt ---
    base_prompt = f"""
    **Your Persona:** You are a friendly and engaging storyteller. Your goal is to tell a story that is fun and easy to read.
    **Your Main Goal:** Write a story in simple, clear, and modern English.
    **Your Task:** Create one single story that connects all the provided images in order.
    **Style Requirement:** The story must fit the '{style}' genre.
    **Core Instructions:**
    1.  **Tell One Single Story:** Connect all images into a narrative with a beginning, middle, and end.
    2.  **Use Every Image:** Include a key detail from each image.
    3.  **Creative Interpretation:** Infer the relationships between the images.
    4.  **Nationality**: Use only Indian Names,Characters, Places , Persona Etc.
    **Output Format:**
    -   **Title:** Start with a simple and clear title.
    -   **Length:** The story must be between 4 and 5 paragraphs.
    """

    # --- Add Style-Specific Instructions ---
    style_instruction = ""
    if style == "Morale":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[MORAL]:` followed by the single-sentence moral of the story."
    elif style == "Mystery":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[SOLUTION]:` that reveals the culprit and the key clue."
    elif style == "Thriller":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[TWIST]:` that reveals a final, shocking twist."

    return base_prompt + style_instruction




def generate_story_from_images(images: List[Image.Image], style: str) -> str:

    # This function now expects PIL Image objects directly
    if not 1 <= len(images) <= 10:
        error_msg = "Validation Error: Please provide between 1 and 10 images."
        logging.error(error_msg)
        return error_msg

    try:
        configure_api()  # Configure API every time to ensure it's set
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt_text = create_advanced_prompt(style)

        prompt_parts = [prompt_text] + images

        logging.info("Generating story with Gemini API...")
        response = model.generate_content(prompt_parts)

        if response.parts:
            story = response.text
            return story
        else:
            error_msg = "API Error: The model returned no content. This might be due to safety filters."
            return error_msg

    except ValueError as ve:  # Catch the specific API key configuration error
        logging.error(str(ve))
        return str(ve)
    except Exception as e:
        error_msg = f"An unexpected error occurred during the API call: {e}"
        return error_msg



def narrate_story(story_text: str) -> BytesIO:
    try:
        tts = gTTS(text=story_text, lang='en', slow=False)
        audio_fp = BytesIO()  # This line requires the import
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        error_msg = f"An unexpected error occurred during the API call: {e}"
        return error_msg
