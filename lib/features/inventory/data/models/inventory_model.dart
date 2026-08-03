class InventoryModel {
  final String? id;

  InventoryModel({this.id});

  factory InventoryModel.fromJson(Map<String, dynamic> json) {
    return InventoryModel(
      id: json['id'],
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
  };
}
