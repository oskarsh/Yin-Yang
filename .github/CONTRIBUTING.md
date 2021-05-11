## Communication

If you need to update the theme from an external application, you can do the following:

1. Add the following sections to the config file, where `<plugin>` is the name of your plugin:
   - `<plugin>Enabled: bool`
   - `<plugin>LightTheme: string`
   - `<plugin>DarkTheme: string`
1. Call `communicate.py` as a process from your application.
2. Write your application name into stdin of that process.
3. Read the response from stdout. It should be a json object with the following data:

```json
{
  "enabled": true,
  "dark_mode": true,
  "scheduled": true,
  "themes": ["light_theme", "dark_theme"],
  "times": [1615881600, 1615924800]
} 
```

- `enabled` is true if your plugin is enabled.
  If not, the response only contains `enabled` and `dark_mode`
- `dark_mode` is true if the system is currently using a dark theme
- `scheduled` is true if the theme changes automatically.
  If not, the response does not contain the times section.
- `themes` is a list of the preferred themes a strings.
- `times` is a list of the times when the theme changes.
  These are unix times in seconds since the epoch and always "surround" the current time.
  This enables your external application to calculate the preferred theme directly and
  compare it to `dark_mode` if you want.
  > For example, the times provided above would be the times when called on `2021-03-16 13:31:05`.

### Testing

To test if `communicat.py` gives the desired output,
got to the directory where you cloned this repo and open a terminal.
The following is an example output for firefox:

```
$ python
> import communicate.py
> communicate.send_config('firefox')
{'enabled': True, 'dark_mode': True, 'scheduled': True, 'themes': ['firefox-compact-light@mozilla.org', 'firefox-compact-dark@mozilla.org'], 'times': [1620756000, 1620795600]}

```
