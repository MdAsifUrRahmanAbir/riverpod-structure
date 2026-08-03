import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/features/cart/data/models/cart_item_model.dart';

class CartController extends Notifier<List<CartItemModel>> {
  @override
  List<CartItemModel> build() => [];
}

final cartControllerProvider = NotifierProvider<CartController, List<CartItemModel>>(CartController.new);
