import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/network/api_client.dart';

final checkoutRepositoryProvider = Provider<CheckoutRepository>((ref) => CheckoutRepository(ref.watch(apiClientProvider)));

class CheckoutRepository {
  final ApiClient _apiClient;
  CheckoutRepository(this._apiClient);
}
