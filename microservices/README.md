# VYRA — Microservices Architecture Implementation

This folder contains the **Microservices Architecture** implementation of the VYRA Fashion E-Commerce Marketplace.

## Critical Assignment Compliance

> **COMPULSORY REQUIREMENT**: Every single microservice in this folder independently contains its own:
> 1. **GUI / User Interface** (Accessible standalone via browser)
> 2. **Business Logic** (Dedicated FastAPI service)
> 3. **Database** (Separate SQLite DB file per service)

## Service Directory

| Service | Port | Database | Standalone GUI URL | Business Function |
|---------|------|----------|-------------------|-------------------|
| **User Service** | `8011` | `users.db` | `http://localhost:8011/` | Auth, Register, Login, User Profile |
| **Product Service** | `8012` | `products.db` | `http://localhost:8012/` | Catalogue, Details, Search, Filter, Stock |
| **Cart & Wishlist Service** | `8013` | `cart.db` | `http://localhost:8013/` | Cart management, Wishlist, Discounts |
| **Order Service** | `8014` | `orders.db` | `http://localhost:8014/` | Order creation, History, Live Status Tracking |
| **Payment Service** | `8015` | `payments.db` | `http://localhost:8015/` | UPI/Card/COD payments, Failure simulation |
| **VYRA Gateway** | `8000` | N/A | `http://localhost:8000/` | Central Dashboard & End-to-End Orchestrator |

## Architecture Diagram

```
                              USER
                                │
                                v
                       VYRA GATEWAY (:8000)
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             v                  v                  v
        USER SERVICE      PRODUCT SERVICE      CART SERVICE
           (:8011)            (:8012)            (:8013)
           [ GUI ]            [ GUI ]            [ GUI ]
             │                  │                  │
             v                  v                  v
          users.db         products.db          cart.db

             ┌──────────────────┴──────────────────┐
             │                                     │
             v                                     v
       ORDER SERVICE                        PAYMENT SERVICE
          (:8014)                               (:8015)
          [ GUI ]                               [ GUI ]
             │                                     │
             v                                     v
         orders.db                            payments.db
```

## How to Run

Run the master start script:
```bash
./start-microservices.sh
```

Or run Docker Compose:
```bash
docker-compose up --build
```

## Database Verification Support

The VYRA Microservices Architecture implements strict Database per Service persistence. You can directly inspect the SQLite `.db` files to verify that all GUI actions persist correctly.

- **Payment Service**: `microservices/payment-service/database/payments.db`
- **Order Service**: `microservices/order-service/database/orders.db`
- **Cart Service**: `microservices/cart-service/database/cart.db`
- **Product Service**: `microservices/product-service/database/products.db`
- **User Service**: `microservices/user-service/database/users.db`

### How to Verify Payments
1. Open the VYRA Microservices Gateway at `http://localhost:8000`.
2. Add items to cart and complete a checkout process with any of the 4 payment methods.
3. Open `microservices/payment-service/database/payments.db` using **DB Browser for SQLite** or run `sqlite3 payments.db`.
4. Inspect the `payments` table—you will see your new transaction safely isolated in the Payment Service's dedicated database.
5. You can simultaneously check `microservices/order-service/database/orders.db` to verify the order was placed independently.
