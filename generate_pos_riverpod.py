import os
import sys

ROOT = os.getcwd()
LIB_PATH = os.path.join(ROOT, "lib")
PACKAGE_NAME = "untitled2"  # Change this to your actual package name

# =========================================================
# Feature-First Architecture + DI + API + Router Structure
# =========================================================
structure = {
    "core": {
        "constants": ["app_colors.dart", "app_strings.dart", "app_sizes.dart", "api_endpoints.dart"],
        "network": ["api_client.dart", "api_exception.dart"],
        "di": ["injection_container.dart"],
        "theme": ["app_theme.dart"],
        "utils": ["responsive.dart", "currency_formatter.dart", "date_formatter.dart"],
        "widgets": [
            "primary_button.dart",
            "primary_input_field.dart",
            "primary_checkbox.dart",
            "custom_loader.dart",
            "custom_shimmer.dart",
            "custom_snackbar.dart",
            "custom_dialog.dart",
            "custom_alert_dialog.dart",
        ]
    },
    "features": {
        "onboarding": {
            "data": ["models/onboarding_model.dart"],
            "presentation": {
                "controllers": ["onboarding_controller.dart"],
                "screens": [
                    "splash_screen.dart",
                    "onboarding_screen.dart",
                    "welcome_screen.dart"
                ],
                "widgets": ["onboarding_item_widget.dart"]
            }
        },
        "auth": {
            "data": ["models/user_model.dart", "repositories/auth_repository.dart"],
            "presentation": {
                "controllers": ["auth_controller.dart"],
                "screens": ["login_screen.dart", "login_mobile_view.dart", "login_tab_view.dart"],
                "widgets": []
            }
        },
        "products": {
            "data": ["models/product_model.dart", "repositories/product_repository.dart"],
            "presentation": {
                "controllers": ["product_controller.dart"],
                "screens": ["product_list_screen.dart", "product_list_mobile_view.dart", "product_list_tab_view.dart"],
                "widgets": ["product_card_item.dart"]
            }
        },
        "cart": {
            "data": ["models/cart_item_model.dart"],
            "presentation": {
                "controllers": ["cart_controller.dart"],
                "screens": ["cart_screen.dart", "cart_mobile_view.dart", "cart_tab_view.dart"],
                "widgets": ["cart_item_tile.dart"]
            }
        },
        "checkout": {
            "data": ["models/invoice_model.dart", "repositories/checkout_repository.dart"],
            "presentation": {
                "controllers": ["checkout_controller.dart"],
                "screens": ["checkout_screen.dart", "checkout_mobile_view.dart", "checkout_tab_view.dart"],
                "widgets": ["receipt_preview.dart"]
            }
        }
    },
    "routes": ["app_router.dart", "route_names.dart"]
}

# =========================================================
# System Templates (Using safe token replacement)
# =========================================================

API_ENDPOINTS_TEMPLATE = """class ApiEndpoints {
  static const String baseUrl = "https://api.yourposapp.com/v1";

  // Auth
  static const String login = "/auth/login";
  static const String register = "/auth/register";

  // Products
  static const String products = "/products";
  static String productDetails(String id) => "/products/$id";

  // Cart & Checkout
  static const String checkout = "/orders/checkout";
  static const String invoices = "/invoices";
}
"""

API_CLIENT_TEMPLATE = """import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/constants/api_endpoints.dart';
import 'package:__PACKAGE_NAME__/core/network/api_exception.dart';

final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());

class ApiClient {
  late final Dio _dio;

  ApiClient() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiEndpoints.baseUrl,
        connectTimeout: const Duration(seconds: 15),
        receiveTimeout: const Duration(seconds: 15),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.add(InterceptorsWrapper(
      onError: (DioException e, handler) {
        handler.next(e);
      },
    ));
  }

  Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) async {
    try {
      return await _dio.get(path, queryParameters: queryParameters);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  Future<Response> post(String path, {dynamic data, Map<String, dynamic>? queryParameters}) async {
    try {
      return await _dio.post(path, data: data, queryParameters: queryParameters);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  Future<Response> put(String path, {dynamic data}) async {
    try {
      return await _dio.put(path, data: data);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  Future<Response> delete(String path, {dynamic data}) async {
    try {
      return await _dio.delete(path, data: data);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }
}
"""

API_EXCEPTION_TEMPLATE = """import 'package:dio/dio.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;

  const ApiException({required this.message, this.statusCode});

  factory ApiException.fromDioError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.sendTimeout:
        return const ApiException(message: 'Connection timed out. Please try again.');
      case DioExceptionType.badResponse:
        return ApiException(
          message: e.response?.data?['message'] ?? 'Server error occurred.',
          statusCode: e.response?.statusCode,
        );
      case DioExceptionType.connectionError:
        return const ApiException(message: 'No internet connection.');
      default:
        return const ApiException(message: 'An unexpected error occurred.');
    }
  }

  @override
  String toString() => 'ApiException: $message (status: $statusCode)';
}
"""

DI_CONTAINER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/network/api_client.dart';

export 'package:__PACKAGE_NAME__/core/network/api_client.dart' show apiClientProvider;
"""

ROUTE_NAMES_TEMPLATE = """class RouteNames {
  static const String splash = '/';
  static const String onboarding = '/onboarding';
  static const String welcome = '/welcome';
  static const String login = '/login';
  static const String products = '/products';
  static const String cart = '/cart';
  static const String checkout = '/checkout';
}
"""

APP_ROUTER_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:__PACKAGE_NAME__/routes/route_names.dart';
import 'package:__PACKAGE_NAME__/features/onboarding/presentation/screens/splash_screen.dart';
import 'package:__PACKAGE_NAME__/features/onboarding/presentation/screens/onboarding_screen.dart';
import 'package:__PACKAGE_NAME__/features/onboarding/presentation/screens/welcome_screen.dart';
import 'package:__PACKAGE_NAME__/features/auth/presentation/screens/login_screen.dart';
import 'package:__PACKAGE_NAME__/features/products/presentation/screens/product_list_screen.dart';
import 'package:__PACKAGE_NAME__/features/cart/presentation/screens/cart_screen.dart';
import 'package:__PACKAGE_NAME__/features/checkout/presentation/screens/checkout_screen.dart';

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
    ],
  );
});
"""

APP_COLORS_TEMPLATE = """import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  static const Color primary = Color(0xFF6C63FF);
  static const Color primaryDark = Color(0xFF4B44CC);
  static const Color primaryLight = Color(0xFFEAE9FF);

  static const Color accent = Color(0xFF00C896);
  static const Color accentLight = Color(0xFFE6F9F5);

  static const Color background = Color(0xFFF5F5F7);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceDark = Color(0xFF1C1C1E);

  static const Color textPrimary = Color(0xFF1C1C1E);
  static const Color textSecondary = Color(0xFF636366);
  static const Color textHint = Color(0xFFAEAEB2);
  static const Color textWhite = Color(0xFFFFFFFF);

  static const Color success = Color(0xFF34C759);
  static const Color warning = Color(0xFFFF9F0A);
  static const Color error = Color(0xFFFF3B30);
  static const Color info = Color(0xFF007AFF);

  static const Color border = Color(0xFFE5E5EA);
  static const Color divider = Color(0xFFF2F2F7);

  static const Color shimmerBase = Color(0xFFE0E0E0);
  static const Color shimmerHighlight = Color(0xFFF5F5F5);
}
"""

APP_STRINGS_TEMPLATE = """class AppStrings {
  AppStrings._();

  static const String appName = 'POS App';
  static const String welcomeTitle = 'Welcome to POS App';
  static const String welcomeSubtitle = 'Manage your sales, products, and receipts seamlessly.';
  static const String getStarted = 'Get Started';
  static const String login = 'Login';
  static const String logout = 'Logout';
  static const String products = 'Products';
  static const String cart = 'Cart';
  static const String checkout = 'Checkout';
  static const String skip = 'Skip';
  static const String next = 'Next';
  static const String errorOccurred = 'Something went wrong. Please try again.';
}
"""

APP_SIZES_TEMPLATE = """class AppSizes {
  AppSizes._();

  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;

  static const double radiusSm = 8.0;
  static const double radiusMd = 12.0;
  static const double radiusLg = 16.0;
  static const double radiusXl = 24.0;
  static const double radiusFull = 100.0;

  static const double iconSm = 16.0;
  static const double iconMd = 24.0;
  static const double iconLg = 32.0;

  static const double fontXs = 11.0;
  static const double fontSm = 13.0;
  static const double fontMd = 15.0;
  static const double fontLg = 17.0;
  static const double fontXl = 20.0;
  static const double fontXxl = 24.0;
  static const double fontDisplay = 32.0;

  static const double buttonHeight = 52.0;
  static const double inputHeight = 52.0;
  static const double appBarHeight = 56.0;
  static const double bottomNavBarHeight = 64.0;

  static const double mobileBreakpoint = 650.0;
  static const double tabletBreakpoint = 1100.0;
}
"""

APP_THEME_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_colors.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_sizes.dart';

class AppTheme {
  AppTheme._();

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: AppColors.surface,
        error: AppColors.error,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: AppColors.background,
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.surface,
        foregroundColor: AppColors.textPrimary,
        elevation: 0,
        scrolledUnderElevation: 0.5,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: AppColors.textPrimary,
          fontSize: AppSizes.fontLg,
          fontWeight: FontWeight.w600,
        ),
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: AppSizes.fontDisplay,
          fontWeight: FontWeight.bold,
          color: AppColors.textPrimary,
        ),
        titleLarge: TextStyle(
          fontSize: AppSizes.fontXl,
          fontWeight: FontWeight.w600,
          color: AppColors.textPrimary,
        ),
        bodyLarge: TextStyle(
          fontSize: AppSizes.fontLg,
          color: AppColors.textPrimary,
        ),
        bodyMedium: TextStyle(
          fontSize: AppSizes.fontMd,
          color: AppColors.textPrimary,
        ),
        bodySmall: TextStyle(
          fontSize: AppSizes.fontSm,
          color: AppColors.textSecondary,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(AppSizes.buttonHeight),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          ),
          textStyle: const TextStyle(
            fontSize: AppSizes.fontMd,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }
}
"""

# =========================================================
# New Onboarding Feature Templates
# =========================================================

ONBOARDING_MODEL_TEMPLATE = """class OnboardingModel {
  final String title;
  final String description;
  final String imagePath;

  const OnboardingModel({
    required this.title,
    required this.description,
    required this.imagePath,
  });
}
"""

ONBOARDING_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/features/onboarding/data/models/onboarding_model.dart';

class OnboardingController extends Notifier<List<OnboardingModel>> {
  @override
  List<OnboardingModel> build() {
    return const [
      OnboardingModel(
        title: 'Manage Inventory',
        description: 'Track stock and product availability in real time.',
        imagePath: 'assets/images/onboarding1.png',
      ),
      OnboardingModel(
        title: 'Fast Checkout',
        description: 'Process transactions efficiently and print receipts.',
        imagePath: 'assets/images/onboarding2.png',
      ),
      OnboardingModel(
        title: 'Business Analytics',
        description: 'Gain valuable insights into daily sales and growth.',
        imagePath: 'assets/images/onboarding3.png',
      ),
    ];
  }
}

final onboardingControllerProvider =
    NotifierProvider<OnboardingController, List<OnboardingModel>>(OnboardingController.new);
"""

SPLASH_SCREEN_TEMPLATE = """import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_colors.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_strings.dart';
import 'package:__PACKAGE_NAME__/routes/route_names.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 3), () {
      if (mounted) {
        context.go(RouteNames.onboarding);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.primary,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.storefront, size: 80, color: Colors.white),
            SizedBox(height: 16),
            Text(
              AppStrings.appName,
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
"""

ONBOARDING_SCREEN_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_colors.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_sizes.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_strings.dart';
import 'package:__PACKAGE_NAME__/features/onboarding/presentation/controllers/onboarding_controller.dart';
import 'package:__PACKAGE_NAME__/routes/route_names.dart';

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
"""

WELCOME_SCREEN_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_colors.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_sizes.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_strings.dart';
import 'package:__PACKAGE_NAME__/routes/route_names.dart';

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
"""

SCREEN_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/utils/responsive.dart';
import '__BASE_NAME___mobile_view.dart';
import '__BASE_NAME___tab_view.dart';

class __CLASSNAME__ extends ConsumerWidget {
  const __CLASSNAME__({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Responsive(
        mobile: const __VIEW_CLASSNAME__MobileView(),
        tablet: const __VIEW_CLASSNAME__TabView(),
      ),
    );
  }
}
"""

VIEW_WIDGET_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class __CLASSNAME__ extends ConsumerWidget {
  const __CLASSNAME__({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: Text('__CLASSNAME__'),
    );
  }
}
"""

REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/network/api_client.dart';

final __PROVIDER_NAME__ = Provider<__CLASSNAME__>((ref) {
  return __CLASSNAME__(ref.watch(apiClientProvider));
});

class __CLASSNAME__ {
  final ApiClient _apiClient;
  __CLASSNAME__(this._apiClient);
}
"""

CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';

class __CLASSNAME__ extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }
}

final __PROVIDER_NAME__ = NotifierProvider<__CLASSNAME__, AsyncValue<void>>(__CLASSNAME__.new);
"""

USER_MODEL_TEMPLATE = """class UserModel {
  final String id;
  final String name;
  final String email;

  UserModel({required this.id, required this.name, required this.email});

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'email': email};
}
"""

PRODUCT_MODEL_TEMPLATE = """class ProductModel {
  final String id;
  final String name;
  final double price;

  ProductModel({required this.id, required this.name, required this.price});

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      price: (json['price'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'price': price};
}
"""

CART_ITEM_MODEL_TEMPLATE = """import 'package:__PACKAGE_NAME__/features/products/data/models/product_model.dart';

class CartItemModel {
  final ProductModel product;
  final int quantity;

  CartItemModel({required this.product, required this.quantity});

  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      product: ProductModel.fromJson(json['product']),
      quantity: json['quantity'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() => {'product': product.toJson(), 'quantity': quantity};
}
"""

INVOICE_MODEL_TEMPLATE = """import 'package:__PACKAGE_NAME__/features/cart/data/models/cart_item_model.dart';

class InvoiceModel {
  final String id;
  final List<CartItemModel> items;
  final double total;

  InvoiceModel({required this.id, required this.items, required this.total});

  factory InvoiceModel.fromJson(Map<String, dynamic> json) {
    return InvoiceModel(
      id: json['id'] ?? '',
      items: (json['items'] as List).map((e) => CartItemModel.fromJson(e)).toList(),
      total: (json['total'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'items': items.map((e) => e.toJson()).toList(),
    'total': total,
  };
}
"""

AUTH_REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/network/api_client.dart';
import 'package:__PACKAGE_NAME__/features/auth/data/models/user_model.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) => AuthRepository(ref.watch(apiClientProvider)));

class AuthRepository {
  final ApiClient _apiClient;
  AuthRepository(this._apiClient);

  Future<UserModel> login(String email, String password) async {
    return UserModel(id: '1', name: 'User', email: email);
  }
}
"""

AUTH_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/features/auth/data/models/user_model.dart';

class AuthController extends Notifier<AsyncValue<UserModel?>> {
  @override
  AsyncValue<UserModel?> build() => const AsyncValue.data(null);
}

final authControllerProvider = NotifierProvider<AuthController, AsyncValue<UserModel?>>(AuthController.new);
"""

PRODUCT_REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/network/api_client.dart';

final productRepositoryProvider = Provider<ProductRepository>((ref) => ProductRepository(ref.watch(apiClientProvider)));

class ProductRepository {
  final ApiClient _apiClient;
  ProductRepository(this._apiClient);
}
"""

PRODUCT_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/features/products/data/models/product_model.dart';

class ProductController extends Notifier<AsyncValue<List<ProductModel>>> {
  @override
  AsyncValue<List<ProductModel>> build() => const AsyncValue.data([]);
}

final productControllerProvider = NotifierProvider<ProductController, AsyncValue<List<ProductModel>>>(ProductController.new);
"""

CART_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/features/cart/data/models/cart_item_model.dart';

class CartController extends Notifier<List<CartItemModel>> {
  @override
  List<CartItemModel> build() => [];
}

final cartControllerProvider = NotifierProvider<CartController, List<CartItemModel>>(CartController.new);
"""

CHECKOUT_REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/network/api_client.dart';

final checkoutRepositoryProvider = Provider<CheckoutRepository>((ref) => CheckoutRepository(ref.watch(apiClientProvider)));

class CheckoutRepository {
  final ApiClient _apiClient;
  CheckoutRepository(this._apiClient);
}
"""

CHECKOUT_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/features/checkout/data/models/invoice_model.dart';

class CheckoutController extends Notifier<AsyncValue<InvoiceModel?>> {
  @override
  AsyncValue<InvoiceModel?> build() => const AsyncValue.data(null);
}

final checkoutControllerProvider = NotifierProvider<CheckoutController, AsyncValue<InvoiceModel?>>(CheckoutController.new);
"""

CURRENCY_FORMATTER_TEMPLATE = """class CurrencyFormatter {
  CurrencyFormatter._();

  static String format(double amount) => '\\${amount.toStringAsFixed(2)}';
}
"""

DATE_FORMATTER_TEMPLATE = """class DateFormatter {
  DateFormatter._();

  static String format(DateTime date) => date.toIso8601String();
}
"""

MAIN_DART_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:__PACKAGE_NAME__/core/theme/app_theme.dart';
import 'package:__PACKAGE_NAME__/routes/app_router.dart';

void main() {
  WidgetsBinding.instance.addPostFrameCallback((_) {});
  runApp(
    const ProviderScope(
      child: PosApp(),
    ),
  );
}

class PosApp extends ConsumerWidget {
  const PosApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'POS System',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      routerConfig: router,
    );
  }
}
"""

COMMON_WIDGET_TEMPLATES = {
    "primary_button.dart": "import 'package:flutter/material.dart';\n\nclass PrimaryButton extends StatelessWidget {\n  const PrimaryButton({super.key});\n\n  @override\n  Widget build(BuildContext context) => const ElevatedButton(onPressed: null, child: Text('Button'));\n}",
    "primary_input_field.dart": "import 'package:flutter/material.dart';\n\nclass PrimaryInputField extends StatelessWidget {\n  const PrimaryInputField({super.key});\n\n  @override\n  Widget build(BuildContext context) => const TextField();\n}",
    "primary_checkbox.dart": "import 'package:flutter/material.dart';\n\nclass PrimaryCheckbox extends StatelessWidget {\n  const PrimaryCheckbox({super.key});\n\n  @override\n  Widget build(BuildContext context) => const Checkbox(value: false, onChanged: null);\n}",
    "custom_loader.dart": "import 'package:flutter/material.dart';\n\nclass CustomLoader extends StatelessWidget {\n  const CustomLoader({super.key});\n\n  @override\n  Widget build(BuildContext context) => const CircularProgressIndicator();\n}",
    "custom_shimmer.dart": "import 'package:flutter/material.dart';\n\nclass CustomShimmer extends StatelessWidget {\n  const CustomShimmer({super.key});\n\n  @override\n  Widget build(BuildContext context) => const SizedBox();\n}",
    "custom_snackbar.dart": "import 'package:flutter/material.dart';\n\nclass CustomSnackbar {\n  CustomSnackbar._();\n  static void show(BuildContext context, String message) {}\n}",
    "custom_dialog.dart": "import 'package:flutter/material.dart';\n\nclass CustomDialog {\n  CustomDialog._();\n  static void show(BuildContext context) {}\n}",
    "custom_alert_dialog.dart": "import 'package:flutter/material.dart';\n\nclass CustomAlertDialog {\n  CustomAlertDialog._();\n  static void show(BuildContext context) {}\n}",
    "responsive.dart": """import 'package:flutter/material.dart';
import 'package:__PACKAGE_NAME__/core/constants/app_sizes.dart';

class Responsive extends StatelessWidget {
  final Widget mobile;
  final Widget tablet;
  const Responsive({super.key, required this.mobile, required this.tablet});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
      if (constraints.maxWidth >= AppSizes.mobileBreakpoint) return tablet;
      return mobile;
    });
  }
}
""",
}

SPECIFIC_FILE_TEMPLATES = {
    "onboarding_model.dart": ONBOARDING_MODEL_TEMPLATE,
    "onboarding_controller.dart": ONBOARDING_CONTROLLER_TEMPLATE,
    "splash_screen.dart": SPLASH_SCREEN_TEMPLATE,
    "onboarding_screen.dart": ONBOARDING_SCREEN_TEMPLATE,
    "welcome_screen.dart": WELCOME_SCREEN_TEMPLATE,
    "user_model.dart": USER_MODEL_TEMPLATE,
    "product_model.dart": PRODUCT_MODEL_TEMPLATE,
    "cart_item_model.dart": CART_ITEM_MODEL_TEMPLATE,
    "invoice_model.dart": INVOICE_MODEL_TEMPLATE,
    "auth_repository.dart": AUTH_REPOSITORY_TEMPLATE,
    "product_repository.dart": PRODUCT_REPOSITORY_TEMPLATE,
    "checkout_repository.dart": CHECKOUT_REPOSITORY_TEMPLATE,
    "auth_controller.dart": AUTH_CONTROLLER_TEMPLATE,
    "product_controller.dart": PRODUCT_CONTROLLER_TEMPLATE,
    "cart_controller.dart": CART_CONTROLLER_TEMPLATE,
    "checkout_controller.dart": CHECKOUT_CONTROLLER_TEMPLATE,
    "app_colors.dart": APP_COLORS_TEMPLATE,
    "app_strings.dart": APP_STRINGS_TEMPLATE,
    "app_sizes.dart": APP_SIZES_TEMPLATE,
    "api_endpoints.dart": API_ENDPOINTS_TEMPLATE,
    "api_client.dart": API_CLIENT_TEMPLATE,
    "api_exception.dart": API_EXCEPTION_TEMPLATE,
    "injection_container.dart": DI_CONTAINER_TEMPLATE,
    "app_theme.dart": APP_THEME_TEMPLATE,
    "currency_formatter.dart": CURRENCY_FORMATTER_TEMPLATE,
    "date_formatter.dart": DATE_FORMATTER_TEMPLATE,
    "route_names.dart": ROUTE_NAMES_TEMPLATE,
    "app_router.dart": APP_ROUTER_TEMPLATE,
}

# =========================================================
# Helpers
# =========================================================
def format_class_name(filename):
    base_name = filename.replace(".dart", "")
    return "".join([word.capitalize() for word in base_name.split("_")])

def apply_template_replacements(content, classname="", base_name="", view_classname=""):
    provider_name = classname[0].lower() + classname[1:] + "Provider" if classname else ""
    return (
        content
        .replace("__PACKAGE_NAME__", PACKAGE_NAME)
        .replace("__CLASSNAME__", classname)
        .replace("__BASE_NAME__", base_name)
        .replace("__VIEW_CLASSNAME__", view_classname)
        .replace("__PROVIDER_NAME__", provider_name)
    )

def create_file(file_path, overwrite=False):
    if os.path.exists(file_path) and not overwrite:
        print(f"  ⏭  Skipped (exists): {file_path}")
        return

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    filename = os.path.basename(file_path)
    classname = format_class_name(filename)

    if filename in SPECIFIC_FILE_TEMPLATES:
        content = SPECIFIC_FILE_TEMPLATES[filename]
    elif filename in COMMON_WIDGET_TEMPLATES:
        content = COMMON_WIDGET_TEMPLATES[filename]
    elif filename.endswith("_screen.dart"):
        base_name = filename.replace("_screen.dart", "")
        view_classname = "".join([w.capitalize() for w in base_name.split("_")])
        content = SCREEN_TEMPLATE
        content = apply_template_replacements(content, classname=classname, base_name=base_name, view_classname=view_classname)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Written: {file_path}")
        return
    elif any(filename.endswith(s) for s in ["_view.dart", "_widget.dart", "_item.dart", "_preview.dart", "_tile.dart", "_card_item.dart"]):
        content = VIEW_WIDGET_TEMPLATE
    elif "repository.dart" in filename:
        content = REPOSITORY_TEMPLATE
    elif "controller.dart" in filename:
        content = CONTROLLER_TEMPLATE
    else:
        content = f"// TODO: Implement {filename}\n"

    content = apply_template_replacements(content, classname=classname)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ Written: {file_path}")

def generate_structure(base_path, struct_dict, overwrite=False):
    for key, val in struct_dict.items():
        current_path = os.path.join(base_path, key)
        if isinstance(val, dict):
            generate_structure(current_path, val, overwrite)
        elif isinstance(val, list):
            for file in val:
                create_file(os.path.join(current_path, file), overwrite=overwrite)

if __name__ == "__main__":
    overwrite = "--overwrite" in sys.argv or "-o" in sys.argv or True
    print("🚀 Generating POS Clean Architecture with Onboarding Flow...")
    generate_structure(LIB_PATH, structure, overwrite=overwrite)

    main_content = apply_template_replacements(MAIN_DART_TEMPLATE)
    with open(os.path.join(LIB_PATH, "main.dart"), "w", encoding="utf-8") as f:
        f.write(main_content)
    print("\n🎉 Done!")