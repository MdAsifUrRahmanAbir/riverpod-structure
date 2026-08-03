import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/utils/responsive.dart';
import '../widgets/cart_mobile_view.dart';
import '../widgets/cart_tab_view.dart';

class CartScreen extends ConsumerWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return const Scaffold(
      body: Responsive(
        mobile: CartMobileView(),
        tablet: CartTabView(),
      ),
    );
  }
}
