import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'shell_screen.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget{
  const LoginScreen({super.key});
  @override State<LoginScreen> createState()=>_LoginScreenState();
}
class _LoginScreenState extends State<LoginScreen>{
  final email=TextEditingController(text:'student@aspira.test');
  final password=TextEditingController(text:'password123');
  bool loading=false; String? error;
  Future<void> submit() async{
    setState((){loading=true;error=null;});
    try{
      await api.login(email.text.trim(),password.text);
      if(!mounted)return;
      Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>const ShellScreen()));
    }catch(e){if(mounted)setState(()=>error=e.toString());}
    finally{if(mounted)setState(()=>loading=false);}
  }
  @override Widget build(BuildContext context)=>Scaffold(body:Center(child:ConstrainedBox(
    constraints:const BoxConstraints(maxWidth:430),
    child:Padding(padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
      const Icon(Icons.auto_awesome,size:70),
      const SizedBox(height:16),
      Text('AI Study Companion',style:Theme.of(context).textTheme.headlineMedium),
      const SizedBox(height:24),
      TextField(controller:email,keyboardType:TextInputType.emailAddress,decoration:const InputDecoration(labelText:'Email',border:OutlineInputBorder())),
      const SizedBox(height:12),
      TextField(controller:password,obscureText:true,decoration:const InputDecoration(labelText:'Password',border:OutlineInputBorder())),
      if(error!=null)Padding(padding:const EdgeInsets.only(top:12),child:Text(error!,style:TextStyle(color:Theme.of(context).colorScheme.error))),
      const SizedBox(height:18),
      SizedBox(width:double.infinity,child:FilledButton.icon(onPressed:loading?null:submit,icon:const Icon(Icons.login),label:Text(loading?'Signing in...':'Sign in'))),
      TextButton(onPressed:loading?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const RegisterScreen())),child:const Text('Create an account')),
    ])),
  )));
}
