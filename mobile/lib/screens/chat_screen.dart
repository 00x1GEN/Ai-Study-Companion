import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class ChatScreen extends StatefulWidget{
  const ChatScreen({super.key});
  @override State<ChatScreen> createState()=>_ChatScreenState();
}
class _ChatScreenState extends State<ChatScreen>{
  final input=TextEditingController();
  final messages=<Map<String,String>>[];
  bool loading=false;
  String provider='mock';
  late Future<List<Course>> coursesFuture;
  int? courseId;

  @override void initState(){
    super.initState();
    coursesFuture=api.courses();
  }

  Future<void> send() async{
    final text=input.text.trim();
    if(text.isEmpty||loading||courseId==null)return;
    setState((){messages.add({'role':'user','text':text});input.clear();loading=true;});
    try{
      final r=await api.chat(courseId!,text,provider:provider);
      final sources=(r['sources'] as List).map((x)=>x['title']).toSet().join(', ');
      if(mounted)setState(()=>messages.add({'role':'assistant','text':'${r['answer']}\n\nSources: ${sources.isEmpty ? 'none' : sources}'}));
    }catch(e){if(mounted)setState(()=>messages.add({'role':'assistant','text':'Error: $e'}));}
    finally{if(mounted)setState(()=>loading=false);}
  }

  @override Widget build(BuildContext context)=>FutureBuilder<List<Course>>(
    future:coursesFuture,
    builder:(context,s){
      if(s.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator());
      if(s.hasError)return Center(child:Text(s.error.toString()));
      final courses=s.data??[];
      if(courses.isEmpty)return const Center(child:Text('Create a course before using AI Chat.'));
      courseId ??= courses.first.id;
      return Column(children:[
        Padding(padding:const EdgeInsets.fromLTRB(12,8,12,0),child:Wrap(spacing:16,crossAxisAlignment:WrapCrossAlignment.center,children:[
          DropdownButton<int>(value:courseId,items:courses.map((c)=>DropdownMenuItem(value:c.id,child:Text(c.title))).toList(),onChanged:(v)=>setState(()=>courseId=v)),
          DropdownButton<String>(value:provider,items:const[
            DropdownMenuItem(value:'mock',child:Text('Mock')),
            DropdownMenuItem(value:'openai',child:Text('OpenAI')),
            DropdownMenuItem(value:'anthropic',child:Text('Claude')),
            DropdownMenuItem(value:'gemini',child:Text('Gemini')),
          ],onChanged:(v)=>setState(()=>provider=v!))
        ])),
        Expanded(child:ListView.builder(padding:const EdgeInsets.all(16),itemCount:messages.length,itemBuilder:(context,i){
          final m=messages[i];final user=m['role']=='user';
          return Align(alignment:user?Alignment.centerRight:Alignment.centerLeft,child:Card(
            color:user?Theme.of(context).colorScheme.primaryContainer:null,
            child:Padding(padding:const EdgeInsets.all(12),child:ConstrainedBox(constraints:const BoxConstraints(maxWidth:550),child:Text(m['text']!)))));
        })),
        if(loading)const LinearProgressIndicator(),
        SafeArea(child:Padding(padding:const EdgeInsets.all(12),child:Row(children:[
          Expanded(child:TextField(controller:input,onSubmitted:(_)=>send(),decoration:const InputDecoration(labelText:'Ask about uploaded course material',border:OutlineInputBorder()))),
          const SizedBox(width:8),IconButton.filled(onPressed:courseId==null?null:send,icon:const Icon(Icons.send))
        ])))
      ]);
    },
  );
}
