import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/features/auth/data/models/user_model.dart';

class AuthController extends Notifier<AsyncValue<UserModel?>> {
  @override
  AsyncValue<UserModel?> build() => const AsyncValue.data(null);
}

final authControllerProvider = NotifierProvider<AuthController, AsyncValue<UserModel?>>(AuthController.new);
