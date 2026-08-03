import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:untitled2/features/checkout/data/models/invoice_model.dart';

class CheckoutController extends Notifier<AsyncValue<InvoiceModel?>> {
  @override
  AsyncValue<InvoiceModel?> build() => const AsyncValue.data(null);
}

final checkoutControllerProvider = NotifierProvider<CheckoutController, AsyncValue<InvoiceModel?>>(CheckoutController.new);
