import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/utils/responsive.dart';
import '../widgets/checkout_mobile_view.dart';
import '../widgets/checkout_tab_view.dart';

class CheckoutScreen extends ConsumerWidget {
  const CheckoutScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return const Scaffold(
      body: Responsive(
        mobile: CheckoutMobileView(),
        tablet: CheckoutTabView(),
      ),
    );
  }
}
