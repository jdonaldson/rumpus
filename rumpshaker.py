import rumps
import argparse

class CustomTextApp(rumps.App):
    def __init__(self, text):
        super(CustomTextApp, self).__init__(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a menubar app with custom text")
    parser.add_argument("text", type=str, help="Text to display in the menubar")
    args = parser.parse_args()

    CustomTextApp(args.text).run()
