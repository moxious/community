import logging
import json
import whisper
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")
log = logging.getLogger(__name__)

def summarize(text):
    client = OpenAI(
        api_key=config.get("OPENAI_API_KEY")
    )
    log.info("Summarizing transcript")
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    You are a helpful summarizer that reads audio transcripts and provides a simple summary. Please keep in mind
                    transcription errors are possible, and that you should account for these and ignore ums, ahs, and other filler words.

                    Your summaries should be no longer than a few sentences, and should not contain any bullet points but may contain
                    lists in prose.
                """
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        model="gpt-4o",
    )
    return completion.choices[0].message.content

def transcribe(video):
    log.info("Locating video: %s" % video)
    data = YouTube(video)

    log.info("Downloading audio stream")
    audio = data.streams.get_audio_only()
    path = audio.download()

    log.info("Transcribing audio")
    model = whisper.load_model("base")
    text = model.transcribe(path)
    return text

def process_video(url):
    text = transcribe(url)
    summary = summarize(text['text'])
    print("Summary: %s\n\nFull transcript:\n%s" % (summary, text['text']))
    combined = dict(text)
    combined["summary"] = summary
    combined["url"] = url

if __name__ == "__main__":
    process_video("https://youtu.be/KmrPkqrRIIE")

