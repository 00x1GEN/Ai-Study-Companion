import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/common.dart';

class ProgressScreen extends StatelessWidget{
  const ProgressScreen({super.key});
  @override Widget build(BuildContext context)=>FutureBuilder<Map<String,dynamic>>(
    future:api.progress(),
    builder:(context,s){
      if(s.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator());
      if(s.hasError)return Center(child:AsyncErrorCard(s.error!));
      final p=s.data!;final badges=(p['badges'] as List);
      return ListView(padding:const EdgeInsets.all(20),children:[
        Text('Progress',style:Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height:16),
        Card(child:Padding(padding:const EdgeInsets.all(20),child:Column(children:[
          Text('Level ${p['level']}',style:Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height:12),LinearProgressIndicator(value:(p['level_progress'] as num).toDouble()),
          const SizedBox(height:8),Text('${p['xp']} XP • ${p['streak']} day streak'),
        ]))),
        const SectionTitle('Badges'),
        if(badges.isEmpty)const Text('No badges yet. Keep learning!'),
        ...badges.map((b)=>Card(child:ListTile(leading:const Icon(Icons.emoji_events),title:Text(b['name']),subtitle:Text(b['description']))))
      ]);
    },
  );
}
