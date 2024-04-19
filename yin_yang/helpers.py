import os
import subprocess

"""Check output of a command.

This is a helper method which will change how we check output depending on if
The application is running in a Flatpak or not.
"""

"""Base Flatpak Arguments

These are the base arguments we use to execute commands when running in 
a flatpak environment.
"""
base_flatpak_args = ['flatpak-spawn', '--host']


def check_output(args, universal_newlines=False) -> bytes:
    try:
        output = subprocess.check_output(
            args=args, universal_newlines=universal_newlines
        )
        return output
    except FileNotFoundError:
        flatpak_args = base_flatpak_args + args
        return subprocess.check_output(
            args=flatpak_args, universal_newlines=universal_newlines
        )


def check_call(command, stdout=None) -> int:
    try:
        return subprocess.check_call(command, stdout=stdout)
    except FileNotFoundError:
        flatpak_args = base_flatpak_args + command
        return subprocess.check_call(flatpak_args, stdout=stdout)


def is_flatpak() -> bool:
    return os.path.isfile('/.flatpak-info')


def get_usr() -> str:
    """
    Returns the proper path to /usr.
    This is need as the path to /usr is different in a flatpak environment.
    :return: The path to /usr with a trailing /
    """
    if is_flatpak():
        return '/var/run/host/usr/'
    return '/usr/'


def get_etc() -> str:
    """
    Returns the proper path to /etc.
    This is need as the path to /etc is different in a flatpak environment.
    :return: The path to /etc with a trailing /
    """
    if is_flatpak():
        return '/var/run/host/etc/'
    return '/etc/'


def run(
    command: list[str], kwargs: list[str] = [], stdout=None
) -> subprocess.CompletedProcess[str]:
    try:
        if len(kwargs) == 0:
            return subprocess.run(command, stdout=stdout)
        else:
            return subprocess.run(command, **kwargs, stdout=stdout)
    except FileNotFoundError:
        flatpak_args = base_flatpak_args + command
        if len(kwargs) == 0:
            return subprocess.run(flatpak_args, stdout=stdout)
        else:
            return subprocess.run(flatpak_args, **kwargs, stdout=stdout)
