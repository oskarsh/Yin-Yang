from plugins._plugin import PluginCommandline


class Xfce(PluginCommandline):
    def __init__(self):
        super(Xfce, self).__init__(['xfconf-query', '-c', 'xsettings', '-p', '/Net/ThemeName', '-s', '{theme}'])
