import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/utils/responsive.dart';
import 'checkout_mobile_view.dart';
import 'checkout_tab_view.dart';

class CheckoutScreen extends ConsumerWidget {
  const CheckoutScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Responsive(
        mobile: const CheckoutMobileView(),
        tablet: const CheckoutTabView(),
      ),
    );
  }
}
