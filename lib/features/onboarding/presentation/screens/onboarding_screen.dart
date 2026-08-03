import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:untitled2/core/constants/app_colors.dart';
import 'package:untitled2/core/constants/app_sizes.dart';
import 'package:untitled2/core/constants/app_strings.dart';
import 'package:untitled2/features/onboarding/presentation/controllers/onboarding_controller.dart';
import 'package:untitled2/routes/route_names.dart';

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentIndex = 0;

  void _onFinish() {
    context.go(RouteNames.welcome);
  }

  @override
  Widget build(BuildContext context) {
    final onboardingList = ref.watch(onboardingControllerProvider);

    return Scaffold(
      appBar: AppBar(
        actions: [
          TextButton(
            onPressed: _onFinish,
            child: const Text(AppStrings.skip),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                itemCount: onboardingList.length,
                onPageChanged: (index) {
                  setState(() => _currentIndex = index);
                },
                itemBuilder: (context, index) {
                  final item = onboardingList[index];
                  return Padding(
                    padding: const EdgeInsets.all(AppSizes.lg),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.touch_app, size: 100, color: AppColors.primary),
                        const SizedBox(height: AppSizes.xl),
                        Text(
                          item.title,
                          style: Theme.of(context).textTheme.titleLarge,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: AppSizes.md),
                        Text(
                          item.description,
                          style: Theme.of(context).textTheme.bodySmall,
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(
                onboardingList.length,
                (index) => AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  margin: const EdgeInsets.symmetric(horizontal: 4),
                  height: 8,
                  width: _currentIndex == index ? 24 : 8,
                  decoration: BoxDecoration(
                    color: _currentIndex == index ? AppColors.primary : AppColors.border,
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(AppSizes.lg),
              child: ElevatedButton(
                onPressed: () {
                  if (_currentIndex == onboardingList.length - 1) {
                    _onFinish();
                  } else {
                    _pageController.nextPage(
                      duration: const Duration(milliseconds: 300),
                      curve: Curves.easeInOut,
                    );
                  }
                },
                child: Text(
                  _currentIndex == onboardingList.length - 1
                      ? AppStrings.getStarted
                      : AppStrings.next,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
