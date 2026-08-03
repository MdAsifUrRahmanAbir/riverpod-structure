import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:untitled2/core/constants/app_colors.dart';
import 'package:untitled2/core/constants/app_sizes.dart';
import 'package:untitled2/core/constants/app_strings.dart';
import 'package:untitled2/routes/route_names.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppSizes.lg),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              const Icon(Icons.rocket_launch, size: 90, color: AppColors.primary),
              const SizedBox(height: AppSizes.lg),
              Text(
                AppStrings.welcomeTitle,
                style: Theme.of(context).textTheme.displayLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSizes.md),
              Text(
                AppStrings.welcomeSubtitle,
                style: Theme.of(context).textTheme.bodySmall,
                textAlign: TextAlign.center,
              ),
              const Spacer(),
              ElevatedButton(
                onPressed: () => context.go(RouteNames.login),
                child: const Text(AppStrings.login),
              ),
              const SizedBox(height: AppSizes.md),
              OutlinedButton(
                onPressed: () => context.go(RouteNames.products),
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size.fromHeight(AppSizes.buttonHeight),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(AppSizes.radiusMd),
                  ),
                ),
                child: const Text('Continue as Guest'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
