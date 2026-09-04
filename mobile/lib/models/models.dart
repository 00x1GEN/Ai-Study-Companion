class Course {
  final int id;
  final String title;
  final String description;
  final double progress;
  Course({required this.id, required this.title, required this.description, required this.progress});
  factory Course.fromJson(Map<String,dynamic> j) => Course(
    id:j['id'], title:j['title'], description:j['description']??'', progress:(j['progress'] as num).toDouble());
}

class MaterialItem {
  final int id;
  final String title;
  final String status;
  final int chunkCount;
  MaterialItem({required this.id, required this.title, required this.status, required this.chunkCount});
  factory MaterialItem.fromJson(Map<String,dynamic> j)=>MaterialItem(
    id:j['id'], title:j['title'], status:j['status'], chunkCount:j['chunk_count']);
}

class Flashcard {
  final int id;
  final String question;
  final String answer;
  final int box;
  Flashcard({required this.id, required this.question, required this.answer, required this.box});
  factory Flashcard.fromJson(Map<String,dynamic> j)=>Flashcard(id:j['id'],question:j['question'],answer:j['answer'],box:j['box']);
}

class QuizQuestion {
  final int id;
  final String question;
  final List<String> options;
  QuizQuestion({required this.id,required this.question,required this.options});
  factory QuizQuestion.fromJson(Map<String,dynamic> j)=>QuizQuestion(id:j['id'],question:j['question'],options:List<String>.from(j['options']));
}

class QuizData {
  final int id;
  final String title;
  final List<QuizQuestion> questions;
  QuizData({required this.id,required this.title,required this.questions});
  factory QuizData.fromJson(Map<String,dynamic> j)=>QuizData(
    id:j['id'],title:j['title'],questions:(j['questions'] as List).map((x)=>QuizQuestion.fromJson(x)).toList());
}
