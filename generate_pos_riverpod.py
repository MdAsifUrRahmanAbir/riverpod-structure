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
        "auth": {
            "data": ["models/user_model.dart", "repositories/auth_repository.dart"],
            "presentation": {
                "controllers": ["auth_controller.dart"],
                "screens": ["login_screen.dart"],
                "widgets": ["login_mobile_view.dart", "login_tab_view.dart"]
            }
        },
        "products": {
            "data": ["models/product_model.dart", "repositories/product_repository.dart"],
            "presentation": {
                "controllers": ["product_controller.dart"],
                "screens": ["product_list_screen.dart"],
                "widgets": ["product_list_mobile_view.dart", "product_list_tab_view.dart", "product_card_item.dart"]
            }
        },
        "cart": {
            "data": ["models/cart_item_model.dart"],
            "presentation": {
                "controllers": ["cart_controller.dart"],
                "screens": ["cart_screen.dart"],
                "widgets": ["cart_mobile_view.dart", "cart_tab_view.dart", "cart_item_tile.dart"]
            }
        },
        "checkout": {
            "data": ["models/invoice_model.dart", "repositories/checkout_repository.dart"],
            "presentation": {
                "controllers": ["checkout_controller.dart"],
                "screens": ["checkout_screen.dart"],
                "widgets": ["checkout_mobile_view.dart", "checkout_tab_view.dart", "receipt_preview.dart"]
            }
        }
    },
    "routes": ["app_router.dart", "route_names.dart"]
}

# =========================================================
# System Templates (DI, Network, Endpoints, Router)
# =========================================================

# 1. API Endpoints
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

# 2. API Client — single clean provider, no duplication
API_CLIENT_TEMPLATE = """import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/constants/api_endpoints.dart';
import 'package:%(pkg)s/core/network/api_exception.dart';

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
""" % {"pkg": PACKAGE_NAME}

# 3. API Exception
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

# 4. DI Container — references api_client provider (no re-declaration)
DI_CONTAINER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/network/api_client.dart';

// Re-export providers for convenience
export 'package:%(pkg)s/core/network/api_client.dart' show apiClientProvider;
""" % {"pkg": PACKAGE_NAME}

# 5. Route Names
ROUTE_NAMES_TEMPLATE = """class RouteNames {
  static const String login = '/login';
  static const String products = '/products';
  static const String cart = '/cart';
  static const String checkout = '/checkout';
}
"""

# 6. App Router (GoRouter) — package imports
APP_ROUTER_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:%(pkg)s/routes/route_names.dart';
import 'package:%(pkg)s/features/auth/presentation/screens/login_screen.dart';
import 'package:%(pkg)s/features/products/presentation/screens/product_list_screen.dart';
import 'package:%(pkg)s/features/cart/presentation/screens/cart_screen.dart';
import 'package:%(pkg)s/features/checkout/presentation/screens/checkout_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: RouteNames.products,
    routes: [
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
""" % {"pkg": PACKAGE_NAME}

# 7. App Colors
APP_COLORS_TEMPLATE = """import 'package:flutter/material.dart';

class AppColors {
  static const Color primary = Color(0xFF6C63FF);
  static const Color primaryDark = Color(0xFF4B44CC);
  static const Color primaryLight = Color(0xFFEAE9FF);
  static const Color accent = Color(0xFF00C896);
  static const Color background = Color(0xFFF5F5F7);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color textPrimary = Color(0xFF1C1C1E);
  static const Color textSecondary = Color(0xFF636366);
  static const Color textHint = Color(0xFFAEAEB2);
  static const Color success = Color(0xFF34C759);
  static const Color warning = Color(0xFFFF9F0A);
  static const Color error = Color(0xFFFF3B30);
  static const Color info = Color(0xFF007AFF);
  static const Color border = Color(0xFFE5E5EA);
}
"""

# 8. App Strings
APP_STRINGS_TEMPLATE = """class AppStrings {
  static const String appName = 'POS App';
  static const String login = 'Login';
  static const String logout = 'Logout';
  static const String products = 'Products';
  static const String cart = 'Cart';
  static const String checkout = 'Checkout';
  static const String errorOccurred = 'Something went wrong. Please try again.';
}
"""

# 9. App Sizes
APP_SIZES_TEMPLATE = """class AppSizes {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double radiusMd = 12;
  static const double radiusLg = 16;
  static const double fontMd = 15;
  static const double fontLg = 17;
  static const double buttonHeight = 52;
  static const double mobileBreakpoint = 650;
}
"""

# 10. App Theme
APP_THEME_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:%(pkg)s/core/constants/app_colors.dart';
import 'package:%(pkg)s/core/constants/app_sizes.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: AppColors.primary),
      scaffoldBackgroundColor: AppColors.background,
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.surface,
        foregroundColor: AppColors.textPrimary,
        elevation: 0,
      ),
    );
  }
}
""" % {"pkg": PACKAGE_NAME}

# 11. Screen Template
SCREEN_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/utils/responsive.dart';
import 'package:%(pkg)s/features/{feature_path}/presentation/widgets/{base_name}_mobile_view.dart';
import 'package:%(pkg)s/features/{feature_path}/presentation/widgets/{base_name}_tab_view.dart';

class {classname} extends ConsumerWidget {
  const {classname}({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    return Scaffold(
      body: Responsive(
        mobile: {classname}MobileView(),
        tablet: {classname}TabView(),
      ),
    );
  }}
}
""" % {"pkg": PACKAGE_NAME}

# 12. View Widgets Template
VIEW_WIDGET_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class {classname} extends ConsumerWidget {
  const {classname}({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return const Center(
      child: Text('{classname}'),
    );
  }
}
"""

# 13. Repository Template
REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/network/api_client.dart';

final {provider_name} = Provider<{classname}>((ref) {
  return {classname}(ref.watch(apiClientProvider));
});

class {classname} {
  final ApiClient _apiClient;
  {classname}(this._apiClient);
}
""" % {"pkg": PACKAGE_NAME}

# 14. Controller Template
CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';

class {classname} extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }
}

final {provider_name} = NotifierProvider<{classname}, AsyncValue<void>>({classname}.new);
"""

# 15. Model Templates
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

CART_ITEM_MODEL_TEMPLATE = """import 'package:%(pkg)s/features/products/data/models/product_model.dart';

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
""" % {"pkg": PACKAGE_NAME}

INVOICE_MODEL_TEMPLATE = """import 'package:%(pkg)s/features/cart/data/models/cart_item_model.dart';

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
""" % {"pkg": PACKAGE_NAME}

# 16-22 are specific controllers/repos which we will keep mostly as is but fix imports
AUTH_REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/network/api_client.dart';
import 'package:%(pkg)s/features/auth/data/models/user_model.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) => AuthRepository(ref.watch(apiClientProvider)));

class AuthRepository {
  final ApiClient _apiClient;
  AuthRepository(this._apiClient);

  Future<UserModel> login(String email, String password) async {
    return UserModel(id: '1', name: 'User', email: email);
  }
}
""" % {"pkg": PACKAGE_NAME}

AUTH_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/features/auth/data/models/user_model.dart';

class AuthController extends Notifier<AsyncValue<UserModel?>> {
  @override
  AsyncValue<UserModel?> build() => const AsyncValue.data(null);
}

final authControllerProvider = NotifierProvider<AuthController, AsyncValue<UserModel?>>(AuthController.new);
""" % {"pkg": PACKAGE_NAME}

PRODUCT_REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/network/api_client.dart';
import 'package:%(pkg)s/features/products/data/models/product_model.dart';

final productRepositoryProvider = Provider<ProductRepository>((ref) => ProductRepository(ref.watch(apiClientProvider)));

class ProductRepository {
  final ApiClient _apiClient;
  ProductRepository(this._apiClient);
}
""" % {"pkg": PACKAGE_NAME}

PRODUCT_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/features/products/data/models/product_model.dart';

class ProductController extends Notifier<AsyncValue<List<ProductModel>>> {
  @override
  AsyncValue<List<ProductModel>> build() => const AsyncValue.data([]);
}

final productControllerProvider = NotifierProvider<ProductController, AsyncValue<List<ProductModel>>>(ProductController.new);
""" % {"pkg": PACKAGE_NAME}

CART_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/features/cart/data/models/cart_item_model.dart';

class CartController extends Notifier<List<CartItemModel>> {
  @override
  List<CartItemModel> build() => [];
}

final cartControllerProvider = NotifierProvider<CartController, List<CartItemModel>>(CartController.new);
""" % {"pkg": PACKAGE_NAME}

CHECKOUT_REPOSITORY_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/network/api_client.dart';

final checkoutRepositoryProvider = Provider<CheckoutRepository>((ref) => CheckoutRepository(ref.watch(apiClientProvider)));

class CheckoutRepository {
  final ApiClient _apiClient;
  CheckoutRepository(this._apiClient);
}
""" % {"pkg": PACKAGE_NAME}

CHECKOUT_CONTROLLER_TEMPLATE = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/features/checkout/data/models/invoice_model.dart';

class CheckoutController extends Notifier<AsyncValue<InvoiceModel?>> {
  @override
  AsyncValue<InvoiceModel?> build() => const AsyncValue.data(null);
}

final checkoutControllerProvider = NotifierProvider<CheckoutController, AsyncValue<InvoiceModel?>>(CheckoutController.new);
""" % {"pkg": PACKAGE_NAME}

# 23-24
CURRENCY_FORMATTER_TEMPLATE = """class CurrencyFormatter {
  static String format(double amount) => '\$${amount.toStringAsFixed(2)}';
}
"""

DATE_FORMATTER_TEMPLATE = """class DateFormatter {
  static String format(DateTime date) => date.toIso8601String();
}
"""

MAIN_DART_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:%(pkg)s/core/theme/app_theme.dart';
import 'package:%(pkg)s/routes/app_router.dart';

void main() {
  runApp(const ProviderScope(child: PosApp()));
}

class PosApp extends ConsumerWidget {
  const PosApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    return MaterialApp.router(
      title: 'POS App',
      theme: AppTheme.lightTheme,
      routerConfig: router,
    );
  }
}
""" % {"pkg": PACKAGE_NAME}

# =========================================================
# Common Widget Templates
# =========================================================
COMMON_WIDGET_TEMPLATES = {
    "primary_button.dart": "import 'package:flutter/material.dart';\n\nclass PrimaryButton extends StatelessWidget { const PrimaryButton({super.key}); @override Widget build(BuildContext context) => const ElevatedButton(onPressed: null, child: Text('Button')); }",
    "primary_input_field.dart": "import 'package:flutter/material.dart';\n\nclass PrimaryInputField extends StatelessWidget { const PrimaryInputField({super.key}); @override Widget build(BuildContext context) => const TextField(); }",
    "primary_checkbox.dart": "import 'package:flutter/material.dart';\n\nclass PrimaryCheckbox extends StatelessWidget { const PrimaryCheckbox({super.key}); @override Widget build(BuildContext context) => const Checkbox(value: false, onChanged: null); }",
    "custom_loader.dart": "import 'package:flutter/material.dart';\n\nclass CustomLoader extends StatelessWidget { const CustomLoader({super.key}); @override Widget build(BuildContext context) => const CircularProgressIndicator(); }",
    "custom_shimmer.dart": "import 'package:flutter/material.dart';\n\nclass CustomShimmer extends StatelessWidget { const CustomShimmer({super.key}); @override Widget build(BuildContext context) => const SizedBox(); }",
    "custom_snackbar.dart": "import 'package:flutter/material.dart';\n\nclass CustomSnackbar { static void show(BuildContext context, String message) {} }",
    "custom_dialog.dart": "import 'package:flutter/material.dart';\n\nclass CustomDialog { static void show(BuildContext context) {} }",
    "custom_alert_dialog.dart": "import 'package:flutter/material.dart';\n\nclass CustomAlertDialog { static void show(BuildContext context) {} }",
    "responsive.dart": """import 'package:flutter/material.dart';
import 'package:%(pkg)s/core/constants/app_sizes.dart';

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
""" % {"pkg": PACKAGE_NAME},
}

SPECIFIC_FILE_TEMPLATES = {
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

def infer_feature_path(file_path):
    parts = file_path.replace("\\", "/").split("/")
    if "features" in parts:
        idx = parts.index("features")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return ""

def create_file(file_path, overwrite=False):
    if os.path.exists(file_path) and not overwrite:
        print(f"  ⏭  Skipped (exists): {file_path}")
        return

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    filename = os.path.basename(file_path)
    classname = format_class_name(filename)
    feature_path = infer_feature_path(file_path)

    if filename in SPECIFIC_FILE_TEMPLATES:
        content = SPECIFIC_FILE_TEMPLATES[filename]
    elif filename in COMMON_WIDGET_TEMPLATES:
        content = COMMON_WIDGET_TEMPLATES[filename]
    elif filename.endswith("_screen.dart"):
        base_name = filename.replace("_screen.dart", "")
        content = (
            SCREEN_TEMPLATE
            .replace("{classname}", classname)
            .replace("{feature_path}", feature_path)
            .replace("{base_name}", base_name)
        )
    elif any(filename.endswith(s) for s in ["_view.dart", "_widget.dart", "_item.dart", "_preview.dart", "_tile.dart", "_card_item.dart"]):
        content = VIEW_WIDGET_TEMPLATE.format(classname=classname)
    elif "repository.dart" in filename:
        provider_name = classname[0].lower() + classname[1:] + "Provider"
        content = REPOSITORY_TEMPLATE.format(classname=classname, provider_name=provider_name)
    elif "controller.dart" in filename:
        provider_name = classname[0].lower() + classname[1:] + "Provider"
        content = CONTROLLER_TEMPLATE.format(classname=classname, provider_name=provider_name)
    else:
        content = f"// TODO: Implement {filename}\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    action = "Updated" if os.path.exists(file_path) else "Created"
    print(f"  ✅ {action}: {file_path}")

def generate_structure(base_path, struct_dict, overwrite=False):
    for key, val in struct_dict.items():
        current_path = os.path.join(base_path, key)
        if isinstance(val, dict):
            generate_structure(current_path, val, overwrite)
        elif isinstance(val, list):
            for file in val:
                create_file(os.path.join(current_path, file), overwrite=overwrite)

if __name__ == "__main__":
    overwrite = "--overwrite" in sys.argv or "-o" in sys.argv or True # Default to True for this fix session
    print("🚀 Generating POS Clean Architecture...")
    generate_structure(LIB_PATH, structure, overwrite=overwrite)
    with open(os.path.join(LIB_PATH, "main.dart"), "w", encoding="utf-8") as f:
        f.write(MAIN_DART_TEMPLATE)
    print("\n🎉 Done!")
