import 'package:process_run/shell.dart';
// import 'package:shared_preferences/shared_preferences.dart';

var shell = Shell();

class Config {
  Config();

  getOS() async {
    print('hello');
    // SharedPreferences prefs = await SharedPreferences.getInstance();
    String osString = await getOS();
    print(osString);
  }
}
