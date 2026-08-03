import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/utils/responsive.dart';
import 'package:untitled2/features/inventory/presentation/screens/inventory_mobile_view.dart';
import 'package:untitled2/features/inventory/presentation/screens/inventory_tab_view.dart';

class InventoryScreen extends ConsumerWidget {
  const InventoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Responsive(
        mobile: const InventoryMobileView(),
        tablet: const InventoryTabView(),
      ),
    );
  }
}
