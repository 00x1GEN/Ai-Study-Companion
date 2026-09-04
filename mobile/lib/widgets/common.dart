import 'package:flutter/material.dart';

class AsyncErrorCard extends StatelessWidget{
  final Object error;
  const AsyncErrorCard(this.error,{super.key});
  @override Widget build(BuildContext context)=>Card(
    color:Theme.of(context).colorScheme.errorContainer,
    child:Padding(padding:const EdgeInsets.all(16),child:Text(error.toString())));
}

class SectionTitle extends StatelessWidget{
  final String text;
  const SectionTitle(this.text,{super.key});
  @override Widget build(BuildContext context)=>Padding(
    padding:const EdgeInsets.only(top:20,bottom:10),
    child:Text(text,style:Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight:FontWeight.bold)));
}
