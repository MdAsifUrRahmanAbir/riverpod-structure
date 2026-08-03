import 'package:flutter_riverpod/flutter_riverpod.dart';

class CheckoutController extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }

  Future<void> placeOrder() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      // TODO: Call checkout repository to place order
    });
  }

  void reset() {
    state = const AsyncValue.data(null);
  }
}

final checkoutControllerProvider =
NotifierProvider<CheckoutController, AsyncValue<void>>(
  CheckoutController.new,
);