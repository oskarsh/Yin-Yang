# Info for packagers

The files in this directory should be installed to these locations:

| File                                 | Path                                       | Description                                      |
|--------------------------------------|--------------------------------------------|--------------------------------------------------|
| `yin_yang`                           | `/usr/bin`                                 | Executable for the terminal                      |
| `yin_yang.desktop`                   | `~/.local/share/applications/`             | Desktop file to start the application from menus |
| `logo.svg`                           | `/usr/share/icons/hicolor/scalable/apps/`  | Logo of the application                          |
| `yin_yang.service`, `yin_yang.timer` | `~/.local/share/systemd/user/`             | systemd unit files                               |
| `yin_yang.json`                      | `/usr/lib/mozilla/native-messaging-hosts/` | Manifest file for the Firefox extension          |

There is an installation script available under `./scripts/install.sh`

After installation, the systemd timer must be enabled:
```shell
systemctl --user enable yin_yang.timer
```
