# Info for packagers

The files in this directory should be installed to these locations:

| File                                 | Path                                       | Description                                      |
|--------------------------------------|--------------------------------------------|--------------------------------------------------|
| `yin-yang`                           | `/usr/bin`                                 | Executable for the terminal                      |
| `Yin-Yang.desktop`                   | `~/.local/share/applications/`             | Desktop file to start the application from menus |
| `logo.svg`                           | `/usr/share/icons/hicolor/scalable/apps/`  | Logo of the application                          |
| `yin_yang.service`, `yin_yang.timer` | `~/.local/share/systemd/user/`             | systemd unit files                               |
| `yin_yang.json`                      | `/usr/lib/mozilla/native-messaging-hosts/` | Manifest file for the Firefox extension          |

There is an installation script available under `./scripts/install.sh`
