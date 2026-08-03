import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';

final checkoutRepositoryProvider = Provider<CheckoutRepository>((ref) {
  return CheckoutRepository(ref.watch(apiClientProvider));
});

class CheckoutRepository {
  final ApiClient _apiClient;

  CheckoutRepository(this._apiClient);

  // TODO: Un-comment when calling API
  // Future<dynamic> fetchData() async {
  //   final response = await _apiClient.get(ApiEndpoints.products);
  //   return response.data;
  // }
}
