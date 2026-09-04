import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthStore {
  static const _storage = FlutterSecureStorage();
  static const _accessKey = 'access_token';
  static const _refreshKey = 'refresh_token';

  Future<String?> access() => _storage.read(key:_accessKey);
  Future<String?> refresh() => _storage.read(key:_refreshKey);

  Future<void> save(String access, String refresh) async {
    await _storage.write(key:_accessKey,value:access);
    await _storage.write(key:_refreshKey,value:refresh);
  }

  Future<void> clear() => _storage.deleteAll();
}

final authStore = AuthStore();
