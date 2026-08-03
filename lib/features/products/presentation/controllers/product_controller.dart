import 'package:flutter_riverpod/flutter_riverpod.dart';

class ProductController extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }

  // প্রোডাক্ট ফেচ বা কোনো অ্যাকশন ট্রিগার করার মেথড
  Future<void> fetchProducts() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      // TODO: Call your product repository here
      // await ref.read(productRepositoryProvider).getProducts();
    });
  }

  // স্টেট রিসেট করার জন্য
  void reset() {
    state = const AsyncValue.data(null);
  }
}

final productControllerProvider =
NotifierProvider<ProductController, AsyncValue<void>>(
  ProductController.new,
);