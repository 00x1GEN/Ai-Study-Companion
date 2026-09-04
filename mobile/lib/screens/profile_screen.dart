import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'login_screen.dart';

class ProfileScreen extends StatelessWidget{
  const ProfileScreen({super.key});
  @override Widget build(BuildContext context)=>ListView(padding:const EdgeInsets.all(20),children:[
    const CircleAvatar(radius:42,child:Icon(Icons.person,size:42)),
    const SizedBox(height:12),
    Center(child:Text('AI Study Companion',style:Theme.of(context).textTheme.titleLarge)),
    const SizedBox(height:24),
    Card(child:ListTile(leading:const Icon(Icons.security),title:const Text('Secure session'),subtitle:const Text('Access and rotating refresh tokens stored in secure storage'))),
    FilledButton.tonalIcon(onPressed:()async{
      await api.logout();
      if(context.mounted)Navigator.pushAndRemoveUntil(context,MaterialPageRoute(builder:(_)=>const LoginScreen()),(_)=>false);
    },icon:const Icon(Icons.logout),label:const Text('Sign out'))
  ]);
}
