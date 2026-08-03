import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/features/products/data/models/product_model.dart';

class ProductController extends Notifier<AsyncValue<List<ProductModel>>> {
  @override
  AsyncValue<List<ProductModel>> build() => const AsyncValue.data([]);
}

final productControllerProvider = NotifierProvider<ProductController, AsyncValue<List<ProductModel>>>(ProductController.new);
