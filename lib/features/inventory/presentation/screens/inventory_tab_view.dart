import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class InventoryTabView extends ConsumerWidget {
  const InventoryTabView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: Text('Inventory Tab View'),
    );
  }
}
