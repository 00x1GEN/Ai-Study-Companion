import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class FlashcardsScreen extends StatefulWidget{
  final Course course;
  const FlashcardsScreen({super.key,required this.course});
  @override State<FlashcardsScreen> createState()=>_FlashcardsScreenState();
}
class _FlashcardsScreenState extends State<FlashcardsScreen>{
  int index=0; bool answer=false;
  late Future<List<Flashcard>> future;
  @override void initState(){super.initState();future=api.flashcards(widget.course.id);}

  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:Text('${widget.course.title} • Flashcards')),
    body:FutureBuilder<List<Flashcard>>(future:future,builder:(context,s){
      if(s.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator());
      if(s.hasError)return Center(child:Text(s.error.toString()));
      final cards=s.data??[];
      if(cards.isEmpty)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
        const Text('No flashcards yet.'),
        FilledButton(onPressed:()async{
          await api.generateFlashcards(widget.course.id,5);
          setState(()=>future=api.flashcards(widget.course.id));
        },child:const Text('Generate with AI'))
      ]));
      if(index>=cards.length)index=cards.length-1;
      final card=cards[index];
      Future<void> rate(bool known) async{
        await api.reviewFlashcard(card.id,known);
        if(mounted)setState((){answer=false;if(index<cards.length-1)index++;});
      }
      return Padding(padding:const EdgeInsets.all(24),child:Column(children:[
        LinearProgressIndicator(value:(index+1)/cards.length),
        const SizedBox(height:20),
        Expanded(child:GestureDetector(onTap:()=>setState(()=>answer=!answer),child:Card(
          child:Center(child:Padding(padding:const EdgeInsets.all(24),child:Text(
            answer?card.answer:card.question,textAlign:TextAlign.center,style:Theme.of(context).textTheme.headlineSmall)))))),
        const SizedBox(height:10),
        Text(answer?'Rate your knowledge':'Tap the card to reveal the answer'),
        const SizedBox(height:12),
        if(answer)Row(children:[
          Expanded(child:OutlinedButton.icon(onPressed:()=>rate(false),icon:const Icon(Icons.refresh),label:const Text('Review again'))),
          const SizedBox(width:12),
          Expanded(child:FilledButton.icon(onPressed:()=>rate(true),icon:const Icon(Icons.check),label:const Text('I know it'))),
        ])
      ]));
    }),
  );
}
