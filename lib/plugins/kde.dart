import 'package:process_run/shell.dart';

class KDE {
  KDE();

  var shell = Shell();

  List<String> getThemes() {
    return [
      'org.kde.breezetwilight.desktop',
      'org.kde.breeze.desktop',
      'org.kde.breezedark.desktop'
    ];
  }

  void switchToDark() async {
    String theme = 'org.kde.breezedark.desktop';
    await shell.run('lookandfeeltool -a $theme');
  }

  void switchToLight() async {
    print('called');
    String theme = 'org.kde.breeze.desktop';
    await shell.run('lookandfeeltool -a $theme');
  }
}
