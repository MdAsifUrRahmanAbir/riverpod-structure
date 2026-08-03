import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/network/api_client.dart';

final inventoryRepositoryProvider = Provider<InventoryRepository>((ref) {
  return InventoryRepository(ref.watch(apiClientProvider));
});

class InventoryRepository {
  final ApiClient _apiClient;

  InventoryRepository(this._apiClient);
}
