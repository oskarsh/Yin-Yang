import 'package:flutter/material.dart';
import 'package:yin_yang/pages/settings.dart';

class Home extends StatefulWidget {
  Home({Key key}) : super(key: key);

  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  RangeValues values = RangeValues(1, 24);
  RangeLabels labels = RangeLabels('1', "24");
  bool _themeIsDark = false;
  bool _isScheduled = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: <Widget>[
            Container(
              padding: EdgeInsets.all(20),
              alignment: Alignment.centerRight,
              height: MediaQuery.of(context).size.height * 0.1,
              child: IconButton(
                padding: EdgeInsets.all(2),
                icon: const Icon(Icons.settings),
                alignment: Alignment.topRight,
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => Settings()),
                  );
                },
              ),
            ),
            Container(
              padding: EdgeInsets.fromLTRB(50, 10, 50, 10),
              height: MediaQuery.of(context).size.height * 0.9,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Container(
                    child: new Image.asset(
                      'assets/icon.png',
                      width: 128.0,
                      height: 128.0,
                      fit: BoxFit.cover,
                    ),
                  ),
                  Center(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        OutlinedButton(
                          onPressed: _themeIsDark ? () {} : null,
                          child: Text('Light'),
                          style: OutlinedButton.styleFrom(
                              primary: Colors.black,
                              padding: EdgeInsets.fromLTRB(50, 20, 50, 20)),
                        ),
                        OutlinedButton(
                            onPressed: _themeIsDark ? null : () {},
                            child: Text('Dark'),
                            style: OutlinedButton.styleFrom(
                                primary: Colors.black,
                                padding: EdgeInsets.fromLTRB(50, 20, 50, 20)))
                      ],
                    ),
                  ),
                  Container(
                    child: Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                              width: MediaQuery.of(context).size.width * 0.4,
                              child: CheckboxListTile(
                                activeColor: Colors.black,
                                title: Text("scheduled"),
                                value: _isScheduled,
                                onChanged: (newValue) {
                                  setState(() {
                                    _isScheduled = !_isScheduled;
                                  });
                                },
                                controlAffinity:
                                    ListTileControlAffinity.leading,
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(20.0),
                              child: Text(
                                labels.start + " - " + labels.end,
                                style: TextStyle(fontSize: 15),
                              ),
                            )
                          ],
                        ),
                        SliderTheme(
                          data: SliderThemeData(
                              thumbColor:
                                  _themeIsDark ? Colors.white : Colors.black,
                              activeTrackColor: Colors.white70,
                              inactiveTrackColor: Colors.black),
                          child: RangeSlider(
                              min: 1,
                              max: 23,
                              divisions: 48,
                              values: values,
                              labels: labels,
                              onChanged: _isScheduled
                                  ? (v) {
                                      String startLabel =
                                          v.start % v.start.round() < 1
                                              ? "30"
                                              : "00";
                                      String endLabel =
                                          v.end % v.end.round() < 1
                                              ? "30"
                                              : "00";
                                      setState(() {
                                        values = v;
                                        labels = RangeLabels(
                                            "${(v.start).toInt().toString()}:$startLabel",
                                            "${(v.end).toInt().toString()}:$endLabel");
                                      });
                                    }
                                  : null),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
