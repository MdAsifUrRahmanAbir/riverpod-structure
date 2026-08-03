import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';

final productRepositoryProvider = Provider<ProductRepository>((ref) {
  return ProductRepository(ref.watch(apiClientProvider));
});

class ProductRepository {
  final ApiClient _apiClient;

  ProductRepository(this._apiClient);

  // TODO: Un-comment when calling API
  // Future<dynamic> fetchData() async {
  //   final response = await _apiClient.get(ApiEndpoints.products);
  //   return response.data;
  // }
}
