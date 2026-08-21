# VYRA — Wear Your Story.

**VYRA** is an original fashion e-commerce marketplace built as an academic software engineering project to demonstrate and compare three core software architectures: **Monolithic**, **Three-Tier**, and **Microservices**.

---

## 🌟 Visual Branding & Aesthetic
- **Brand Identity**: VYRA ("Wear Your Story.")
- **Visual Aesthetic**: High-fashion editorial aesthetic featuring stylized V logo branding, neutral off-white (`#FAF9F6`) and deep charcoal base with champagne gold and electric violet accents, fluid card micro-animations, and live order tracking.
- **Product Catalogue**: 26 fashion products across 6 categories (Women, Men, Footwear, Accessories, New Arrivals, Seasonal Collection) and 8 fictional fashion brands (*Aurelia Studio*, *NorthThread*, *Viora*, *Ember and Loom*, *Solace Street*, *Urban Halo*, *ThreadTheory*, *Luna Wardrobe*).

---

## 🏛️ Architectures Implemented

### 1. Monolithic Architecture (`/monolithic`)
- **Structure**: Single integrated application process containing GUI / Frontend, Business Logic, and Database Access.
- **Database**: Single central SQLite database (`data/vyra.db`).
- **Launch**: `./monolithic/start-monolith.sh` ➔ `http://localhost:8000`

### 2. Three-Tier Architecture (`/three-tier`)
- **Presentation Tier (Tier 1)**: Next.js / HTML5 GUI running on `http://localhost:3000`. Strictly communicates via REST APIs with Tier 2; zero direct database code.
- **Application Tier (Tier 2)**: FastAPI backend on `http://localhost:8001` handling auth logic, product business rules, discount calculations, and payment simulation.
- **Database Tier (Tier 3)**: Relational SQLite database (`vyra.db`).
- **Launch**: `./three-tier/start-threetier.sh` ➔ `http://localhost:3000`

### 3. Microservices Architecture (`/microservices`)
- **Compulsory Requirement Compliance**: Every microservice independently contains its own **GUI + Business Logic + Isolated Database**:
  - `user-service`: Port `8011` API & Standalone GUI | DB: `users.db`
  - `product-service`: Port `8012` API & Standalone GUI | DB: `products.db`
  - `cart-service`: Port `8013` API & Standalone GUI | DB: `cart.db`
  - `order-service`: Port `8014` API & Standalone GUI | DB: `orders.db`
  - `payment-service`: Port `8015` API & Standalone GUI | DB: `payments.db`
- **Gateway & Dashboard**: Port `8000` (Unified Shopping Journey & Service Inspector)
- **Launch**: `./microservices/start-microservices.sh` or `docker-compose up`

---

## 📁 Repository Directory Structure

```
VYRA/
├── README.md                        # Master documentation
├── start-all.sh                     # Interactive launcher script
│
├── monolithic/                      # Monolithic Implementation
│   ├── backend/                     # FastAPI backend & database layer
│   ├── frontend/                    # Single-page HTML5/JS GUI
│   ├── database/                    # vyra.db central SQLite database
│   ├── start-monolith.sh            # 1-click launch script
│   └── README.md
│
├── three-tier/                      # Three-Tier Implementation
│   ├── presentation-tier/           # Next.js/HTML GUI (Port 3000)
│   ├── application-tier/            # FastAPI Business Logic (Port 8001)
│   ├── database-tier/               # vyra.db database tier
│   ├── start-threetier.sh           # 1-click launch script
│   └── README.md
│
├── microservices/                   # Microservices Implementation
│   ├── user-service/                # Auth & User Profile (Port 8011 & GUI 8011, users.db)
│   ├── product-service/             # Catalogue & Inventory (Port 8012 & GUI 8012, products.db)
│   ├── cart-service/                # Cart & Wishlist (Port 8013 & GUI 8013, cart.db)
│   ├── order-service/               # Orders & Tracking (Port 8014 & GUI 8014, orders.db)
│   ├── payment-service/             # Payment Simulation (Port 8015 & GUI 8015, payments.db)
│   ├── gateway/                     # Central Gateway & Hub (Port 8000)
│   ├── docker-compose.yml           # Docker orchestration
│   ├── start-microservices.sh       # 1-click launch script for all 5 services
│   └── README.md
│
├── architecture-diagrams/           # High-resolution architectural specifications
│   ├── monolithic.md
│   ├── three-tier.md
│   └── microservices.md
│
└── demo-guide/                      # Group Screencast & Evaluation Deliverables
    ├── group-demo-flow.md           # 10-minute 5-student presentation script
    └── architecture-comparison.md   # Architectural evaluation matrix
```

---

## ⚡ Quickstart Commands

Launch interactively:
```bash
./start-all.sh
```

Or run any architecture directly:
```bash
# Launch Monolithic Application
./monolithic/start-monolith.sh

# Launch Three-Tier Application
./three-tier/start-threetier.sh

# Launch Microservices Architecture
./microservices/start-microservices.sh
```

---

## 🎥 10-Minute Screencast Presentation Guide
Refer to [demo-guide/group-demo-flow.md](demo-guide/group-demo-flow.md) for the exact 5-student breakdown (2 minutes per student) with dialogues, screen actions, and code locations.
