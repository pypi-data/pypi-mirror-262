from nicegui import ui, native


def run():
    ui.label("Hello, world!")
    ui.button("Click me")


def run_web():
    run()
    ui.run()


def run_native():
    run()
    ui.run(native=True, reload=False)
