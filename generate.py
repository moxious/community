import os
from datetime import datetime
import subprocess

def generate_markdown(title, content):
    # Prepare the filename with the required Jekyll format (YYYY-MM-DD-title.md)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-")
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join('_posts', filename)

    # Write the file with front matter and content
    with open(filepath, 'w') as file:
        file.write(f"---\n")
        file.write(f"title: \"{title}\"\n")
        file.write(f"date: {datetime.now().isoformat()}\n")
        file.write(f"layout: post\n")
        file.write(f"---\n\n")
        file.write(content)

    print(f"Generated {filename}")

def git_commit_and_push(filename, commit_message="Add new post"):
    subprocess.run(['git', 'add', filename])
    subprocess.run(['git', 'commit', '-m', commit_message + ' [skip ci]'])
    subprocess.run(['git', 'push'])

# Example usage
title = "My New Post"
content = "This is the content of my new post."
slug = 'first'
generate_markdown(title, content)

# Example usage
generate_markdown(title, content)
date_str = datetime.now().strftime("%Y-%m-%d")
git_commit_and_push(f'_posts/{date_str}-{slug}.md', "Added a new blog post")
