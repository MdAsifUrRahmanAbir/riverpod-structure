import 'package:flutter_riverpod/flutter_riverpod.dart';

class InventoryController extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }
}

final inventoryControllerProvider = NotifierProvider<InventoryController, AsyncValue<void>>(InventoryController.new);
