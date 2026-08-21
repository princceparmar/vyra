# VYRA — Three-Tier Architecture Implementation

This folder contains the **Three-Tier Application** implementation of the VYRA Fashion E-Commerce Marketplace.

## Architecture Overview

The application is strictly separated into three distinct layers:

1. **Presentation Tier (`presentation-tier/frontend`)**:
   - Next.js / HTML5 + Tailwind CSS web interface running on `http://localhost:3000`.
   - Responsible strictly for rendering pages, handling user input, and communicating with the Application Tier via HTTP REST APIs.
   - **Enforced Rule**: Does NOT contain direct database queries or connection logic.

2. **Application Tier (`application-tier/backend`)**:
   - Python FastAPI service running on `http://localhost:8001`.
   - Implements authentication, product search/filtering algorithms, cart calculation engine, payment simulation, and order status handling.
   - Communicates with the Database Tier to query and persist state.

3. **Database Tier (`database-tier`)**:
   - SQLite database (`vyra.db`) holding relational tables (`users`, `products`, `wishlist`, `cart_items`, `orders`, `order_items`).

```
+----------------------------------------------------+
|               PRESENTATION TIER                    |
|           Next.js / React / HTML GUI               |
|             (http://localhost:3000)                |
+-------------------------+--------------------------+
                          |
                 REST HTTP API Requests
                          |
                          v
+----------------------------------------------------+
|               APPLICATION TIER                     |
|           Python FastAPI Business Logic            |
|             (http://localhost:8001)                |
+-------------------------+--------------------------+
                          |
                SQLite Database DAO
                          |
                          v
+----------------------------------------------------+
|                DATABASE TIER                       |
|           SQLite Database (vyra.db)                |
+----------------------------------------------------+
```

## Running Instructions

From this directory or root, run:
```bash
./start-threetier.sh
```

Access points:
- **Presentation Tier**: `http://localhost:3000`
- **Application Tier API Docs**: `http://localhost:8001/docs`

## Database Verification Support

The VYRA Three-Tier Architecture uses a physical SQLite database located precisely within its Database Tier. You can directly inspect the file to verify that all GUI actions persist correctly through the Application Tier.

- **Database Path**: `three-tier/database-tier/vyra.db`

### Tables and Triggers
- `users`: Updated upon user registration.
- `products`: Holds the entire product catalogue and inventory details.
- `cart_items`: Updated when adding/removing products to/from cart or changing quantities.
- `wishlist`: Updated when saving items to the wishlist.
- `orders` and `order_items`: Created successfully when placing a new order.
- `payments`: Created when executing a checkout with any of the 4 payment methods.

### How to Verify
1. Open the VYRA frontend at `http://localhost:3000`.
2. Complete a checkout process (e.g., using a Credit Card).
3. Open `three-tier/database-tier/vyra.db` using **DB Browser for SQLite** or run `sqlite3 vyra.db`.
4. Inspect the `payments` and `orders` tables—you will see your new transaction stored physically on disk.
