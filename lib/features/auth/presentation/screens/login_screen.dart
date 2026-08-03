import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/core/utils/responsive.dart';
import 'login_mobile_view.dart';
import 'login_tab_view.dart';

class LoginScreen extends ConsumerWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Responsive(
        mobile: const LoginMobileView(),
        tablet: const LoginTabView(),
      ),
    );
  }
}
