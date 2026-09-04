import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class QuizScreen extends StatefulWidget{
  final Course course;
  const QuizScreen({super.key,required this.course});
  @override State<QuizScreen> createState()=>_QuizScreenState();
}
class _QuizScreenState extends State<QuizScreen>{
  late Future<QuizData> future;
  int index=0; final answers=<int,int>{}; Map<String,dynamic>? result;
  @override void initState(){super.initState();future=api.quiz(widget.course.id);}

  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:Text('${widget.course.title} • Quiz')),
    body:FutureBuilder<QuizData>(future:future,builder:(context,s){
      if(s.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator());
      if(s.hasError)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
        Text(s.error.toString()),
        FilledButton(onPressed:()async{
          await api.generateQuiz(widget.course.id,5);
          setState(()=>future=api.quiz(widget.course.id));
        },child:const Text('Generate quiz with AI'))
      ]));
      final quiz=s.data!;
      if(quiz.questions.isEmpty)return const Center(child:Text('This quiz contains no valid questions. Generate a new quiz.'));
      if(result!=null)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
        Text('Quiz complete',style:Theme.of(context).textTheme.headlineMedium),
        Text('Score: ${result!['score']} / ${result!['total']}'),
        Text('+${result!['xp_awarded']} XP'),
      ]));
      final q=quiz.questions[index];
      final selected=answers[q.id];
      return ListView(padding:const EdgeInsets.all(24),children:[
        LinearProgressIndicator(value:(index+1)/quiz.questions.length),
        const SizedBox(height:24),
        Text(q.question,style:Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height:16),
        for(int i=0;i<q.options.length;i++)
          RadioListTile<int>(value:i,groupValue:selected,onChanged:(v)=>setState(()=>answers[q.id]=v!),title:Text(q.options[i])),
        FilledButton(
          onPressed:selected==null?null:()async{
            if(index<quiz.questions.length-1){setState(()=>index++);}
            else{final r=await api.submitQuiz(quiz.id,answers);if(mounted)setState(()=>result=r);}
          },
          child:Text(index<quiz.questions.length-1?'Next':'Submit quiz'),
        )
      ]);
    }),
  );
}
