# Microservices Architecture Specification — VYRA

## Architectural Model
The Microservices Architecture decomposes VYRA into 5 completely autonomous, domain-driven services, plus a Central Gateway. Every microservice adheres strictly to the compulsory academic rule: **GUI + Business Logic + Isolated Database**.

```mermaid
graph TD
    User[User Client] --> Gateway[VYRA Gateway & Dashboard :8000]
    
    subgraph Microservice 1: User Service
        UGUI[User GUI :8011] --> UAPI[User API Logic]
        UAPI --> UDB[(users.db)]
    end

    subgraph Microservice 2: Product Service
        PGUI[Product GUI :8012] --> PAPI[Product API Logic]
        PAPI --> PDB[(products.db)]
    end

    subgraph Microservice 3: Cart Service
        CGUI[Cart GUI :8013] --> CAPI[Cart API Logic]
        CAPI --> CDB[(cart.db)]
    end

    subgraph Microservice 4: Order Service
        OGUI[Order GUI :8014] --> OAPI[Order API Logic]
        OAPI --> ODB[(orders.db)]
    end

    subgraph Microservice 5: Payment Service
        PAYGUI[Payment GUI :8015] --> PAYAPI[Payment API Logic]
        PAYAPI --> PAYDB[(payments.db)]
    end

    Gateway -- Orchestration REST Calls --> UAPI
    Gateway -- Orchestration REST Calls --> PAPI
    Gateway -- Orchestration REST Calls --> CAPI
    Gateway -- Orchestration REST Calls --> OAPI
    Gateway -- Orchestration REST Calls --> PAYAPI
```

## Database & GUI Isolation Table
| Service Name | Port | Isolated GUI Path | Isolated Database File | Managed Domain Entities |
|--------------|------|------------------|------------------------|-------------------------|
| `user-service` | 8011 | `http://localhost:8011/` | `users.db` | Users, Registration, Auth Credentials |
| `product-service` | 8012 | `http://localhost:8012/` | `products.db` | Catalogue, Categories, Inventory Stock |
| `cart-service` | 8013 | `http://localhost:8013/` | `cart.db` | Cart Items, Wishlist Items, Discounts |
| `order-service` | 8014 | `http://localhost:8014/` | `orders.db` | Orders, Order Items, Status Timeline |
| `payment-service` | 8015 | `http://localhost:8015/` | `payments.db` | Payments, Transactions, Audit Log |
