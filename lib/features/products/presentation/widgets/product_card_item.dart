import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ProductCardItem extends ConsumerWidget {
  const ProductCardItem({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: Text('ProductCardItem'),
    );
  }
}
