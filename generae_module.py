import os
import re

ROOT = os.getcwd()
LIB_PATH = os.path.join(ROOT, "lib")

def format_class_name(name):
    """Convert snake_case or clean string to PascalCase (e.g., product_list -> ProductList)"""
    words = name.replace("-", "_").split("_")
    return "".join([w.capitalize() for w in words])

def format_snake_case(name):
    """Convert PascalCase or space string to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def append_to_file(file_path, target_pattern, insertion_text):
    """Helper to inject new routes and DI into existing files without overwriting"""
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if insertion_text.strip() in content:
        print(f"⚠️ Notice: Route/DI already exists in {os.path.basename(file_path)}")
        return

    # Insert right before the closing target bracket/pattern
    if target_pattern in content:
        new_content = content.replace(target_pattern, f"{insertion_text}\n  {target_pattern}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"🔄 Updated: {os.path.basename(file_path)}")

def create_module(module_raw_name):
    module_snake = format_snake_case(module_raw_name)
    class_prefix = format_class_name(module_snake)

    feature_dir = os.path.join(LIB_PATH, "features", module_snake)

    # File Paths
    model_path = os.path.join(feature_dir, "data", "models", f"{module_snake}_model.dart")
    repo_path = os.path.join(feature_dir, "data", "repositories", f"{module_snake}_repository.dart")
    controller_path = os.path.join(feature_dir, "presentation", "controllers", f"{module_snake}_controller.dart")
    screen_path = os.path.join(feature_dir, "presentation", "screens", f"{module_snake}_screen.dart")
    mobile_view_path = os.path.join(feature_dir, "presentation", "widgets", f"{module_snake}_mobile_view.dart")
    tab_view_path = os.path.join(feature_dir, "presentation", "widgets", f"{module_snake}_tab_view.dart")

    # =========================================================
    # Code Templates
    # =========================================================
    model_code = f"""class {class_prefix}Model {{
  final String? id;

  {class_prefix}Model({{this.id}});

  factory {class_prefix}Model.fromJson(Map<String, dynamic> json) {{
    return {class_prefix}Model(
      id: json['id'],
    );
  }}

  Map<String, dynamic> toJson() => {{
    'id': id,
  }};
}}
"""

    repo_code = f"""import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/api_client.dart';
import '../../../core/constants/api_endpoints.dart';

final {module_snake}RepositoryProvider = Provider<{class_prefix}Repository>((ref) {{
  return {class_prefix}Repository(ref.watch(apiClientProvider));
}});

class {class_prefix}Repository {{
  final ApiClient _apiClient;

  {class_prefix}Repository(this._apiClient);

  // Future<dynamic> fetch{class_prefix}Data() async {{
  //   final response = await _apiClient.get(ApiEndpoints.baseUrl);
  //   return response.data;
  // }}
}}
"""

    controller_code = f"""import 'package:flutter_riverpod/flutter_riverpod.dart';

class {class_prefix}Controller extends StateNotifier<AsyncValue<void>> {{
  {class_prefix}Controller() : super(const AsyncValue.data(null));
}}

final {module_snake}ControllerProvider = StateNotifierProvider<{class_prefix}Controller, AsyncValue<void>>((ref) {{
  return {class_prefix}Controller();
}});
"""

    screen_code = f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/utils/responsive.dart';
import '../widgets/{module_snake}_mobile_view.dart';
import '../widgets/{module_snake}_tab_view.dart';

class {class_prefix}Screen extends ConsumerWidget {{
  const {class_prefix}Screen({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    return const Scaffold(
      body: Responsive(
        mobile: {class_prefix}MobileView(),
        tablet: {class_prefix}TabView(),
      ),
    );
  }}
}}
"""

    view_widget_code = lambda device: f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class {class_prefix}{device}View extends ConsumerWidget {{
  const {class_prefix}{device}View({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_prefix} {device}'),
      ),
      body: const Center(
        child: Text('{class_prefix} {device} View'),
      ),
    );
  }}
}}
"""

    # Create All Files
    files_to_create = {
        model_path: model_code,
        repo_path: repo_code,
        controller_path: controller_code,
        screen_path: screen_code,
        mobile_view_path: view_widget_code("Mobile"),
        tab_view_path: view_widget_code("Tab"),
    }

    for path, content in files_to_create.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Created: {os.path.relpath(path, ROOT)}")

    # =========================================================
    # Auto Inject to Route Names & App Router
    # =========================================================
    route_names_path = os.path.join(LIB_PATH, "routes", "route_names.dart")
    app_router_path = os.path.join(LIB_PATH, "routes", "app_router.dart")

    # 1. Inject Route Constant
    route_const_line = f"static const String {module_snake} = '/{module_snake}';"
    append_to_file(route_names_path, "}", f"  {route_const_line}")

    # 2. Inject GoRoute to Router Config
    go_route_code = f"""GoRoute(
        path: RouteNames.{module_snake},
        builder: (context, state) => const {class_prefix}Screen(),
      ),"""

    # Add screen import at the top of app_router.dart if missing
    import_statement = f"import '../features/{module_snake}/presentation/screens/{module_snake}_screen.dart';\n"
    if os.path.exists(app_router_path):
        with open(app_router_path, "r", encoding="utf-8") as f:
            router_content = f.read()

        if import_statement not in router_content:
            router_content = import_statement + router_content

        with open(app_router_path, "w", encoding="utf-8") as f:
            f.write(router_content)

    append_to_file(app_router_path, "],", f"      {go_route_code}")

    print(f"\n🎉 Module '{class_prefix}' Generated & Routes Configured Successfully!")

if __name__ == "__main__":
    print("=======================================")
    print("🚀 Flutter Riverpod Feature Module Generator")
    print("=======================================")
    module_input = input("Enter new Screen/Feature Name (e.g. inventory / supplier / customer_orders): ").strip()

    if module_input:
        create_module(module_input)
        print("\n👉 Run `dart format lib/` to clean formatting.")
    else:
        print("❌ Error: Module name cannot be empty.")