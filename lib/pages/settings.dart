import 'package:flutter/material.dart';

class Settings extends StatefulWidget {
  Settings({Key key}) : super(key: key);

  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
                alignment: Alignment.centerLeft,
                padding: EdgeInsets.all(20),
                height: MediaQuery.of(context).size.height * 0.1,
                child: TextButton.icon(
                  label: Text('back'),
                  style: TextButton.styleFrom(
                      primary: Colors.black, padding: EdgeInsets.all(5)),
                  onPressed: () => {Navigator.pop(context)},
                  icon: Icon(Icons.arrow_back),
                )),
            Container(
                padding: EdgeInsets.all(20),
                height: MediaQuery.of(context).size.height * 0.8,
                child: Column(
                  children: [
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Settings',
                        style: TextStyle(
                            fontSize: 25, fontWeight: FontWeight.bold),
                      ),
                    )
                  ],
                ))
          ],
        ),
      ),
    );
  }
}
