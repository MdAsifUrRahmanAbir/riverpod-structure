import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/network/api_client.dart';
import 'package:untitled2/features/auth/data/models/user_model.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) => AuthRepository(ref.watch(apiClientProvider)));

class AuthRepository {
  final ApiClient _apiClient;
  AuthRepository(this._apiClient);

  Future<UserModel> login(String email, String password) async {
    return UserModel(id: '1', name: 'User', email: email);
  }
}
