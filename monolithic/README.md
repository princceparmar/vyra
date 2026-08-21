# VYRA — Monolithic Architecture Implementation

This folder contains the **Monolithic Application** implementation of the VYRA Fashion E-Commerce Marketplace.

## Architecture Overview

In this monolithic pattern:
- **Integrated Application**: GUI / Frontend, Business Logic, and Database Access logic are coupled within a single deployable FastAPI application.
- **Single Central Database**: A single SQLite database (`database/vyra.db`) holds all data tables (`users`, `products`, `wishlist`, `cart_items`, `orders`, `order_items`).
- **Unified Deployment**: The backend handles API routes and directly serves the responsive single-page fashion frontend interface.

```
USER ───► [ VYRA Monolithic App (FastAPI :8000) ] ───► Central Database (vyra.db)
             │
             ├── GUI / HTML5 Editorial Frontend
             ├── Auth Logic
             ├── Product Catalogue & Search Logic
             ├── Cart & Wishlist Logic
             └── Checkout & Payment Simulation Logic
```

## Setup & Running Instructions

### Prerequisites
- Python 3.10+
- `fastapi`, `uvicorn`, `pydantic` installed

### Quick Launch
From the project root or this folder, run:
```bash
./start-monolith.sh
```
Or manually:
```bash
cd backend
python3 seed.py
python3 -m uvicorn main:app --port 8000 --reload
```

Open your browser at:
`http://localhost:8000`

## Features Handled
1. **User Authentication**: Login/Register demo (`elena@vyra.fashion` / `vyra2026`).
2. **Product Catalogue**: 26 fashion products across 6 categories & 8 fictional brands.
3. **Filtering & Search**: Live keyword search, price range filter, size/color options, sorting by price/rating.
4. **Wishlist & Cart**: Persistent item state and instant subtotal/discount calculations.
5. **Simulated Payment & Orders**: UPI, Credit Card, Debit Card, Cash on Delivery.

## Database Verification Support

The VYRA Monolith uses a physical SQLite database. You can directly inspect the file to verify that all GUI actions persist correctly.

- **Database Path**: `monolithic/data/vyra.db`

### Tables and Triggers
- `users`: Updated upon user registration.
- `products`: Holds the entire product catalogue and inventory details.
- `cart_items`: Updated when adding/removing products to/from cart or changing quantities.
- `wishlist`: Updated when saving items to the wishlist.
- `orders` and `order_items`: Created successfully when placing a new order.
- `payments`: Created when executing a checkout with any of the 4 payment methods.

### How to Verify
1. Open the VYRA frontend.
2. Complete a checkout process (e.g., using a Credit Card).
3. Open `monolithic/data/vyra.db` using **DB Browser for SQLite** or run `sqlite3 vyra.db`.
4. Inspect the `payments` and `orders` tables—you will see your new transaction stored physically on disk.
