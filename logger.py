def setup_logging(verbose: bool = False) -> None:
    LOG_DIRECTORY = os.path.expanduser('~/.config/luminos/logs')
    LOG_FILE = os.path.join(LOG_DIRECTORY, 'luminos.log')

    os.makedirs(LOG_DIRECTORY, exist_ok=True)  # Ensure log directory exists

    file_handler = logging.FileHandler(LOG_FILE)
    console_handler = logging.StreamHandler()

    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)