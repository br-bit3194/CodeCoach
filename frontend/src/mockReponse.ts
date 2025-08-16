import { SearchResultResponse, UploadResultResponse } from './types/types';

export const mockUploadResponse: UploadResultResponse = {
   prdDoc: 'https://your-bucket-name.s3.amazonaws.com/fake-prd-doc.pdf',
};

export const getMockSearchResponse = (query: string): SearchResultResponse => ({
   answer:
      "Yes, there is a payment service used in the codebase. Here are the key points based on the retrieved context:\n\n1. **Dedicated Payment Service**: There is a `payment_service` microservice, as seen in the file paths (e.g., `payment_service/payments/management/commands/poll_sqs.py`).\n\n2. **Integration with Razorpay**: The code in `poll_sqs.py` mentions creating payment links using the Razorpay service. This is done by sending a POST request to the payment service's `/create_payment_link/` endpoint.\n\n3. **Order Service Communication**: The order service sends payment initiation messages to an AWS SQS queue, which the payment service polls. This is handled by the `send_payment_init_message` function in `order_service/orders/services/payment_sqs_service.py`.\n\n4. **Payment Callback Handling**: The payment service has a `payment_link_callback` view that processes callbacks from Razorpay, verifies signatures, updates payment status, and notifies the order service of payment results.\n\n5. **SQS-Based Messaging**: Both the order and payment services use AWS SQS queues to communicate payment initiation and status updates.\n\n**Relevant files and functions to explore:**\n- `payment_service/payments/management/commands/poll_sqs.py` (polls SQS for payment requests, interacts with Razorpay)\n- `order_service/orders/services/payment_sqs_service.py` (`send_payment_init_message` function)\n- `payment_service/payments/views.py` (`payment_link_callback` function)\n\nIf you want to extend, debug, or integrate with the payment service, these files are the best starting points.",
   related_files: [
      'ecommerce-microservices-dockerized_setup/payment_service/payments/management/commands/poll_sqs.py',
      'ecommerce-microservices-dockerized_setup/order_service/orders/services/payment_sqs_service.py',
      'ecommerce-microservices-dockerized_setup/payment_service/payments/views.py',
   ],
});
