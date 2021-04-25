import 'package:flutter/material.dart';
import 'package:process_run/shell.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:yin_yang/pages/home.dart';

class RouteSplash extends StatefulWidget {
  @override
  _RouteSplashState createState() => _RouteSplashState();
}

class _RouteSplashState extends State<RouteSplash> {
  bool loading = true;
  var shell = Shell();
  @override
  void initState() {
    super.initState();
    shell.run('sh lib/scripts/getOS.sh').then((env) {
      SharedPreferences.getInstance().then((prefs) {
        String desktop = '';

        if (env.outText.contains('KDE') ||
            env.outText.contains('plasma') ||
            env.outText.contains('plasma5')) {
          desktop = 'KDE';
        }
        if (env.outText.contains('gnome')) {
          desktop = 'gnome';
        }
        if (env.outText.contains('budgie')) {
          desktop = 'budgie';
        }
        if (env.outText.contains('xfce')) {
          desktop = 'xfce';
        }
        prefs.setString('desktop', desktop);
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => Home()),
        );
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold();
  }
}
