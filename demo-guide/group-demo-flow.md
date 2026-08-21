# VYRA — 10-Minute Group Screencast Script (5 Students)

**Total Duration**: 10 Minutes  
**Students**: 5  
**Time Per Student**: ~2 Minutes  
**Target Audience**: Academic Software Engineering Evaluators  

---

## 🎬 Student 1 (0:00 – 2:00): Introduction & Monolithic Architecture

### 🎙️ Dialogue Script:
> *"Hello everyone! Welcome to our group presentation of **VYRA — Wear Your Story**, an original modern fashion e-commerce marketplace built for our Software Engineering assignment.*  
> *Today, our group of 5 students will demonstrate the exact same VYRA business application across three fundamentally different software engineering architectures: Monolithic, Three-Tier, and Microservices.*  
> *I am Student 1, and I will be presenting the **Monolithic Architecture**.*  
> *Let's launch the Monolithic app using `./start-monolith.sh` and open `http://localhost:8000`.*  
> *As you can see, VYRA features a high-end editorial fashion catalogue with 26 products across 8 fictional brands like Aurelia Studio and Viora.*  
> *Under the hood, this entire application—the HTML5 GUI, business logic, discount calculations, and database operations—exists within a single integrated FastAPI process connecting to one central SQLite database file, `vyra.db`.*  
> *Let me demonstrate adding a item to the cart and browsing. In a monolith, this happens in-process with zero network overhead between modules."*

### 💻 Screen Actions:
1. Terminal: Execute `./start-monolith.sh`.
2. Browser: Navigate to `http://localhost:8000`.
3. Highlight branding: Logo, "Wear Your Story.", category pills, product grid.
4. Open Architecture Info modal showing `vyra.db` single database model.
5. Click "Add to Bag" on a product to show cart update.

---

## 🎬 Student 2 (2:00 – 4:00): Three-Tier Architecture — Presentation Tier

### 🎙️ Dialogue Script:
> *"Thank you, Student 1! I am Student 2, and I will introduce our **Three-Tier Architecture** implementation and walk you through **Tier 1: The Presentation Tier**.*  
> *In Three-Tier architecture, we strictly decouple the User Interface from the backend and database. Let's run `./start-threetier.sh` and open the Presentation Tier at `http://localhost:3000`.*  
> *Notice the crucial architectural constraint enforced here: The Presentation Tier contains **zero database access logic** and **zero direct SQL queries**. It is a pure Next.js/HTML GUI.*  
> *When I filter products by category or brand, or when I search for 'silk coat', the Presentation Tier constructs asynchronous HTTP REST requests to the Application Tier running on port 8001.*  
> *Let's open the browser developer network tools: every action translates into a REST call to `http://localhost:8001/api/products`."*

### 💻 Screen Actions:
1. Terminal: Execute `./start-threetier.sh`.
2. Browser: Open `http://localhost:3000`.
3. Open Browser Developer Tools ➔ Network tab.
4. Interact with brand dropdown and category pills; point to live fetch calls targeting `http://localhost:8001/api/...`.
5. Point out the top announcement banner confirming "TIER 1: PRESENTATION TIER (Port 3000)".

---

## 🎬 Student 3 (4:00 – 6:00): Three-Tier Architecture — Application & Database Tiers

### 🎙️ Dialogue Script:
> *"Thanks Student 2! I am Student 3, and I will demonstrate **Tier 2: The Application Tier** and **Tier 3: The Database Tier**.*  
> *Here on screen is our FastAPI Application Tier running on port `8001` (`three-tier/application-tier/main.py`).*  
> *This layer holds all the business rules: pricing discount algorithms, stock inventory validations, cart total calculations, and payment simulation.*  
> *When a checkout request arrives at `/api/checkout`, the Application Tier verifies cart contents, calculates delivery fees, executes the simulated payment logic, and then issues SQL transactions to Tier 3.*  
> *Tier 3 is located in `three-tier/database-tier/vyra.db`. Let's inspect the database file and query the `orders` and `order_items` tables using SQLite browser to confirm persistent storage."*

### 💻 Screen Actions:
1. Open code editor to `three-tier/application-tier/main.py` line-by-line showing `/api/checkout` and discount calculation logic.
2. Open `http://localhost:8001/docs` (Swagger UI) to show FastAPI OpenAPI documentation.
3. Show database schema file `three-tier/database-tier/db.py`.
4. Perform a successful checkout on the frontend (`:3000`) and show the database row created in `vyra.db`.

---

## 🎬 Student 4 (6:00 – 8:00): Microservices Architecture & Database Isolation

### 🎙️ Dialogue Script:
> *"Thank you! I am Student 4, and I will introduce the **Microservices Architecture**.*  
> *Our project strictly satisfies the compulsory assignment requirement: **Every microservice independently contains its own GUI, Business Logic, and Database**.*  
> *Let's execute `./start-microservices.sh`. This launches 5 autonomous microservices plus our central Gateway.*  
> *Let's inspect service 1: **User Service** on port `8011` with its own `users.db` and standalone GUI.*  
> *Let's inspect service 2: **Product Service** on port `8012` with its own `products.db` and standalone GUI.*  
> *Unlike fake microservices that share one single database, every service here is completely isolated. If the Product Service database goes down, the User Service remains 100% operational!"*

### 💻 Screen Actions:
1. Terminal: Run `./start-microservices.sh`.
2. Open `http://localhost:8011/` in browser to show standalone User Service GUI & `users.db` badge.
3. Open `http://localhost:8012/` in browser to show standalone Product Service GUI & `products.db` badge.
4. Show directory tree `microservices/` emphasizing `user-service/database/users.db`, `product-service/database/products.db`, etc.

---

## 🎬 Student 5 (8:00 – 10:00): Microservices Integration & Final Architectural Trade-Offs

### 🎙️ Dialogue Script:
> *"Thank you Student 4! I am Student 5, and I will demonstrate the end-to-end Microservices purchase flow and conclude our architectural evaluation.*  
> *Let's open the **VYRA Central Gateway** at `http://localhost:8000`.*  
> *When a user completes a purchase here, the Gateway orchestrates a distributed multi-service flow:*  
> 1. *It fetches active items from **Cart Service** (`cart.db` at `:8013`).*  
> 2. *It calls **Payment Service** (`payments.db` at `:8015`) to process simulated UPI/Card payments.*  
> 3. *Upon success, it calls **Order Service** (`orders.db` at `:8014`) to generate the order and tracking timeline.*  
> 4. *Finally, it clears the cart in Cart Service.*  
> *Let's view the **Architecture Comparison Dashboard**: Monoliths provide simplicity and low latency; Three-Tier provides layer decoupling; Microservices provide independent scaling, fault isolation, and autonomous deployments at the cost of higher operational complexity.*  
> *That concludes our 10-minute demonstration of VYRA. Thank you!"*

### 💻 Screen Actions:
1. Open Gateway at `http://localhost:8000`.
2. Add product to bag, open checkout modal, choose UPI payment method, and complete order.
3. Show popup alert confirming multi-service execution across `cart.db`, `payments.db`, and `orders.db`.
4. Open Service Inspector / Architecture Inspector modal to highlight health status of all 5 services.
5. Conclude video presentation.
