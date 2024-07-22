import rumps
import argparse
import os
import emoji

class EmojiCountApp(rumps.App):
    def __init__(self, directory, file_types):
        super(EmojiCountApp, self).__init__("Emoji Count")
        self.directory = directory
        self.file_types = file_types
        self.emoji_counts = {}
        self.update_emoji_counts()

    def update_emoji_counts(self):
        self.emoji_counts = {}
        for file in os.listdir(self.directory):
            if any(file.endswith(ft) for ft in self.file_types):
                file_path = os.path.join(self.directory, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    emojis = emoji.emoji_list(content)
                    for emoji_dict in emojis:
                        e = emoji_dict['emoji']
                        self.emoji_counts[e] = self.emoji_counts.get(e, 0) + 1
        self.update_title()

    def update_title(self):
        title = " ".join([f"{e}{c}" for e, c in self.emoji_counts.items()])
        self.title = title[:25] + "..." if len(title) > 28 else title

    @rumps.clicked('Refresh')
    def refresh(self, _):
        self.update_emoji_counts()

    @rumps.clicked('Show Details')
    def show_details(self, _):
        details = "\n".join([f"{e}: {c}" for e, c in self.emoji_counts.items()])
        rumps.Window(message=details, title="Emoji Counts", default_text="", ok="OK").run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count emojis in files of specific types in a directory")
    parser.add_argument("directory", type=str, help="Directory to search for files")
    parser.add_argument("file_types", nargs='+', help="File types to include (e.g. .txt .md)")
    args = parser.parse_args()

    app = EmojiCountApp(args.directory, args.file_types)
    app.run()
