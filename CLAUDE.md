# CLAUDE.md - AI Coding Agent Guidelines

## 📌 PROJECT OVERVIEW & CONCEPT
A modern Flutter Point-of-Sale (POS) application built using Clean Architecture with a Feature-First modular structure. State management is powered by Riverpod 3.x with GoRouter for declarative routing and Dio for API integration.

## 🏗️ FOLDER & FEATURE STRUCTURE
```
lib/
├── core/
│   ├── constants/       # AppColors, AppSizes, AppStrings, ApiEndpoints
│   ├── di/              # Injection container & exports
│   ├── network/         # ApiClient (Dio), ApiException
│   ├── theme/           # AppTheme data
│   ├── utils/           # Responsive layout, Date/Currency formatters
│   └── widgets/         # Shared UI (PrimaryButton, InputField, Shimmer, Loader, Dialogs)
├── features/            # Feature-first modular structure
│   ├── auth/            # (models, repositories, controllers, screens, widgets)
│   ├── cart/            # (models, controllers, screens, widgets)
│   ├── checkout/        # (repositories, controllers, screens, widgets)
│   └── products/        # (models, repositories, controllers, screens, widgets)
├── routes/              # AppRouter (GoRouter), RouteNames
└── main.dart            # ProviderScope entry point
```

## 🛠️ TECH STACK & STATE MANAGEMENT RULES
- **State Management**: Modern Riverpod ONLY (`Notifier`, `AsyncNotifier`, `NotifierProvider`). Strictly NO `StateNotifier`, `StateProvider`, or `legacy.dart`.
- **Network & Data**: Inject `ApiClient` via `apiClientProvider`. Repositories wrap API calls. Controllers handle async mutation via `AsyncValue.guard()`.
- **UI Architecture**: Mobile vs Tablet layouts using `Responsive(mobile: ..., tablet: ...)`. All layout limits derive from `AppSizes` and `AppColors`.

## 📜 CODING CONVENTIONS & STRICT RULES
- **Private Constructors**: Constant and utility classes must use private constructors (e.g., `AppStrings._()`).
- **Constructor Tear-Offs**: Always use `.new` syntax for provider instantiations (e.g., `NotifierProvider<MyController, AsyncValue<void>>(MyController.new)`).
- **No Hardcoded Values**: All strings must use `AppStrings`, dimensions/padding must use `AppSizes`, colors must use `AppColors`.
- **Clean Imports**: Use package imports (`package:untitled2/...`). Avoid relative imports (`../../../../`). Remove unused imports.
- **Lean State**: Access `ref` directly inside Notifier methods (`ref.read(...)`). Do NOT pass `ref` to controller constructors.

## ⚡ COMMANDS & WORKFLOWS
- **Fetch Dependencies**: `flutter pub get`
- **Run Application**: `flutter run`
- **Analyze Code**: `flutter analyze`
- **Run Tests**: `flutter test`
- **Build Runner**: `dart run build_runner build --delete-conflicting-outputs`

## 🚫 WHAT NOT TO DO (AI Guardrails)
- ❌ Do NOT rewrite entire files when applying minor edits.
- ❌ Do NOT use deprecated Riverpod patterns (`StateNotifier`, `StateNotifierProvider`, `StateProvider`, `legacy.dart`).
- ❌ Do NOT introduce inline hardcoded strings, magic numbers, or raw `Color(0x...)` values.
- ❌ Do NOT alter existing `Responsive` wrapper logic without explicit instructions.
