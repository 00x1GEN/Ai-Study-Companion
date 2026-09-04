import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'shell_screen.dart';

class RegisterScreen extends StatefulWidget{
  const RegisterScreen({super.key});
  @override State<RegisterScreen> createState()=>_RegisterScreenState();
}
class _RegisterScreenState extends State<RegisterScreen>{
  final name=TextEditingController();
  final email=TextEditingController();
  final password=TextEditingController();
  bool loading=false; String? error;

  Future<void> submit() async{
    if(name.text.trim().length<2||!email.text.contains('@')||password.text.length<8){
      setState(()=>error='Enter a valid name, email and password of at least 8 characters.');
      return;
    }
    setState((){loading=true;error=null;});
    try{
      await api.register(name.text.trim(),email.text.trim(),password.text);
      if(!mounted)return;
      Navigator.pushAndRemoveUntil(context,MaterialPageRoute(builder:(_)=>const ShellScreen()),(_)=>false);
    }catch(e){if(mounted)setState(()=>error=e.toString());}
    finally{if(mounted)setState(()=>loading=false);}
  }

  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('Create account')),
    body:Center(child:ConstrainedBox(constraints:const BoxConstraints(maxWidth:430),child:ListView(
      shrinkWrap:true,padding:const EdgeInsets.all(24),children:[
        TextField(controller:name,decoration:const InputDecoration(labelText:'Name',border:OutlineInputBorder())),
        const SizedBox(height:12),
        TextField(controller:email,keyboardType:TextInputType.emailAddress,decoration:const InputDecoration(labelText:'Email',border:OutlineInputBorder())),
        const SizedBox(height:12),
        TextField(controller:password,obscureText:true,decoration:const InputDecoration(labelText:'Password',border:OutlineInputBorder())),
        if(error!=null)Padding(padding:const EdgeInsets.only(top:12),child:Text(error!,style:TextStyle(color:Theme.of(context).colorScheme.error))),
        const SizedBox(height:18),
        FilledButton(onPressed:loading?null:submit,child:Text(loading?'Creating account...':'Create account')),
      ],
    ))),
  );
}
