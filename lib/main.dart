import 'dart:io';
import 'package:flutter/material.dart';
import 'package:window_size/window_size.dart';
import 'package:yin_yang/pages/home.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    setWindowTitle('uhrwald - focus timer');
    setWindowMinSize(const Size(600, 800));
    setWindowMaxSize(const Size(600, 800));
  }
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Home(),
    );
  }
}
