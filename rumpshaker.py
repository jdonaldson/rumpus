import rumps

class HelloWorldApp(rumps.App):
    def __init__(self):
        super(HelloWorldApp, self).__init__("Hello World")

if __name__ == "__main__":
    HelloWorldApp().run()
