import subprocess
from pathlib import Path
from textwrap import dedent

from django.utils.crypto import get_random_string


def _create_settings_file(settings: dict[str, str]) -> None:
    data: str = dedent(
        f"""
        [settings]
        DEBUG = True
        SECRET_KEY = {get_random_string(32)}
        ALLOWED_HOSTS = *
        DATABASE_URL = {settings['db_url']}
        LOG_FILE_PATH = {settings['log_file_path']}
        STATIC_ROOT_BASE = {settings['static_root_base']}
        MEDIA_ROOT_BASE = {settings['media_root_base']}
    """
    ).strip()
    with open(
        Path.cwd()
        / settings["project_dir"]
        / settings["project_name"]
        / "settings/settings.ini",
        "w",
    ) as f:
        f.write(data)


def _create_project(project_dir: str, project_name: str) -> None:
    """Create the wagtail project."""
    project_path: Path = Path.cwd() / project_dir
    project_path.mkdir()
    template_path: Path = Path(__file__).parent / "project_template"
    subprocess.run(
        ["wagtail", "start", f"--template={template_path}", project_name, project_path]
    )


def _get_settings() -> dict[str, str]:
    """Get the settings from the user."""
    settings: dict[str, str] = {}
    settings["project_dir"] = input("Project directory: ")
    settings["project_name"] = input("Project name: ")
    settings["log_file_path"] = input("Log file path: ")
    settings["db_url"] = input("Database url: ")
    settings["static_root_base"] = input("Static root base: ")
    settings["media_root_base"] = input("Media root base: ")

    return settings


def run() -> None:
    """Run the command line script to collect information and start the project."""
    settings: dict[str, str] = _get_settings()
    _create_project(settings["project_dir"], settings["project_name"])
    _create_settings_file(settings)
