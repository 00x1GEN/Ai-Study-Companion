import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';
import '../widgets/common.dart';
import 'flashcards_screen.dart';
import 'quiz_screen.dart';

class CoursesScreen extends StatefulWidget{
  const CoursesScreen({super.key});
  @override State<CoursesScreen> createState()=>_CoursesScreenState();
}
class _CoursesScreenState extends State<CoursesScreen>{
  late Future<List<Course>> future;
  @override void initState(){super.initState();future=api.courses();}
  void reload()=>setState(()=>future=api.courses());

  Future<void> createCourse() async{
    final title=TextEditingController();
    final description=TextEditingController();
    final created=await showDialog<bool>(context:context,builder:(context)=>AlertDialog(
      title:const Text('Create course'),
      content:SizedBox(width:420,child:Column(mainAxisSize:MainAxisSize.min,children:[
        TextField(controller:title,decoration:const InputDecoration(labelText:'Course title')),
        TextField(controller:description,decoration:const InputDecoration(labelText:'Description')),
      ])),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(context,false),child:const Text('Cancel')),
        FilledButton(onPressed:()async{
          if(title.text.trim().length<2)return;
          try{await api.createCourse(title.text.trim(),description.text.trim());if(context.mounted)Navigator.pop(context,true);}
          catch(e){if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(e.toString())));}
        },child:const Text('Create'))
      ],
    ));
    if(created==true)reload();
  }

  Future<void> upload(Course course) async{
    final result=await FilePicker.platform.pickFiles(type:FileType.custom,allowedExtensions:['pdf','docx']);
    if(result==null||result.files.single.path==null)return;
    if(!mounted)return;
    showDialog(context:context,barrierDismissible:false,builder:(_)=>const Center(child:CircularProgressIndicator()));
    try{
      final material=await api.uploadMaterial(course.id,result.files.single.path!);
      if(mounted){
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Material status: ${material.status}, chunks: ${material.chunkCount}')));
      }
    }catch(e){
      if(mounted){Navigator.pop(context);ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(e.toString())));}
    }
  }

  @override Widget build(BuildContext context)=>FutureBuilder<List<Course>>(
    future:future,
    builder:(context,s){
      if(s.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator());
      if(s.hasError)return Center(child:AsyncErrorCard(s.error!));
      final courses=s.data??[];
      return RefreshIndicator(onRefresh:()async=>reload(),child:ListView(
        padding:const EdgeInsets.all(20),
        children:[
          Row(children:[Expanded(child:Text('Courses',style:Theme.of(context).textTheme.headlineMedium)),IconButton(onPressed:createCourse,tooltip:'Create course',icon:const Icon(Icons.add)),IconButton(onPressed:reload,icon:const Icon(Icons.refresh))]),
          if(courses.isEmpty)const Padding(padding:EdgeInsets.symmetric(vertical:40),child:Center(child:Text('No courses yet. Use + to create your first course.'))),
          ...courses.map((c)=>Card(child:ExpansionTile(
            leading:const Icon(Icons.school),
            title:Text(c.title),
            subtitle:Text(c.description),
            children:[
              ListTile(leading:const Icon(Icons.upload_file),title:const Text('Upload PDF/DOCX'),onTap:()=>upload(c)),
              ListTile(leading:const Icon(Icons.style),title:const Text('Flashcards'),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>FlashcardsScreen(course:c)))),
              ListTile(leading:const Icon(Icons.quiz),title:const Text('Quiz'),onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>QuizScreen(course:c)))),
            ],
          ))),
        ],
      ));
    },
  );
}
