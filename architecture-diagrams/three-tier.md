# Three-Tier Architecture Specification — VYRA

## Architectural Model
The Three-Tier Architecture physically and logically decouples the VYRA Fashion E-Commerce application into three independent tiers: **Presentation Tier (Tier 1)**, **Application Tier (Tier 2)**, and **Database Tier (Tier 3)**.

```mermaid
graph TD
    subgraph Tier 1: Presentation Tier
        GUI[Next.js / HTML5 Web Interface :3000]
    end
    
    subgraph Tier 2: Application Tier
        API[FastAPI Business Logic Server :8001]
        AuthLogic[Auth & Session Business Rules]
        DiscountCalc[Discount & Total Calculation Engine]
        OrderEngine[Order Processing & Status Engine]
        PaySim[Payment Simulation Engine]
        
        API --> AuthLogic
        API --> DiscountCalc
        API --> OrderEngine
        API --> PaySim
    end
    
    subgraph Tier 3: Database Tier
        DB[(Relational SQLite Database: vyra.db)]
    end
    
    GUI -- HTTP REST APIs --> API
    API -- SQLite Connection Layer --> DB
```

## Strict Boundary Rules
- **Presentation Tier Rules**: Must only execute UI rendering and user interactions. Zero direct file access to `vyra.db` or database queries. All data access must pass through REST API endpoints on Port 8001.
- **Application Tier Rules**: Executes business rules, discount calculations, validation, and database operations.
- **Database Tier Rules**: Manages table persistence, schema constraints, and transaction integrity.
