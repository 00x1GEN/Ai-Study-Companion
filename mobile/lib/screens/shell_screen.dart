import 'package:flutter/material.dart';
import 'dashboard_screen.dart';
import 'courses_screen.dart';
import 'chat_screen.dart';
import 'progress_screen.dart';
import 'profile_screen.dart';

class ShellScreen extends StatefulWidget{
  const ShellScreen({super.key});
  @override State<ShellScreen> createState()=>_ShellScreenState();
}
class _ShellScreenState extends State<ShellScreen>{
  int index=0;
  final pages=const[DashboardScreen(),CoursesScreen(),ChatScreen(),ProgressScreen(),ProfileScreen()];
  @override Widget build(BuildContext context)=>Scaffold(
    body:SafeArea(child:pages[index]),
    bottomNavigationBar:NavigationBar(selectedIndex:index,onDestinationSelected:(i)=>setState(()=>index=i),destinations:const[
      NavigationDestination(icon:Icon(Icons.dashboard_outlined),label:'Home'),
      NavigationDestination(icon:Icon(Icons.school_outlined),label:'Courses'),
      NavigationDestination(icon:Icon(Icons.smart_toy_outlined),label:'AI Chat'),
      NavigationDestination(icon:Icon(Icons.insights_outlined),label:'Progress'),
      NavigationDestination(icon:Icon(Icons.person_outline),label:'Profile'),
    ]),
  );
}
