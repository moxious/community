import logging
import json
import whisper
import os
import sys
from pytubefix import YouTube
from pytubefix.cli import on_progress
from openai import OpenAI
from dotenv import dotenv_values
from slugify import slugify

config = dotenv_values(".env")
log = logging.getLogger(__name__)

def get_media():
    import json
    with open(os.path.join(os.path.dirname(__file__), '../../media.json')) as f:
        return json.load(f)

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

    metadata = {}
    title = data.title
    metadata['title'] = title

    log.info("Downloading audio stream")
    audio = data.streams.get_audio_only()
    path = audio.download()

    log.info("Transcribing audio")
    model = whisper.load_model("base")
    text = model.transcribe(path)
    return (text, metadata)

def process_video(url):
    (text, metadata) = transcribe(url)
    summary = summarize(text['text'])
    print("Summary: %s\n\nFull transcript:\n%s" % (summary, text['text']))
    combined = dict(text)
    combined["summary"] = summary
    combined["url"] = url
    combined["title"] = metadata["title"]
    return combined

def markdownize(combined_data):
    return f"""## {combined_data["title"]}
[Link to asset]({combined_data["url"]})

### Summary

{combined_data["summary"]}

### Full Transcript (whisper)

{combined_data["text"]}
    """

def json_path(slug):
    return os.path.join(os.path.dirname(__file__), '../../media/') + slug + ".json"

def markdown_path(slug):
    return os.path.join(os.path.dirname(__file__), '../../media/') + slug + ".md"

def write_files(combined_data):
    json_file = json_path(combined_data["slug"])
    md = markdown_path(combined_data["slug"])
    
    with open(json_file, 'w') as f:
        f.write(json.dumps(combined_data, indent=2))
    
    with open(md, 'w') as f:
        f.write(markdownize(combined_data))

if __name__ == "__main__":
    media = get_media()

    for m in media:
        slug = slugify(m['name'])

        if os.path.isfile(json_path(slug)) and os.path.isfile(markdown_path(slug)):
            log.info("Skipping %s, already processed" % slug)

        if m['type'] != "video":
            log.info("Skipping %s, not a video" % slug)
            continue

        log.info("Processing new video %s => %s" % (slug, m['url']))
        combined_data = process_video(m['url'])
        combined_data["slug"] = slug
        write_files(combined_data)

