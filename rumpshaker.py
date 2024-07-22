import rumps
import argparse
import os
import emoji
import subprocess

class EmojiCountApp(rumps.App):
    def __init__(self, directory, file_types):
        super(EmojiCountApp, self).__init__("Emoji Count")
        self.directory = directory
        self.file_types = file_types
        self.emoji_counts = {}
        self.emoji_files = {}
        self.update_emoji_counts()

    def update_emoji_counts(self):
        self.emoji_counts = {}
        self.emoji_files = {}
        for file in os.listdir(self.directory):
            if any(file.endswith(ft) for ft in self.file_types):
                file_path = os.path.join(self.directory, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    emojis = emoji.emoji_list(content)
                    for emoji_dict in emojis:
                        e = emoji_dict['emoji']
                        self.emoji_counts[e] = self.emoji_counts.get(e, 0) + 1
                        if e not in self.emoji_files:
                            self.emoji_files[e] = set()
                        self.emoji_files[e].add(file_path)
        self.update_menu()

    def update_menu(self):
        self.menu.clear()
        for e, count in self.emoji_counts.items():
            emoji_menu = rumps.MenuItem(f"{e} ({count})")
            for file_path in self.emoji_files[e]:
                file_name = os.path.basename(file_path)
                emoji_menu.add(rumps.MenuItem(file_name, callback=self.open_file))
            self.menu.add(emoji_menu)
        self.menu.add(rumps.MenuItem('Refresh', callback=self.refresh))
        self.update_title()

    def update_title(self):
        title = " ".join([f"{e}{c}" for e, c in self.emoji_counts.items()])
        self.title = title[:25] + "..." if len(title) > 28 else title

    @rumps.clicked('Refresh')
    def refresh(self, _):
        self.update_emoji_counts()

    def open_file(self, sender):
        file_path = next(path for path in self.emoji_files[sender.parent.title[0]] if sender.title in path)
        subprocess.run(['open', file_path])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count emojis in files of specific types in a directory")
    parser.add_argument("directory", type=str, help="Directory to search for files")
    parser.add_argument("file_types", nargs='+', help="File types to include (e.g. .txt .md)")
    args = parser.parse_args()

    app = EmojiCountApp(args.directory, args.file_types)
    app.run()
