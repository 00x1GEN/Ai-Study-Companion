import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/api_config.dart';
import '../models/models.dart';
import 'auth_store.dart';

class ApiException implements Exception {
  final int? status;
  final String message;
  ApiException(this.message,{this.status});
  @override String toString()=>message;
}

class ApiService {
  Future<Map<String,String>> _headers() async {
    final token=await authStore.access();
    return {'Content-Type':'application/json',if(token!=null)'Authorization':'Bearer $token'};
  }

  Future<void> register(String name,String email,String password) async {
    final r=await http.post(Uri.parse('${ApiConfig.baseUrl}/auth/register'),
      headers:{'Content-Type':'application/json'},
      body:jsonEncode({'name':name,'email':email,'password':password}));
    if(r.statusCode!=201){String msg='Registration failed';try{msg=jsonDecode(r.body)['detail']?.toString()??msg;}catch(_){}throw ApiException(msg,status:r.statusCode);}
    final j=jsonDecode(r.body);
    await authStore.save(j['access_token'],j['refresh_token']);
  }

  Future<void> login(String email,String password) async {
    final r=await http.post(Uri.parse('${ApiConfig.baseUrl}/auth/login'),
      headers:{'Content-Type':'application/json'},
      body:jsonEncode({'email':email,'password':password}));
    if(r.statusCode!=200){String msg='Login failed';try{msg=jsonDecode(r.body)['detail']?.toString()??msg;}catch(_){}throw ApiException(msg,status:r.statusCode);}
    final j=jsonDecode(r.body);
    await authStore.save(j['access_token'],j['refresh_token']);
  }

  Future<void> logout() async {
    final refresh=await authStore.refresh();
    if(refresh!=null){
      try{
        await http.post(Uri.parse('${ApiConfig.baseUrl}/auth/logout'),
          headers:{'Content-Type':'application/json'},
          body:jsonEncode({'refresh_token':refresh}));
      }catch(_){ }
    }
    await authStore.clear();
  }

  Future<bool> refreshTokens() async {
    final refresh=await authStore.refresh();
    if(refresh==null)return false;
    final r=await http.post(Uri.parse('${ApiConfig.baseUrl}/auth/refresh'),
      headers:{'Content-Type':'application/json'},
      body:jsonEncode({'refresh_token':refresh}));
    if(r.statusCode!=200){await authStore.clear();return false;}
    final j=jsonDecode(r.body);
    await authStore.save(j['access_token'],j['refresh_token']);
    return true;
  }

  Future<http.Response> _authorized(Future<http.Response> Function(Map<String,String>) action) async {
    var r=await action(await _headers());
    if(r.statusCode==401 && await refreshTokens()){
      r=await action(await _headers());
    }
    return r;
  }

  void _ok(http.Response r,[List<int> statuses=const[200]]){
    if(!statuses.contains(r.statusCode)){
      String msg='Request failed';
      try{msg=jsonDecode(r.body)['detail']?.toString()??msg;}catch(_){}
      throw ApiException(msg,status:r.statusCode);
    }
  }

  Future<List<Course>> courses() async {
    final r=await _authorized((h)=>http.get(Uri.parse('${ApiConfig.baseUrl}/courses'),headers:h));
    _ok(r);
    return (jsonDecode(r.body) as List).map((x)=>Course.fromJson(x)).toList();
  }

  Future<Course> createCourse(String title,String description) async {
    final r=await _authorized((h)=>http.post(Uri.parse('${ApiConfig.baseUrl}/courses'),headers:h,
      body:jsonEncode({'title':title,'description':description})));
    _ok(r,[201]);
    return Course.fromJson(jsonDecode(r.body));
  }

  Future<List<MaterialItem>> materials(int courseId) async {
    final r=await _authorized((h)=>http.get(Uri.parse('${ApiConfig.baseUrl}/courses/$courseId/materials'),headers:h));
    _ok(r);
    return (jsonDecode(r.body) as List).map((x)=>MaterialItem.fromJson(x)).toList();
  }

  Future<MaterialItem> uploadMaterial(int courseId,String filePath) async {
    final token=await authStore.access();
    final request=http.MultipartRequest('POST',Uri.parse('${ApiConfig.baseUrl}/courses/$courseId/materials'));
    if(token!=null)request.headers['Authorization']='Bearer $token';
    request.files.add(await http.MultipartFile.fromPath('file',filePath));
    var streamed=await request.send();
    var r=await http.Response.fromStream(streamed);
    if(r.statusCode==401 && await refreshTokens()){
      final retry=http.MultipartRequest('POST',Uri.parse('${ApiConfig.baseUrl}/courses/$courseId/materials'));
      final newToken=await authStore.access();
      if(newToken!=null)retry.headers['Authorization']='Bearer $newToken';
      retry.files.add(await http.MultipartFile.fromPath('file',filePath));
      r=await http.Response.fromStream(await retry.send());
    }
    _ok(r,[201]);
    return MaterialItem.fromJson(jsonDecode(r.body));
  }

  Future<List<Flashcard>> flashcards(int courseId) async {
    final r=await _authorized((h)=>http.get(Uri.parse('${ApiConfig.baseUrl}/courses/$courseId/flashcards'),headers:h));
    _ok(r);
    return (jsonDecode(r.body) as List).map((x)=>Flashcard.fromJson(x)).toList();
  }

  Future<void> reviewFlashcard(int id,bool known) async {
    final r=await _authorized((h)=>http.post(Uri.parse('${ApiConfig.baseUrl}/flashcards/$id/review'),headers:h,
      body:jsonEncode({'known':known})));
    _ok(r);
  }

  Future<QuizData> quiz(int courseId) async {
    final r=await _authorized((h)=>http.get(Uri.parse('${ApiConfig.baseUrl}/courses/$courseId/quiz'),headers:h));
    _ok(r);
    return QuizData.fromJson(jsonDecode(r.body));
  }

  Future<Map<String,dynamic>> submitQuiz(int quizId,Map<int,int> answers) async {
    final stringMap=answers.map((k,v)=>MapEntry(k.toString(),v));
    final r=await _authorized((h)=>http.post(Uri.parse('${ApiConfig.baseUrl}/quizzes/$quizId/submit'),headers:h,
      body:jsonEncode({'answers':stringMap})));
    _ok(r);
    return jsonDecode(r.body);
  }

  Future<Map<String,dynamic>> progress() async {
    final r=await _authorized((h)=>http.get(Uri.parse('${ApiConfig.baseUrl}/progress'),headers:h));
    _ok(r);
    return jsonDecode(r.body);
  }

  Future<Map<String,dynamic>> chat(int courseId,String message,{String? provider}) async {
    final r=await _authorized((h)=>http.post(Uri.parse('${ApiConfig.baseUrl}/ai/chat'),headers:h,
      body:jsonEncode({'course_id':courseId,'message':message,if(provider!=null)'provider':provider})));
    _ok(r);
    return jsonDecode(r.body);
  }

  Future<int> generateFlashcards(int courseId,int count) async {
    final r=await _authorized((h)=>http.post(Uri.parse('${ApiConfig.baseUrl}/ai/flashcards/generate'),headers:h,
      body:jsonEncode({'course_id':courseId,'count':count})));
    _ok(r);
    return jsonDecode(r.body)['created'];
  }

  Future<int> generateQuiz(int courseId,int count) async {
    final r=await _authorized((h)=>http.post(Uri.parse('${ApiConfig.baseUrl}/ai/quiz/generate'),headers:h,
      body:jsonEncode({'course_id':courseId,'count':count})));
    _ok(r);
    return jsonDecode(r.body)['created'];
  }
}
final api=ApiService();
