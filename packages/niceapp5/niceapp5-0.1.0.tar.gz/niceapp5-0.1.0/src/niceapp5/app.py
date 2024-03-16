from nicegui import ui


def run():
    ui.label("Hello, world!")
    ui.button("Click me")


def main():
    run()
    ui.run(native=True, reload=False)
