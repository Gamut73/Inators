import os
from dataclasses import dataclass
from typing import List
from PIL import Image
from enum import Enum

from google import genai
from dotenv import load_dotenv

dotenv_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'local.env')
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = 'gemini-2.5-flash'


@dataclass
class LLMPrompt:
    action: str
    examples: List['LLMPromptExample']
    payload: str


class LLMPromptMediaType(Enum):
    IMAGE = 1
    VIDEO = 2


@dataclass
class LLMPromptMedia:
    media_path: str
    media_type: LLMPromptMediaType


@dataclass
class LLMMediaPrompt:
    action: str
    media: List[LLMPromptMedia]


@dataclass
class LLMPromptExample:
    input: str
    output: str


def make_llm_request_with_media(llm_media_prompt: 'LLMMediaPrompt', model: str = GEMINI_MODEL):
    client = genai.Client(api_key=GEMINI_API_KEY)
    images = []
    videos = []

    for media in llm_media_prompt.media:
        if media.media_type == LLMPromptMediaType.IMAGE:
            images.append(Image.open(media.media_path))
        elif media.media_type == LLMPromptMediaType.VIDEO:
            upload = client.files.upload(file=media.media_path)
            while upload.state != 'ACTIVE':
                upload = client.files.get(name=upload.name)
            if upload.state == 'ACTIVE':
                videos.append(upload)

    prompt_text = "Using the image attached, " + llm_media_prompt.action
    return client.models.generate_content(model=model, contents=[prompt_text] + images + videos).text


def make_llm_request(llm_prompt: 'LLMPrompt', model: str = GEMINI_MODEL):
    print(f"Gemini Api key is not None: {GEMINI_API_KEY is not None}")
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt_text = "For the payload below, " + llm_prompt.action + "\n Here are some examples:\n"
    for example in llm_prompt.examples:
        prompt_text += f"Input: {example.input}\nOutput: {example.output}\n"
    prompt_text += "\nHere is the payload:\n" + llm_prompt.payload
    return client.models.generate_content(model=model, contents=prompt_text).text


def _private_test_make_llm_image_request():
    prompt = LLMMediaPrompt(
        action="Retrieve the text from the following images with handwritten text and say what is happening in the video",
        media=[
            LLMPromptMedia(
                media_path=os.path.join(os.path.dirname(__file__), 'image0.jpg'),
                media_type=LLMPromptMediaType.IMAGE
            ),
            LLMPromptMedia(
                media_path=os.path.join(os.path.dirname(__file__), 'image1.png'),
                media_type=LLMPromptMediaType.IMAGE
            ),
            LLMPromptMedia(
                media_path=os.path.join(os.path.dirname(__file__), 'test.mp4'),
                media_type=LLMPromptMediaType.VIDEO
            )
        ]
    )
    response = make_llm_request_with_media(prompt)
    print(response)


def _private_test_make_llm_request():
    prompt = LLMPrompt(
        action="Translate the following English text to French.",
        examples=[
            LLMPromptExample(input="Hello, how are you?", output="Bonjour, comment ça va?"),
            LLMPromptExample(input="What is your name?", output="Quel est votre nom?")
        ],
        payload="I am a genius and nobody knows it but me."
    )
    response = make_llm_request(prompt)
    print(response)


if __name__ == "__main__":
    _private_test_make_llm_request()

