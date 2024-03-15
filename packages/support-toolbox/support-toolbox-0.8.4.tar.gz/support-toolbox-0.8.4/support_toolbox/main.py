from support_toolbox.app_handler.app import start_app
from support_toolbox.app_handler.auto_updater import check_for_updates
import app_version


def main():
    check_for_updates(app_version.__version__)
    start_app()


if __name__ == "__main__":
    main()
