import os
from datetime import datetime
import subprocess
from slugify import slugify

def generate_markdown(basedir, title, content):
    # Prepare the filename with the required Jekyll format (YYYY-MM-DD-title.md)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-")
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(basedir, filename)
    return generate_markdown_file(filepath, content)

def generate_markdown_file(filepath, content):
    # Write the file with front matter and content
    with open(filepath, 'w') as file:
        file.write("---\n")
        file.write(f"date: {datetime.now().isoformat()}\n")
        file.write("---\n\n")
        file.write(content)

    print(f"Generated {filepath}")
    return filepath

def git_commit_and_push(filename, commit_message="Add new post"):
    subprocess.run(['git', 'config', '--global', 'user.email', 'GithubAction@nowhere.com'])
    subprocess.run(['git', 'config', '--global', 'user.name', 'Github Action'])
    subprocess.run(['git', 'add', filename])
    subprocess.run(['git', 'commit', '-m', commit_message + ' [skip ci]'])
    subprocess.run(['git', 'push'])

# Example usage
# title = "My Second Post"
# content = "This is the content of my second post."

# Example usage
# path = generate_markdown("_posts", title, content)
# date_str = datetime.now().strftime("%Y-%m-%d")
# git_commit_and_push(path, "Added a new blog post")

def get_media():
    import json
    with open(os.path.join(os.path.dirname(__file__), '../media.json')) as f:
        return json.load(f)

def generate_media_markdown():
    media = get_media()
    markdown = ""
    for m in media:
        print(m)
        name = m["name"]
        url = m["url"]
        summary = m.get("summary", "No summary available")
        type = m["type"]
        author = m.get("author", "Unknown")
        markdown = markdown + f"## {name}\n\n[LINK]({url})\n\nType: {type}, Author: {author}\n\nSummary: {summary}\n\n"

        slug = slugify(name)

        if os.path.isfile(os.path.join(os.path.dirname(__file__), f'../media/{slug}.md')):
            markdown = markdown + f'[Link to full transcript]({slug}.md)\n\n'
    
    path = generate_markdown_file(
        os.path.join(os.path.dirname(__file__), '../media/media-list.md'),
        markdown)
    return git_commit_and_push(path, "Add new media post")

if __name__ == "__main__":
    generate_media_markdown()
