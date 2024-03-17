from .app import main
from .build import buildApp


def start() -> str:
    main()


def build():
    buildApp()
