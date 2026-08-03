class ProductModel {
  final String id;
  final String name;
  final double price;

  ProductModel({required this.id, required this.name, required this.price});

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      price: (json['price'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'price': price};
}
