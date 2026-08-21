# Architectural Evaluation & Comparison Report — VYRA

## Executive Summary
This document presents an academic comparative analysis of the three software engineering architectures implemented for the **VYRA Fashion Marketplace**:
1. **Monolithic Architecture**
2. **Three-Tier Architecture**
3. **Microservices Architecture**

---

## Architecture Comparison Matrix

| Evaluation Criteria | Monolithic Architecture | Three-Tier Architecture | Microservices Architecture |
|---------------------|------------------------|-------------------------|---------------------------|
| **System Structure** | Single integrated application process | 3 physically/logically separated layers | 5 independent microservices + 1 gateway |
| **GUI Location** | Embedded within monolithic server (`:8000`) | Standalone Presentation Tier (`:3000`) | Standalone GUI per service (`:8011` to `:8015`) + Gateway Hub (`:8000`) |
| **Database Isolation** | Single central database (`vyra.db`) | Single central database tier (`vyra.db`) | Separate isolated database per service (`users.db`, `products.db`, `cart.db`, `orders.db`, `payments.db`) |
| **Deployment Complexity** | Low (Single process startup) | Moderate (2 server processes + 1 DB) | High (6 server processes / Docker Compose) |
| **Network Overhead** | Zero (In-memory function calls) | Low (Client ➔ App Tier REST calls) | Moderate (Gateway ➔ Inter-service REST calls) |
| **Fault Isolation** | Poor (Failure in cart crashes entire app) | Moderate (UI decoupled from backend) | Excellent (Product service crash does not affect User service) |
| **Scalability** | Scale whole monolith instance | Scale individual tiers independently | Scale individual microservices independently based on load |

---

## Architectural Deep Dive

### 1. Monolithic Architecture (`/monolithic`)
- **Pros**: Easy local setup, zero inter-service network latency, simple transactional integrity with single database transactions.
- **Cons**: Tight coupling between domains; scaling requires duplicating the entire application stack.

### 2. Three-Tier Architecture (`/three-tier`)
- **Pros**: Strict separation of concerns (Presentation vs Business Logic vs Data Access); frontend can be refactored or replaced without modifying database tier.
- **Cons**: Central database tier remains a single point of failure and scaling bottleneck.

### 3. Microservices Architecture (`/microservices`)
- **Pros**: True domain autonomy, data isolation per service, independent deployment pipelines, high resilience. Satisfies compulsory requirement where every service has its own GUI, Logic, and Database.
- **Cons**: Increased operational complexity, distributed data consistency considerations (eventual consistency).
