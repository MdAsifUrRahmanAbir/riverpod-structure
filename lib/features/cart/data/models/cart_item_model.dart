import 'package:untitled2/features/products/data/models/product_model.dart';

class CartItemModel {
  final ProductModel product;
  final int quantity;

  CartItemModel({required this.product, required this.quantity});

  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      product: ProductModel.fromJson(json['product']),
      quantity: json['quantity'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() => {'product': product.toJson(), 'quantity': quantity};
}
