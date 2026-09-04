import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/common.dart';

class DashboardScreen extends StatelessWidget{
  const DashboardScreen({super.key});
  @override Widget build(BuildContext context)=>FutureBuilder(
    future:Future.wait([api.courses(),api.progress()]),
    builder:(context,s){
      if(s.connectionState!=ConnectionState.done)return const Center(child:CircularProgressIndicator());
      if(s.hasError)return Center(child:AsyncErrorCard(s.error!));
      final courses=s.data![0] as List; final p=s.data![1] as Map<String,dynamic>;
      return ListView(padding:const EdgeInsets.all(20),children:[
        Text('Welcome back',style:Theme.of(context).textTheme.headlineMedium),
        const Text('Learn from your own materials with AI-assisted study tools.'),
        const SectionTitle('Progress'),
        Wrap(spacing:12,runSpacing:12,children:[
          _Metric('XP','${p['xp']}'),_Metric('Level','${p['level']}'),_Metric('Streak','${p['streak']} days')
        ]),
        const SectionTitle('Courses'),
        ...courses.take(4).map((c)=>Card(child:ListTile(
          leading:const Icon(Icons.menu_book),
          title:Text(c.title),
          subtitle:Text('${(c.progress*100).round()}% complete'),
        ))),
      ]);
    },
  );
}
class _Metric extends StatelessWidget{
  final String label,value;
  const _Metric(this.label,this.value);
  @override Widget build(BuildContext context)=>Card(child:SizedBox(width:115,child:Padding(
    padding:const EdgeInsets.all(16),child:Column(children:[
      Text(value,style:Theme.of(context).textTheme.headlineSmall),Text(label)
    ]))));
}
