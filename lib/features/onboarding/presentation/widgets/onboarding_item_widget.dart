import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class OnboardingItemWidget extends ConsumerWidget {
  const OnboardingItemWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: Text('OnboardingItemWidget'),
    );
  }
}
