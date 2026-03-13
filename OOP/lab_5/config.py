import configparser

_config = configparser.ConfigParser()
_config.read("config.ini", encoding="utf-8")

USERS_FILE: str = _config.get("files", "users_file", fallback="users.json")
SESSION_FILE: str = _config.get("files", "session_file", fallback="session.json")
