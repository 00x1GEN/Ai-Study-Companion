import 'package:flutter_test/flutter_test.dart';
import 'package:ai_study_companion/main.dart';

void main(){
  testWidgets('shows login form',(tester)async{
    await tester.pumpWidget(const AiStudyCompanionApp());
    expect(find.text('AI Study Companion'),findsOneWidget);
    expect(find.text('Sign in'),findsOneWidget);
  });
}
