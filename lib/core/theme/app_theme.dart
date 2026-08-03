import 'package:flutter/material.dart';
import 'package:untitled2/core/constants/app_colors.dart';
import 'package:untitled2/core/constants/app_sizes.dart';

class AppTheme {
  AppTheme._(); // Private constructor to prevent instantiation

  // =========================================================
  // Light Theme
  // =========================================================
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,

      // Color Scheme
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: AppColors.surface,
        error: AppColors.error,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: AppColors.background,

      // App Bar Theme
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

      // Text Theme
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

      // Elevated Button Theme
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

      // Text Button Theme
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.primary,
          textStyle: const TextStyle(
            fontSize: AppSizes.fontMd,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),

      // Input Decoration Theme (TextFields)
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.surface,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSizes.md,
          vertical: AppSizes.md,
        ),
        hintStyle: const TextStyle(
          color: AppColors.textHint,
          fontSize: AppSizes.fontMd,
        ),
        labelStyle: const TextStyle(
          color: AppColors.textSecondary,
          fontSize: AppSizes.fontMd,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.primary, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.error),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.error, width: 2),
        ),
      ),

      // Card Theme
      cardTheme: CardThemeData(
        color: AppColors.surface,
        elevation: 0,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          side: const BorderSide(color: AppColors.border),
        ),
      ),

      // Floating Action Button Theme
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        elevation: 2,
      ),

      // Divider Theme
      dividerTheme: const DividerThemeData(
        color: AppColors.border,
        thickness: 1,
        space: 1,
      ),
    );
  }

  // =========================================================
  // Dark Theme
  // =========================================================
  static ThemeData get darkTheme {
    // Dark mode specific colors (adjust via AppColors if defined there)
    const darkBackground = Color(0xFF121212);
    const darkSurface = Color(0xFF1E1E1E);
    const darkBorder = Color(0xFF2C2C2C);
    const darkTextPrimary = Color(0xFFEEEEEE);
    const darkTextSecondary = Color(0xFFA0A0A0);
    const darkTextHint = Color(0xFF666666);

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,

      // Color Scheme
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: darkSurface,
        error: AppColors.error,
        brightness: Brightness.dark,
      ),
      scaffoldBackgroundColor: darkBackground,

      // App Bar Theme
      appBarTheme: const AppBarTheme(
        backgroundColor: darkSurface,
        foregroundColor: darkTextPrimary,
        elevation: 0,
        scrolledUnderElevation: 0.5,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: darkTextPrimary,
          fontSize: AppSizes.fontLg,
          fontWeight: FontWeight.w600,
        ),
      ),

      // Text Theme
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: AppSizes.fontDisplay,
          fontWeight: FontWeight.bold,
          color: darkTextPrimary,
        ),
        titleLarge: TextStyle(
          fontSize: AppSizes.fontXl,
          fontWeight: FontWeight.w600,
          color: darkTextPrimary,
        ),
        bodyLarge: TextStyle(
          fontSize: AppSizes.fontLg,
          color: darkTextPrimary,
        ),
        bodyMedium: TextStyle(
          fontSize: AppSizes.fontMd,
          color: darkTextPrimary,
        ),
        bodySmall: TextStyle(
          fontSize: AppSizes.fontSm,
          color: darkTextSecondary,
        ),
      ),

      // Elevated Button Theme
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

      // Text Button Theme
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.primaryLight,
          textStyle: const TextStyle(
            fontSize: AppSizes.fontMd,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),

      // Input Decoration Theme
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: darkSurface,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSizes.md,
          vertical: AppSizes.md,
        ),
        hintStyle: const TextStyle(
          color: darkTextHint,
          fontSize: AppSizes.fontMd,
        ),
        labelStyle: const TextStyle(
          color: darkTextSecondary,
          fontSize: AppSizes.fontMd,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: darkBorder),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: darkBorder),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.primary, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.error),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          borderSide: const BorderSide(color: AppColors.error, width: 2),
        ),
      ),

      // Card Theme
      cardTheme: CardThemeData(
        color: darkSurface,
        elevation: 0,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          side: const BorderSide(color: darkBorder),
        ),
      ),

      // Floating Action Button Theme
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        elevation: 2,
      ),

      // Divider Theme
      dividerTheme: const DividerThemeData(
        color: darkBorder,
        thickness: 1,
        space: 1,
      ),
    );
  }
}