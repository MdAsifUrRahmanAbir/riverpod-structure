import os
import re

ROOT = os.getcwd()
LIB_PATH = os.path.join(ROOT, "lib")
PACKAGE_NAME = "untitled2"  # 👈 আপনার pubspec.yaml এর package name বসান

def format_class_name(name):
    """Convert snake_case or clean string to PascalCase (e.g., product_list -> ProductList)"""
    words = name.replace("-", "_").split("_")
    return "".join([w.capitalize() for w in words])

def format_snake_case(name):
    """Convert PascalCase or space string to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def safe_inject_route_name(file_path, route_name):
    """Inject route name constant safely before the last closing brace of RouteNames class"""
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    insertion = f"static const String {route_name} = '/{route_name}';"
    if insertion in content:
        print(f"⚠️ Notice: Route '{route_name}' already exists in route_names.dart")
        return

    # Find the last closing brace of the class
    last_brace_index = content.rfind("}")
    if last_brace_index != -1:
        new_content = (
            content[:last_brace_index]
            + f"  {insertion}\n"
            + content[last_brace_index:]
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"🔄 Updated: {os.path.basename(file_path)}")

def safe_inject_go_route(file_path, route_code, import_statement):
    """Inject GoRoute and Import statement into app_router.dart safely"""
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Import Statement if not present
    if import_statement.strip() not in content:
        content = import_statement + content

    # 2. Add GoRoute before the routes list closing bracket '];' or ']'
    if route_code.strip() in content:
        print(f"⚠️ Notice: Route definition already exists in app_router.dart")
        return

    target_pattern = "];"
    if target_pattern in content:
        content = content.replace(target_pattern, f"  {route_code}\n    {target_pattern}")
    else:
        # Fallback for trailing comma routes list
        target_pattern = "]"
        last_bracket = content.rfind("]")
        if last_bracket != -1:
            content = content[:last_bracket] + f"  {route_code}\n  " + content[last_bracket:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"🔄 Updated: {os.path.basename(file_path)}")

def create_module(module_raw_name):
    module_snake = format_snake_case(module_raw_name)
    class_prefix = format_class_name(module_snake)

    feature_dir = os.path.join(LIB_PATH, "features", module_snake)

    # Corrected File Paths (Widgets & Views in presentation/widgets or presentation/screens)
    model_path = os.path.join(feature_dir, "data", "models", f"{module_snake}_model.dart")
    repo_path = os.path.join(feature_dir, "data", "repositories", f"{module_snake}_repository.dart")
    controller_path = os.path.join(feature_dir, "presentation", "controllers", f"{module_snake}_controller.dart")
    screen_path = os.path.join(feature_dir, "presentation", "screens", f"{module_snake}_screen.dart")
    mobile_view_path = os.path.join(feature_dir, "presentation", "screens", f"{module_snake}_mobile_view.dart")
    tab_view_path = os.path.join(feature_dir, "presentation", "screens", f"{module_snake}_tab_view.dart")

    # =========================================================
    # Updated Code Templates
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
import 'package:{PACKAGE_NAME}/core/network/api_client.dart';

final {module_snake}RepositoryProvider = Provider<{class_prefix}Repository>((ref) {{
  return {class_prefix}Repository(ref.watch(apiClientProvider));
}});

class {class_prefix}Repository {{
  final ApiClient _apiClient;

  {class_prefix}Repository(this._apiClient);
}}
"""

    controller_code = f"""import 'package:flutter_riverpod/flutter_riverpod.dart';

class {class_prefix}Controller extends Notifier<AsyncValue<void>> {{
  @override
  AsyncValue<void> build() {{
    return const AsyncValue.data(null);
  }}
}}

final {module_snake}ControllerProvider = NotifierProvider<{class_prefix}Controller, AsyncValue<void>>({class_prefix}Controller.new);
"""

    screen_code = f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:{PACKAGE_NAME}/core/utils/responsive.dart';
import 'package:{PACKAGE_NAME}/features/{module_snake}/presentation/screens/{module_snake}_mobile_view.dart';
import 'package:{PACKAGE_NAME}/features/{module_snake}/presentation/screens/{module_snake}_tab_view.dart';

class {class_prefix}Screen extends ConsumerWidget {{
  const {class_prefix}Screen({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    return Scaffold(
      body: Responsive(
        mobile: const {class_prefix}MobileView(),
        tablet: const {class_prefix}TabView(),
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
    return Center(
      child: Text('{class_prefix} {device} View'),
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

    # 1. Safe Route Constant Injection
    safe_inject_route_name(route_names_path, module_snake)

    # 2. Safe Router Injection
    go_route_code = f"""GoRoute(
        path: RouteNames.{module_snake},
        builder: (context, state) => const {class_prefix}Screen(),
      ),"""
    import_statement = f"import 'package:{PACKAGE_NAME}/features/{module_snake}/presentation/screens/{module_snake}_screen.dart';\n"

    safe_inject_go_route(app_router_path, go_route_code, import_statement)

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