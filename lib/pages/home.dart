import 'package:flutter/material.dart';

class Home extends StatefulWidget {
  Home({Key key}) : super(key: key);

  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              child: IconButton(
                icon: const Icon(Icons.settings),
                alignment: Alignment.topRight,
              ),
            ),
            Container(
              child: new Image.asset(
                'images/lake.jpg',
                width: 600.0,
                height: 240.0,
                fit: BoxFit.cover,
              ),
            ),
            Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  RawMaterialButton(
                      child: Text('Light'),
                      onPressed: () {
                        print('light');
                      }),
                  RawMaterialButton(
                      child: Text('Dark'),
                      onPressed: () {
                        print('Dark');
                      })
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
