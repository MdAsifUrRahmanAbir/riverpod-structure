import 'package:flutter_riverpod/flutter_riverpod.dart';

class CartController extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }

  Future<void> addItem() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      // TODO: Call API or repository
    });
  }
}

final cartControllerProvider =
NotifierProvider<CartController, AsyncValue<void>>(
  CartController.new,
);