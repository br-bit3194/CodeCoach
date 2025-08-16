---
# Product Requirements Document (PRD)
## Project: E-commerce Microservices (Dockerized Setup)

---

### 1. Product Overview

The E-commerce Microservices project is a modern, backend-focused e-commerce platform structured using a microservices architecture. Its primary goal is to demonstrate how a scalable, maintainable, and robust e-commerce backend can be accomplished by decomposing core business domains into independent but cooperating services. The system includes four principal microservices: User, Product, Order, and Payment, each developed as a standalone Django application, containerized, and orchestrated using Docker and Docker Compose.

Key objectives of this software are to:
- Provide an example architecture for modular e-commerce backend applications.
- Demonstrate best practices such as API-driven development, clear separation of business logic, asynchronous communication, and traceable distributed systems.
- Support local developer onboarding and experimentation via Docker-based setup and comprehensive documentation.

---

### 2. Core Features

**A. User Service**
- User registration and authentication (JWT/support planned).
- User profile management (CRUD).
- Role-based access control (planned).
- Secure password storage and password reset (planned).
- Administrative management via Django Admin.
- OpenAPI/Swagger documentation for all endpoints.

**B. Product Service**
- Product catalog management (CRUD for products).
- Category management (CRUD).
- Inventory/stock management including stock level checks.
- Product filtering and search endpoints.
- Administrative management via Django Admin.
- OpenAPI/Swagger documentation for all endpoints.

**C. Order Service**
- Order creation and management (creation, retrieval, and updates).
- Management of order items and status transitions (Pending, Completed, Failed).
- Stock verification via Product Service integration.
- Fetching user details (via User Service).
- Asynchronous payment initiation via AWS SQS.
- Receiving payment status updates (also via SQS).
- Administrative management via Django Admin.
- OpenAPI/Swagger documentation for all endpoints.

**D. Payment Service**
- Payment link creation and handling via Razorpay integration.
- Payment signature verification and security.
- Order and payment status tracking (PENDING, COMPLETED, FAILED, EXPIRED, etc.).
- Callback support for third-party payment providers.
- Asynchronous notification to the Order Service (via SQS) on payment status change.
- Administrative management via Django Admin.
- OpenAPI/Swagger documentation for all endpoints.

**E. Common/Cross-Cutting**
- Each service maintains its own database schema with migration support.
- Distributed tracing via CorrelationId propagation in HTTP headers and logs.
- Structured/centralized logging including correlation identifiers for debugging and monitoring.
- Automated environment configuration file encoding normalization.
- Docker and Docker Compose setup for local orchestration and isolation.

---

### 3. Architecture Summary

- **Modular Microservices:**  
  - **User, Product, Order, and Payment** each operate as distinct Django projects within their own directory with independent dependencies, configuration, and deployments.
- **Service Intercommunication:**  
  - Synchronous communication via HTTP REST APIs.
  - Asynchronous event-based communication via AWS Simple Queue Service (SQS)—emulated locally using LocalStack.
- **Business Logic Layer:**  
  - Core logic for domain operations is encapsulated in service/manager classes (e.g., OrderManager, ProductManager, RazorpayService).
- **API Layer:**  
  - Each service exposes its domain capabilities through RESTful APIs, documented interactively with Swagger (drf-yasg).
- **Cross-Service Observability:**  
  - Correlation IDs are handled via custom middleware and logger utilities to enable distributed tracing and root-cause analysis.
- **Administrative Management:**  
  - Django Admin sites for each service provide backend data management.
- **Testing & Maintainability:**  
  - Standardized directory and project structure.
  - Foundation for automated testing (placeholders/templates present).

---

### 4. Technology Stack

- **Application Framework:**  
  - Python 3.x  
  - Django  
  - Django REST Framework (DRF)
- **API Documentation:**  
  - drf-yasg (Swagger & Redoc auto-documentation)
- **Containerization/DevOps:**  
  - Docker  
  - Docker Compose  
  - LocalStack (AWS service emulator)
- **Inter-Service Messaging:**  
  - AWS SQS (with LocalStack for local development)
- **Database:**  
  - SQLite (for development; can be replaced with RDBMS in production)
- **3rd Party Integrations:**  
  - Razorpay (for payments)
- **Other Packages:**  
  - python-dotenv (environment variable management)
  - Custom logging, middleware, and utility libraries within each service

---

### 5. API or User Interface

**A. RESTful APIs:**  
Each microservice exposes RESTful endpoints, grouped as follows:
- **User Service:** `/user/` for registration and user management.
- **Product Service:** `/products/` for product and category operations, `/products/health/` for service monitoring.
- **Order Service:** `/orders/` for order operations.
- **Payment Service:** `/payments/` for payment link generation, `/payments/payment_link_callback/` for payment result handling.

**B. Documentation/UIs:**
- **Swagger & Redoc (API Docs):**  
  Accessible at `/swagger/`, `/redoc/`, `/swagger.json`, and `/swagger.yaml` per Django service.
- **Django Admin:**  
  Accessible via `/admin/` for backend management on each microservice.
- **Service Health/Debug Endpoints:**  
  Health endpoints (e.g., in Product Service) and correlation ID-enabled logging for operational insight.

**C. Integration Patterns:**
- HTTP-based synchronous APIs (external integrations with product, user, payment, order).
- Asynchronous commands/events via SQS between Order ↔ Payment services.

---

### 6. Known Limitations / TODOs

- **Automated Testing:**  
  Test files are scaffolded but currently lack implementation across all microservices.
- **Authentication:**  
  JWT-based authentication and full session support are planned but not fully implemented.
- **Frontend/Customer-Facing UI:**  
  No frontend user interface is included; this is a backend-only project.
- **Production Database:**  
  SQLite is used for local development; configuration and migration for production RDBMS are required for deployment.
- **Cloud Infrastructure:**  
  SQS is emulated using LocalStack for local development, but production deployment must handle IAM, scaling, monitoring, and other AWS/cloud concerns.
- **Feature Incompleteness:**  
  Role-based access and advanced user profile management are planned extensions.
  - Payment admin console lacks model registration.
- **Monitoring/Tracing Enhancements:**  
  Distributed tracing is limited to correlation IDs in logs; integration with full observability stacks (e.g., AWS X-Ray, CloudWatch) is noted for future.
- **Security:**  
  Further configuration is required for HTTPS, data encryption at rest, and secure secret management in production deployments.
- **API Rate Limiting/Throttling:**  
  Not present; essential for public deployments to protect against abuse.

---

### 7. Conclusion & Next Steps

This project serves as a highly instructive, extensible, and robust architecture for backend e-commerce platforms, demonstrating best practices in microservices, API-first development, and operational traceability. To reach production-grade quality, work remains in automated testing, security hardening, advanced authentication/authorization, and cloud deployment at scale. The modular structure, clear documentation, and focus on clean interfaces make it suitable for onboarding new team members, rapid prototyping, or as the foundation of a new e-commerce business.

---

**For stakeholders:**  
- Review service boundaries to ensure business needs are fully addressed.
- Prioritize implementation of automated testing, production-ready authentication, and API rate-limiting/security enhancements.
- Plan cloud deployment, monitoring, and CI/CD integration for reliable and scalable rollout.

**For engineers:**  
- Follow service-specific README instructions for local development.
- Adhere to service abstraction layers (manager/services) for business logic and API endpoint separation.
- Extend test suites and API docs as new features are added.

---markdown
Copy
Edit
## Database Schema

### Table: Users
- `id`: BigAutoField, Primary Key, auto_created
- `created_at`: DateTimeField, auto_now_add=True, Not Null
- `updated_at`: DateTimeField, auto_now=True, Not Null
- `name`: CharField(max_length=100), Not Null
- `email`: EmailField(max_length=254), Unique, Not Null

---

### Table: Category
- `id`: BigAutoField, Primary Key, auto_created
- `created_at`: DateTimeField, auto_now_add=True, Not Null
- `updated_at`: DateTimeField, auto_now=True, Not Null
- `name`: CharField(max_length=100), Unique, Not Null
- `description`: TextField, blank=True, Nullable

---

### Table: Products
- `id`: BigAutoField, Primary Key, auto_created
- `created_at`: DateTimeField, auto_now_add=True, Not Null
- `updated_at`: DateTimeField, auto_now=True, Not Null
- `name`: CharField(max_length=100), Not Null
- `description`: TextField, blank=True, Nullable
- `price`: DecimalField(max_digits=10, decimal_places=2), Not Null
- `stock_quantity`: PositiveIntegerField, Not Null
- `category_id`: ForeignKey to `Category(id)`, Nullable, on_delete=SET_NULL, related_name='products'

---

### Table: AuditLog
- `id`: BigAutoField, Primary Key, auto_created
- `created_at`: DateTimeField, auto_now_add=True, Not Null
- `updated_at`: DateTimeField, auto_now=True, Not Null

---

### Table: Payment
- `auditlog_ptr_id`: OneToOneField (to AuditLog, parent_link=True), Primary Key
- `order_id`: CharField(max_length=255), Not Null
- `razorpay_order_id`: CharField(max_length=255), Unique, Nullable
- `razorpay_payment_id`: CharField(max_length=255), Unique, Nullable
- `razorpay_payment_link_id`: CharField(max_length=255), Unique, Nullable
- `razorpay_short_url`: CharField(max_length=255), Unique, Nullable
- `amount`: DecimalField(max_digits=10, decimal_places=2), Not Null
- `currency`: CharField(max_length=3), Default='INR', Not Null
- `status`: CharField(max_length=50), Not Null
- `receipt`: CharField(max_length=255), Unique, Not Null
- `reason`: CharField(max_length=255), Nullable, blank=True

---

### Table: Order
- `id`: BigAutoField, Primary Key, auto_created
- `created_at`: DateTimeField, auto_now_add=True, Not Null
- `updated_at`: DateTimeField, auto_now=True, Not Null
- `user_id`: IntegerField, Not Null           <!-- references Users.id logically, but no ForeignKey constraint in schema -->
- `total_price`: DecimalField(max_digits=15, decimal_places=2), Not Null
- `status`: CharField(max_length=20), Choices (pending/success/failed), Default='pending', Not Null

---

### Table: OrderItems
- `id`: BigAutoField, Primary Key, auto_created
- `created_at`: DateTimeField, auto_now_add=True, Not Null
- `updated_at`: DateTimeField, auto_now=True, Not Null
- `order_id`: ForeignKey to `Order(id)`, on_delete=CASCADE, related_name='order_items', Not Null
- `product_id`: IntegerField, Not Null        <!-- references Products.id logically, but not as a ForeignKey in schema -->
- `quantity`: PositiveIntegerField, Not Null
- `price`: DecimalField(max_digits=10, decimal_places=2), Not Null

---

## Entity Relationships

- **Category** 1 --- * Products: Each `Products` row may reference one `Category` via `category_id` (nullable, via foreign key).
- **Order** 1 --- * OrderItems: Each `OrderItems` row references one `Order` via `order_id` (foreign key, required).
- **AuditLog** 1 --- 1 Payment: Inheritance via OneToOneField on `auditlog_ptr_id`.
- **Users**: No explicit foreign keys to Users, but `Order.user_id` indicates intended relation (should ideally be ForeignKey to Users).

- **Products** and **OrderItems**: There is an implicit (non-FK) relationship from `OrderItems.product_id` to `Products.id`.
- **Order** and **Users**: There is an implicit (non-FK) relationship from `Order.user_id` to `Users.id`.

## Database Usage Summary

- **ORM**: Django ORM is employed throughout (models use Django's `models.Model`, and migrations are generated for every model/table evolution).
- **Migrations**: Automatic Django migrations are present for all model/table changes (field alters, renames, etc.).
- **No raw SQL**: There is no use of `cursor.execute(...)` or raw SQL in the provided code; all DB operations use Django's ORM.
- **Indexing**: Uniqueness constraints on fields (`email` in Users, `receipt`, and Razorpay fields in Payment) imply auto-index creation.
- **Model Inheritance**: Abstract base classes (`AuditModel`, `AuditLog`) are used for audit fields; Payment uses multi-table inheritance via OneToOneField.
- **Relations**: Foreign keys and one-to-one relationships are managed by Django; some relationships (Orders-Users, OrderItems-Products) use plain IntegerFields without explicit FK constraints.
- **Usage Patterns**: All database access is via standard Django ORM model managers (`objects.all()`, `objects.filter()`), with serialization for API or internal use. Exception handling for integrity and validation errors is present.
- **Joins**: Implicit joins via ForeignKeys in ORM, but no explicit SQL joins.

## Mermaid ER Diagram

```mermaid
erDiagram
  Users {
    BIGINT id PK
    DATETIME created_at
    DATETIME updated_at
    STRING name
    STRING email UNIQUE
  }
  Category {
    BIGINT id PK
    DATETIME created_at
    DATETIME updated_at
    STRING name UNIQUE
    TEXT description
  }
  Products {
    BIGINT id PK
    DATETIME created_at
    DATETIME updated_at
    STRING name
    TEXT description
    DECIMAL price
    INTEGER stock_quantity
    BIGINT category_id FK
  }
  AuditLog {
    BIGINT id PK
    DATETIME created_at
    DATETIME updated_at
  }
  Payment {
    BIGINT auditlog_ptr_id PK, FK
    STRING order_id
    STRING razorpay_order_id UNIQUE
    STRING razorpay_payment_id UNIQUE
    STRING razorpay_payment_link_id UNIQUE
    STRING razorpay_short_url UNIQUE
    DECIMAL amount
    STRING currency
    STRING status
    STRING receipt UNIQUE
    STRING reason
  }
  Order {
    BIGINT id PK
    DATETIME created_at
    DATETIME updated_at
    INTEGER user_id
    DECIMAL total_price
    STRING status
  }
  OrderItems {
    BIGINT id PK
    DATETIME created_at
    DATETIME updated_at
    BIGINT order_id FK
    INTEGER product_id
    INTEGER quantity
    DECIMAL price
  }

  Category ||--o{ Products : has
  Order ||--o{ OrderItems : contains
  AuditLog ||--|| Payment : inherits
  %% Logical/implicit relationships (not DB-enforced)
  Users ||--o{ Order : places
  Products ||--o{ OrderItems : in
```

---

**Note:**  
- Relationships between `Users`-`Order` and `Products`-`OrderItems` are logical, and not enforced as ForeignKey constraints in the schema.
- `Payment` is a one-to-one (“inherits from”) with `AuditLog`.
- All audit fields are included via base/abstract models.