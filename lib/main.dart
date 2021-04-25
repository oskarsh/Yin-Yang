import 'dart:io';
import 'package:flutter/material.dart';
import 'package:window_size/window_size.dart';
import 'package:yin_yang/pages/splash.dart';
import 'package:yin_yang/theme/ThemeNotifier.dart';
import 'package:provider/provider.dart';
import 'package:yin_yang/theme/theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    setWindowTitle('Yin-Yang Auto Nightmode');
    setWindowMinSize(const Size(400, 550));
    setWindowMaxSize(const Size(400, 550));
  }

  runApp(
    ChangeNotifierProvider<ThemeNotifier>(
      create: (_) => ThemeNotifier(darkTheme),
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final themeNotifier = Provider.of<ThemeNotifier>(context);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Yin-Yang',
      theme: themeNotifier.getTheme(),
      home: RouteSplash(),
    );
  }
}
