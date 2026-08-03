import 'package:untitled2/features/cart/data/models/cart_item_model.dart';

class InvoiceModel {
  final String id;
  final List<CartItemModel> items;
  final double total;

  InvoiceModel({required this.id, required this.items, required this.total});

  factory InvoiceModel.fromJson(Map<String, dynamic> json) {
    return InvoiceModel(
      id: json['id'] ?? '',
      items: (json['items'] as List).map((e) => CartItemModel.fromJson(e)).toList(),
      total: (json['total'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'items': items.map((e) => e.toJson()).toList(),
    'total': total,
  };
}
