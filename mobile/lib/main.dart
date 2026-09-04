import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main()=>runApp(const AiStudyCompanionApp());

class AiStudyCompanionApp extends StatelessWidget{
  const AiStudyCompanionApp({super.key});
  @override Widget build(BuildContext context)=>MaterialApp(
    title:'AI Study Companion',
    debugShowCheckedModeBanner:false,
    theme:ThemeData(colorSchemeSeed:Colors.indigo,useMaterial3:true),
    darkTheme:ThemeData(colorSchemeSeed:Colors.indigo,brightness:Brightness.dark,useMaterial3:true),
    home:const LoginScreen(),
  );
}
