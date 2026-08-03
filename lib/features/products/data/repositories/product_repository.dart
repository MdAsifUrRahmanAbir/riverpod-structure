import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/network/api_client.dart';

final productRepositoryProvider = Provider<ProductRepository>((ref) => ProductRepository(ref.watch(apiClientProvider)));

class ProductRepository {
  final ApiClient _apiClient;
  ProductRepository(this._apiClient);
}
