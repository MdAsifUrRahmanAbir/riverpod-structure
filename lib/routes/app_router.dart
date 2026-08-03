import 'package:untitled2/features/inventory/presentation/screens/inventory_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:untitled2/routes/route_names.dart';
import 'package:untitled2/features/onboarding/presentation/screens/splash_screen.dart';
import 'package:untitled2/features/onboarding/presentation/screens/onboarding_screen.dart';
import 'package:untitled2/features/onboarding/presentation/screens/welcome_screen.dart';
import 'package:untitled2/features/auth/presentation/screens/login_screen.dart';
import 'package:untitled2/features/products/presentation/screens/product_list_screen.dart';
import 'package:untitled2/features/cart/presentation/screens/cart_screen.dart';
import 'package:untitled2/features/checkout/presentation/screens/checkout_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: RouteNames.splash,
    routes: [
      GoRoute(
        path: RouteNames.splash,
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: RouteNames.onboarding,
        builder: (context, state) => const OnboardingScreen(),
      ),
      GoRoute(
        path: RouteNames.welcome,
        builder: (context, state) => const WelcomeScreen(),
      ),
      GoRoute(
        path: RouteNames.login,
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: RouteNames.products,
        builder: (context, state) => const ProductListScreen(),
      ),
      GoRoute(
        path: RouteNames.cart,
        builder: (context, state) => const CartScreen(),
      ),
      GoRoute(
        path: RouteNames.checkout,
        builder: (context, state) => const CheckoutScreen(),
      ),
      GoRoute(
        path: RouteNames.inventory,
        builder: (context, state) => const InventoryScreen(),
      ),
  ],
  );
});
