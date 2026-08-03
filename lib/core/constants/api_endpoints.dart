class ApiEndpoints {
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
