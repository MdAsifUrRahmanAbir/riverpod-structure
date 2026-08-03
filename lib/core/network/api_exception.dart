import 'package:dio/dio.dart';

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
