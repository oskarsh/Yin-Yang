import subprocess


"""Check output of a command.

This is a helper method which will change how we check output depending on if
The application is running in a Flatpak or not.
"""


def check_output(args, universal_newlines=False) -> bytes:
    try:
        output = subprocess.check_output(
            args=args, universal_newlines=universal_newlines
        )
        return output
    except FileNotFoundError:
        flatpak_args = ["flatpak-spawn", "--host"] + args
        return subprocess.check_output(
            args=flatpak_args, universal_newlines=universal_newlines
        )


def check_call(command, stdout=None) -> int:
    try:
        return subprocess.check_call(command, stdout=stdout)
    except FileNotFoundError:
        flatpak_args = ["flatpak-spawn", "--host"] + command
        return subprocess.check_call(flatpak_args, stdout=stdout)


def is_flatpak() -> bool:
    try:
        subprocess.run('lookandfeeltool')
        return False
    except FileNotFoundError:
        return True

def run(command: list[str], kwargs: list[str] = []) -> subprocess.CompletedProcess[str]:
    try:
        if len(kwargs) == 0:
            return subprocess.run(command)
        else:
            return subprocess.run(command, **kwargs)
    except FileNotFoundError:
        flatpak_args = ["flatpak-spawn", "--host"] + command
        if len(kwargs) == 0:
            return subprocess.run(flatpak_args)
        else:
            return subprocess.run(flatpak_args, **kwargs)
