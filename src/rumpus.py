import rumps
import argparse
import os
import emoji
import subprocess
import re

class EmojiCountApp(rumps.App):
    def __init__(self, directory, file_types):
        super(EmojiCountApp, self).__init__("Code Check")
        self.directory = directory
        self.file_types = file_types
        self.emoji_counts = {}
        self.emoji_files = {}
        self.file_paths = {}
        self.phrase_to_emoji = {
            "TODO": "📝",
            "FIXME": "🔧",
            "XXX": "⚠️",
            "HACK": "💻",
            "BUG": "🐛",
            "NOTE": "📌"
        }
        self.update_counts()

    def update_counts(self):
        self.emoji_counts = {}
        self.emoji_files = {}
        self.file_paths = {}
        for root, _, files in os.walk(self.directory):
            for file in files:
                if any(file.endswith(ft) for ft in self.file_types):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.count_emojis(content, file)
                        self.count_phrases(content, file)
                    self.file_paths[file] = file_path
        self.update_menu()

    def count_emojis(self, content, file):
        emojis = emoji.emoji_list(content)
        for emoji_dict in emojis:
            e = emoji_dict['emoji']
            self.update_counts_and_files(e, file)

    def count_phrases(self, content, file):
        for phrase, e in self.phrase_to_emoji.items():
            count = len(re.findall(r'\b' + re.escape(phrase) + r'\b', content))
            if count > 0:
                self.update_counts_and_files(e, file, count)

    def update_counts_and_files(self, e, file, count=1):
        self.emoji_counts[e] = self.emoji_counts.get(e, 0) + count
        if e not in self.emoji_files:
            self.emoji_files[e] = set()
        self.emoji_files[e].add(file)

    def update_menu(self):
        self.menu.clear()
        for e, count in self.emoji_counts.items():
            emoji_menu = rumps.MenuItem(f"{e} ({count})")
            for file in self.emoji_files[e]:
                emoji_menu.add(rumps.MenuItem(file, callback=self.open_file))
            self.menu.add(emoji_menu)
        self.menu.add(rumps.MenuItem('Refresh', callback=self.refresh))
        self.update_title()

    def update_title(self):
        title = " ".join([f"{e}{c}" for e, c in self.emoji_counts.items()])
        self.title = title[:25] + "..." if len(title) > 28 else title

    @rumps.clicked('Refresh')
    def refresh(self, _):
        self.update_counts()

    def open_file(self, sender):
        file_path = self.file_paths[sender.title]
        subprocess.run(['open', file_path])

def main():
    parser = argparse.ArgumentParser(description="Count emojis and code phrases in files")
    parser.add_argument("--directory", type=str, help="Directory to search for files")
    parser.add_argument("--file_types", nargs='+', help="File types to include (e.g. .py .js)")
    args = parser.parse_args()

    app = EmojiCountApp(args.directory, args.file_types)
    app.run()

if __name__ == "__main__":
    main()
