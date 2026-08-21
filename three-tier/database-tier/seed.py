import sqlite3
import hashlib
import sys
from pathlib import Path

# Add database-tier to sys.path
sys.path.append(str(Path(__file__).parent))
from db import get_db_connection, init_db_tier

PRODUCTS = [
    {
        "name": "Minimalist Silk Trench Coat",
        "brand": "Aurelia Studio",
        "description": "Crafted from fluid mulberry silk-blend fabric, this double-breasted trench coat offers an airy editorial silhouette with storm flaps and a waist tie belt.",
        "category": "Women",
        "price": 189.00,
        "discount": 15,
        "sizes": "XS,S,M,L",
        "colors": "Beige,Charcoal,Sage",
        "images": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "stock": 35,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Oversized Cashmere Knit Sweater",
        "brand": "Luna Wardrobe",
        "description": "Ultra-soft grade-A cashmere knit with dropped shoulders and ribbed cuffs. Designed for cozy warmth and effortlessness.",
        "category": "Women",
        "price": 129.00,
        "discount": 10,
        "sizes": "S,M,L,XL",
        "colors": "Cream,Oatmeal,Dusty Rose",
        "images": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "stock": 42,
        "is_new": 0,
        "is_seasonal": 1
    },
    {
        "name": "Sculpted Tailored Blazer",
        "brand": "Viora",
        "description": "Precision-tailored single-breasted blazer featuring padded shoulders, welt pockets, and a cinch waist silhouette.",
        "category": "Women",
        "price": 159.00,
        "discount": 20,
        "sizes": "XS,S,M,L",
        "colors": "Midnight Black,Ivory,Olive",
        "images": "https://images.unsplash.com/photo-1584273143981-41c073dfe8f8?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "stock": 28,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Fluid Wide-Leg Linen Trousers",
        "brand": "Ember and Loom",
        "description": "High-waisted wide leg pants tailored in breathable European linen. Elastic back waistband for peak comfort.",
        "category": "Women",
        "price": 95.00,
        "discount": 0,
        "sizes": "XS,S,M,L,XL",
        "colors": "Sand,White,Terracotta",
        "images": "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1551803091-e20673f15770?auto=format&fit=crop&w=800&q=80",
        "rating": 4.6,
        "stock": 50,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Asymmetric Pleated Midi Dress",
        "brand": "Solace Street",
        "description": "Architectural pleated silhouette with asymmetrical neckline and fluid movement for modern evening occasions.",
        "category": "Women",
        "price": 145.00,
        "discount": 12,
        "sizes": "S,M,L",
        "colors": "Emerald,Champagne,Black",
        "images": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "stock": 20,
        "is_new": 0,
        "is_seasonal": 1
    },
    {
        "name": "Structured Wool Double-Breasted Coat",
        "brand": "NorthThread",
        "description": "Heavyweight Italian wool coat featuring sharp lapels, deep side pockets, and satin lining. Built for cold winters.",
        "category": "Men",
        "price": 210.00,
        "discount": 25,
        "sizes": "S,M,L,XL",
        "colors": "Camel,Navy,Charcoal",
        "images": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "stock": 25,
        "is_new": 0,
        "is_seasonal": 1
    },
    {
        "name": "Japanese Selvage Denim Jacket",
        "brand": "Urban Halo",
        "description": "14oz raw selvage denim crafted in Okayama. Features custom brass hardware, dual chest pockets, and contrast stitching.",
        "category": "Men",
        "price": 135.00,
        "discount": 10,
        "sizes": "S,M,L,XL",
        "colors": "Indigo Wash,Washed Black",
        "images": "https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "stock": 38,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Relaxed Merino Wool Hoodie",
        "brand": "ThreadTheory",
        "description": "Elevated loungewear spun from extrafine Australian merino wool. Double-layer hood and clean seamless finish.",
        "category": "Men",
        "price": 110.00,
        "discount": 5,
        "sizes": "S,M,L,XL",
        "colors": "Heather Grey,Dark Moss,Black",
        "images": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1509967419530-da38b4704bc6?auto=format&fit=crop&w=800&q=80",
        "rating": 4.5,
        "stock": 45,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Slim Fit Cotton Oxford Shirt",
        "brand": "NorthThread",
        "description": "Classic button-down shirt woven from 100% organic Supima cotton. Garment washed for subtle softness.",
        "category": "Men",
        "price": 79.00,
        "discount": 0,
        "sizes": "S,M,L,XL",
        "colors": "Sky Blue,Classic White,Pink Stripe",
        "images": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=800&q=80",
        "rating": 4.6,
        "stock": 60,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Pleated Tapered Chino Pants",
        "brand": "Solace Street",
        "description": "Contemporary pleated chinos with a gentle taper, horn button closure, and stretch cotton twill weave.",
        "category": "Men",
        "price": 88.00,
        "discount": 15,
        "sizes": "30,32,34,36",
        "colors": "Khaki,Olive,Navy",
        "images": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80",
        "rating": 4.4,
        "stock": 40,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Handcrafted Italian Leather Chelsea Boots",
        "brand": "Aurelia Studio",
        "description": "Full-grain Tuscan calf leather upper, Goodyear welted rubber soles, and elastic side gussets for effortless slip-on style.",
        "category": "Footwear",
        "price": 220.00,
        "discount": 18,
        "sizes": "39,40,41,42,43,44",
        "colors": "Tan Brown,Obsidian Black",
        "images": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "stock": 30,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Retro Canvas Platform Sneakers",
        "brand": "Urban Halo",
        "description": "70s heritage low-top canvas sneakers featuring chunky vulcanized soles and cushioned ortholite insoles.",
        "category": "Footwear",
        "price": 98.00,
        "discount": 10,
        "sizes": "36,37,38,39,40,41,42",
        "colors": "Off-White,Mustard,Forest Green",
        "images": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "stock": 55,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Minimalist Calfskin Leather Loafers",
        "brand": "Viora",
        "description": "Sleek penny loafer silhouette with a square toe, buttery soft calfskin lining, and flexible leather outsole.",
        "category": "Footwear",
        "price": 165.00,
        "discount": 12,
        "sizes": "38,39,40,41,42,43",
        "colors": "Burgundy,Black",
        "images": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "stock": 24,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Chunky Sole Trail Runner Sneakers",
        "brand": "ThreadTheory",
        "description": "Technical mesh and suede overlay upper with high-traction Vibram outsole and reflective accents.",
        "category": "Footwear",
        "price": 140.00,
        "discount": 0,
        "sizes": "40,41,42,43,44,45",
        "colors": "Concrete Grey,Neon Sage,Black",
        "images": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80",
        "rating": 4.6,
        "stock": 40,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Architectural Crossbody Shoulder Bag",
        "brand": "Luna Wardrobe",
        "description": "Sculptural geometric leather bag with magnetic flap closure and adjustable gold-tone chain strap.",
        "category": "Accessories",
        "price": 175.00,
        "discount": 15,
        "sizes": "One Size",
        "colors": "Cognac Leather,Black,Cream",
        "images": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "stock": 18,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Polarized Acetate Sunglasses",
        "brand": "Ember and Loom",
        "description": "Hand-polished Mazzucchelli acetate frames paired with UV400 anti-reflective polarized dark green lenses.",
        "category": "Accessories",
        "price": 85.00,
        "discount": 20,
        "sizes": "One Size",
        "colors": "Tortoiseshell,Matte Black",
        "images": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "stock": 60,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Brushed Stainless Steel Chronograph Watch",
        "brand": "NorthThread",
        "description": "40mm minimalist dial with Japanese quartz movement, sapphire crystal glass, and interchangeable mesh strap.",
        "category": "Accessories",
        "price": 195.00,
        "discount": 10,
        "sizes": "40mm",
        "colors": "Silver/White,All Black,Rose Gold",
        "images": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "stock": 22,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Pure Silk Editorial Pattern Scarf",
        "brand": "Aurelia Studio",
        "description": "100% twill silk square scarf printed with abstract fashion motifs. Rolled edge hem crafted by hand.",
        "category": "Accessories",
        "price": 65.00,
        "discount": 0,
        "sizes": "90x90cm",
        "colors": "Gold/Navy,Earthy Terracotta",
        "images": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?auto=format&fit=crop&w=800&q=80",
        "rating": 4.5,
        "stock": 35,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Textured Minimalist Leather Wallet",
        "brand": "Solace Street",
        "description": "Compact bi-fold wallet featuring RFID blocking protection, 6 card slots, and full-grain pebbled leather finish.",
        "category": "Accessories",
        "price": 55.00,
        "discount": 5,
        "sizes": "Standard",
        "colors": "Charcoal,Espresso Brown",
        "images": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
        "rating": 4.6,
        "stock": 50,
        "is_new": 0,
        "is_seasonal": 0
    },
    {
        "name": "Monochrome Ribbed Beanie",
        "brand": "Urban Halo",
        "description": "Chunky knit beanie made from recycled wool blend. Turn-up cuff with woven brand tab.",
        "category": "Accessories",
        "price": 42.00,
        "discount": 0,
        "sizes": "One Size",
        "colors": "Black,Camel,Melange Grey",
        "images": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=800&q=80",
        "rating": 4.4,
        "stock": 70,
        "is_new": 0,
        "is_seasonal": 1
    },
    {
        "name": "Draped Velvet Evening Gown",
        "brand": "Viora",
        "description": "Floor-length evening gown cut from heavy silk velvet. Thigh-high slit and cowl neck back detail.",
        "category": "Seasonal Collection",
        "price": 280.00,
        "discount": 25,
        "sizes": "XS,S,M,L",
        "colors": "Deep Ruby,Midnight Blue",
        "images": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=80",
        "rating": 5.0,
        "stock": 15,
        "is_new": 0,
        "is_seasonal": 1
    },
    {
        "name": "Thermal Puffer Vest",
        "brand": "NorthThread",
        "description": "Water-resistant matte shell filled with 700-fill down insulation. Fleece-lined handwarmer pockets.",
        "category": "Seasonal Collection",
        "price": 125.00,
        "discount": 15,
        "sizes": "S,M,L,XL",
        "colors": "Matte Olive,Jet Black",
        "images": "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
        "rating": 4.6,
        "stock": 30,
        "is_new": 0,
        "is_seasonal": 1
    },
    {
        "name": "Raw Edge Oversized Graphic Tee",
        "brand": "ThreadTheory",
        "description": "Heavy 260gsm combed cotton short-sleeve tee with vintage wash effect and subtle front typography.",
        "category": "New Arrivals",
        "price": 48.00,
        "discount": 0,
        "sizes": "S,M,L,XL",
        "colors": "Washed Grey,Off-White",
        "images": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?auto=format&fit=crop&w=800&q=80",
        "rating": 4.7,
        "stock": 80,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Satin Wrap Slip Skirt",
        "brand": "Luna Wardrobe",
        "description": "High-shine satin skirt with bias-cut drape and tie waist. Moves gracefully with every step.",
        "category": "New Arrivals",
        "price": 89.00,
        "discount": 10,
        "sizes": "XS,S,M,L",
        "colors": "Champagne,Emerald Green",
        "images": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1577900232427-18219b9166a0?auto=format&fit=crop&w=800&q=80",
        "rating": 4.8,
        "stock": 32,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Quilted Travel Weekender Bag",
        "brand": "Ember and Loom",
        "description": "Spacious duffle bag crafted from water-repellent nylon with leather handles, shoe compartment, and trolley sleeve.",
        "category": "New Arrivals",
        "price": 160.00,
        "discount": 12,
        "sizes": "One Size",
        "colors": "Olive Green,Midnight Black",
        "images": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=800&q=80",
        "rating": 4.9,
        "stock": 25,
        "is_new": 1,
        "is_seasonal": 0
    },
    {
        "name": "Urban Utility Cargo Pants",
        "brand": "Urban Halo",
        "description": "Tactical cotton ripstop pants featuring 6 functional pockets, adjustable drawstring cuffs, and articulated knees.",
        "category": "New Arrivals",
        "price": 105.00,
        "discount": 15,
        "sizes": "30,32,34,36",
        "colors": "Camo Olive,Stealth Black",
        "images": "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80",
        "rating": 4.6,
        "stock": 40,
        "is_new": 1,
        "is_seasonal": 0
    }
]

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def seed_db_tier():
    init_db_tier()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM cart_items")
    cursor.execute("DELETE FROM wishlist")

    pwd_hash = hash_password("vyra2026")
    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                   ("Elena Rostova", "elena@vyra.fashion", pwd_hash))
    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                   ("Marcus Vance", "marcus@vyra.fashion", pwd_hash))

    for p in PRODUCTS:
        cursor.execute("""
        INSERT INTO products (name, brand, description, category, price, discount, sizes, colors, images, rating, stock, is_new, is_seasonal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["name"], p["brand"], p["description"], p["category"],
            p["price"], p["discount"], p["sizes"], p["colors"],
            p["images"], p["rating"], p["stock"], p["is_new"], p["is_seasonal"]
        ))

    conn.commit()
    conn.close()
    print("Database Tier seeded successfully.")

if __name__ == "__main__":
    seed_db_tier()
