PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO users VALUES(9,'Elena Rostova','elena@vyra.fashion','a3dc68deb3d49ee93bb191bf1d0abf72721672d691580d7152c88058153a0df4','2026-08-20 20:04:28');
INSERT INTO users VALUES(10,'Marcus Vance','marcus@vyra.fashion','a3dc68deb3d49ee93bb191bf1d0abf72721672d691580d7152c88058153a0df4','2026-08-20 20:04:28');
CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        brand TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        discount INTEGER DEFAULT 0,
        sizes TEXT NOT NULL, -- JSON or comma-separated: S,M,L,XL
        colors TEXT NOT NULL, -- JSON or comma-separated: Black,Cream,Olive
        images TEXT NOT NULL, -- Pipe separated image URLs
        rating REAL DEFAULT 4.5,
        stock INTEGER DEFAULT 50,
        is_new INTEGER DEFAULT 0,
        is_seasonal INTEGER DEFAULT 0
    );
INSERT INTO products VALUES(105,'Minimalist Silk Trench Coat','Aurelia Studio','Crafted from fluid mulberry silk-blend fabric, this double-breasted trench coat offers an airy editorial silhouette with storm flaps and a waist tie belt.','Women',189.0,15,'XS,S,M,L','Beige,Charcoal,Sage','https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80',4.799999999999999823,35,1,0);
INSERT INTO products VALUES(106,'Oversized Cashmere Knit Sweater','Luna Wardrobe','Ultra-soft grade-A cashmere knit with dropped shoulders and ribbed cuffs. Designed for cozy warmth and effortlessness.','Women',129.0,10,'S,M,L,XL','Cream,Oatmeal,Dusty Rose','https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=800&q=80',4.700000000000000177,42,0,1);
INSERT INTO products VALUES(107,'Sculpted Tailored Blazer','Viora','Precision-tailored single-breasted blazer featuring padded shoulders, welt pockets, and a cinch waist silhouette.','Women',159.0,20,'XS,S,M,L','Midnight Black,Ivory,Olive','https://images.unsplash.com/photo-1584273143981-41c073dfe8f8?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80',4.900000000000000355,28,1,0);
INSERT INTO products VALUES(108,'Fluid Wide-Leg Linen Trousers','Ember and Loom','High-waisted wide leg pants tailored in breathable European linen. Elastic back waistband for peak comfort.','Women',95.0,0,'XS,S,M,L,XL','Sand,White,Terracotta','https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1551803091-e20673f15770?auto=format&fit=crop&w=800&q=80',4.599999999999999644,50,0,0);
INSERT INTO products VALUES(109,'Asymmetric Pleated Midi Dress','Solace Street','Architectural pleated silhouette with asymmetrical neckline and fluid movement for modern evening occasions.','Women',145.0,12,'S,M,L','Emerald,Champagne,Black','https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=800&q=80',4.799999999999999823,20,0,1);
INSERT INTO products VALUES(110,'Structured Wool Double-Breasted Coat','NorthThread','Heavyweight Italian wool coat featuring sharp lapels, deep side pockets, and satin lining. Built for cold winters.','Men',210.0,25,'S,M,L,XL','Camel,Navy,Charcoal','https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=800&q=80',4.900000000000000355,25,0,1);
INSERT INTO products VALUES(111,'Japanese Selvage Denim Jacket','Urban Halo','14oz raw selvage denim crafted in Okayama. Features custom brass hardware, dual chest pockets, and contrast stitching.','Men',135.0,10,'S,M,L,XL','Indigo Wash,Washed Black','https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80',4.700000000000000177,38,1,0);
INSERT INTO products VALUES(112,'Relaxed Merino Wool Hoodie','ThreadTheory','Elevated loungewear spun from extrafine Australian merino wool. Double-layer hood and clean seamless finish.','Men',110.0,5,'S,M,L,XL','Heather Grey,Dark Moss,Black','https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1509967419530-da38b4704bc6?auto=format&fit=crop&w=800&q=80',4.5,45,0,0);
INSERT INTO products VALUES(113,'Slim Fit Cotton Oxford Shirt','NorthThread','Classic button-down shirt woven from 100% organic Supima cotton. Garment washed for subtle softness.','Men',79.0,0,'S,M,L,XL','Sky Blue,Classic White,Pink Stripe','https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=800&q=80',4.599999999999999644,60,0,0);
INSERT INTO products VALUES(114,'Pleated Tapered Chino Pants','Solace Street','Contemporary pleated chinos with a gentle taper, horn button closure, and stretch cotton twill weave.','Men',88.0,15,'30,32,34,36','Khaki,Olive,Navy','https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80',4.400000000000000356,40,0,0);
INSERT INTO products VALUES(115,'Handcrafted Italian Leather Chelsea Boots','Aurelia Studio','Full-grain Tuscan calf leather upper, Goodyear welted rubber soles, and elastic side gussets for effortless slip-on style.','Footwear',220.0,18,'39,40,41,42,43,44','Tan Brown,Obsidian Black','https://images.unsplash.com/photo-1638247025967-b4e38f787b76?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&w=800&q=80',4.900000000000000355,30,1,0);
INSERT INTO products VALUES(116,'Retro Canvas Platform Sneakers','Urban Halo','70s heritage low-top canvas sneakers featuring chunky vulcanized soles and cushioned ortholite insoles.','Footwear',98.0,10,'36,37,38,39,40,41,42','Off-White,Mustard,Forest Green','https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80',4.700000000000000177,55,0,0);
INSERT INTO products VALUES(117,'Minimalist Calfskin Leather Loafers','Viora','Sleek penny loafer silhouette with a square toe, buttery soft calfskin lining, and flexible leather outsole.','Footwear',165.0,12,'38,39,40,41,42,43','Burgundy,Black','https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=800&q=80',4.799999999999999823,24,0,0);
INSERT INTO products VALUES(118,'Chunky Sole Trail Runner Sneakers','ThreadTheory','Technical mesh and suede overlay upper with high-traction Vibram outsole and reflective accents.','Footwear',140.0,0,'40,41,42,43,44,45','Concrete Grey,Neon Sage,Black','https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80',4.599999999999999644,40,1,0);
INSERT INTO products VALUES(119,'Architectural Crossbody Shoulder Bag','Luna Wardrobe','Sculptural geometric leather bag with magnetic flap closure and adjustable gold-tone chain strap.','Accessories',175.0,15,'One Size','Cognac Leather,Black,Cream','https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=800&q=80',4.900000000000000355,18,1,0);
INSERT INTO products VALUES(120,'Polarized Acetate Sunglasses','Ember and Loom','Hand-polished Mazzucchelli acetate frames paired with UV400 anti-reflective polarized dark green lenses.','Accessories',85.0,20,'One Size','Tortoiseshell,Matte Black','https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80',4.700000000000000177,60,0,0);
INSERT INTO products VALUES(121,'Brushed Stainless Steel Chronograph Watch','NorthThread','40mm minimalist dial with Japanese quartz movement, sapphire crystal glass, and interchangeable mesh strap.','Accessories',195.0,10,'40mm','Silver/White,All Black,Rose Gold','https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80',4.799999999999999823,22,0,0);
INSERT INTO products VALUES(122,'Pure Silk Editorial Pattern Scarf','Aurelia Studio','100% twill silk square scarf printed with abstract fashion motifs. Rolled edge hem crafted by hand.','Accessories',65.0,0,'90x90cm','Gold/Navy,Earthy Terracotta','https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?auto=format&fit=crop&w=800&q=80',4.5,35,0,0);
INSERT INTO products VALUES(123,'Textured Minimalist Leather Wallet','Solace Street','Compact bi-fold wallet featuring RFID blocking protection, 6 card slots, and full-grain pebbled leather finish.','Accessories',55.0,5,'Standard','Charcoal,Espresso Brown','https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80',4.599999999999999644,50,0,0);
INSERT INTO products VALUES(124,'Monochrome Ribbed Beanie','Urban Halo','Chunky knit beanie made from recycled wool blend. Turn-up cuff with woven brand tab.','Accessories',42.0,0,'One Size','Black,Camel,Melange Grey','https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=800&q=80',4.400000000000000356,70,0,1);
INSERT INTO products VALUES(125,'Draped Velvet Evening Gown','Viora','Floor-length evening gown cut from heavy silk velvet. Thigh-high slit and cowl neck back detail.','Seasonal Collection',280.0,25,'XS,S,M,L','Deep Ruby,Midnight Blue','https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=80',5.0,15,0,1);
INSERT INTO products VALUES(126,'Thermal Puffer Vest','NorthThread','Water-resistant matte shell filled with 700-fill down insulation. Fleece-lined handwarmer pockets.','Seasonal Collection',125.0,15,'S,M,L,XL','Matte Olive,Jet Black','https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80',4.599999999999999644,30,0,1);
INSERT INTO products VALUES(127,'Raw Edge Oversized Graphic Tee','ThreadTheory','Heavy 260gsm combed cotton short-sleeve tee with vintage wash effect and subtle front typography.','New Arrivals',48.0,0,'S,M,L,XL','Washed Grey,Off-White','https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?auto=format&fit=crop&w=800&q=80',4.700000000000000177,80,1,0);
INSERT INTO products VALUES(128,'Satin Wrap Slip Skirt','Luna Wardrobe','High-shine satin skirt with bias-cut drape and tie waist. Moves gracefully with every step.','New Arrivals',89.0,10,'XS,S,M,L','Champagne,Emerald Green','https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1577900232427-18219b9166a0?auto=format&fit=crop&w=800&q=80',4.799999999999999823,32,1,0);
INSERT INTO products VALUES(129,'Quilted Travel Weekender Bag','Ember and Loom','Spacious duffle bag crafted from water-repellent nylon with leather handles, shoe compartment, and trolley sleeve.','New Arrivals',160.0,12,'One Size','Olive Green,Midnight Black','https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=800&q=80',4.900000000000000355,25,1,0);
INSERT INTO products VALUES(130,'Urban Utility Cargo Pants','Urban Halo','Tactical cotton ripstop pants featuring 6 functional pockets, adjustable drawstring cuffs, and articulated knees.','New Arrivals',105.0,15,'30,32,34,36','Camo Olive,Stealth Black','https://images.unsplash.com/photo-1517445312882-bc9910d016b7?auto=format&fit=crop&w=800&q=80|https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80',4.599999999999999644,40,1,0);
CREATE TABLE wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id)
    );
CREATE TABLE cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        size TEXT NOT NULL,
        color TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id, size, color)
    );
CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        subtotal REAL NOT NULL,
        discount_amount REAL NOT NULL,
        delivery_fee REAL NOT NULL,
        total_amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        payment_status TEXT NOT NULL,
        order_status TEXT DEFAULT 'Order Placed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO orders VALUES(1,'VYRA-1E499E27',1,'Elena Rostova','elena@vyra.fashion','742 Fashion Boulevard, Suite 400','New York','10001',284.0,28.35000000000000142,0.0,255.6500000000000056,'UPI','SUCCESS','Order Placed','2026-08-20 19:41:48');
INSERT INTO orders VALUES(2,'VYRA-D5AC9131',1,'Elena Rostova','elena@vyra.fashion','742 Fashion Boulevard, Suite 400','New York','10001',129.0,12.90000000000000035,15.0,131.0999999999999944,'UPI','SUCCESS','Order Placed','2026-08-20 19:44:57');
INSERT INTO orders VALUES(3,'VYRA-678256FE',1,'Elena Rostova','elena@vyra.fashion','742 Fashion Boulevard, Suite 400','New York','10001',189.0,28.35000000000000142,0.0,160.6500000000000056,'UPI','SUCCESS','Order Placed','2026-08-20 19:57:53');
INSERT INTO orders VALUES(4,'VYRA-0FAB6869',1,'Elena Rostova','elena@vyra.fashion','742 Fashion Boulevard, Suite 400','New York','10001',318.0,41.25,0.0,276.75,'Credit / Debit Card','SUCCESS','Order Placed','2026-08-20 20:06:36');
CREATE TABLE order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        size TEXT NOT NULL,
        color TEXT NOT NULL,
        image_url TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    );
INSERT INTO order_items VALUES(1,1,79,'Minimalist Silk Trench Coat','Aurelia Studio',160.6500000000000056,1,'XS','Beige','https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80');
INSERT INTO order_items VALUES(2,1,82,'Fluid Wide-Leg Linen Trousers','Ember and Loom',95.0,1,'XS','Sand','https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=80');
INSERT INTO order_items VALUES(3,2,80,'Oversized Cashmere Knit Sweater','Luna Wardrobe',116.0999999999999944,1,'S','Cream','https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=800&q=80');
INSERT INTO order_items VALUES(4,3,79,'Minimalist Silk Trench Coat','Aurelia Studio',160.6500000000000056,1,'XS','Beige','https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80');
INSERT INTO order_items VALUES(5,4,105,'Minimalist Silk Trench Coat','Aurelia Studio',160.6500000000000056,1,'XS','Beige','https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80');
INSERT INTO order_items VALUES(6,4,106,'Oversized Cashmere Knit Sweater','Luna Wardrobe',116.0999999999999944,1,'S','Cream','https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=800&q=80');
INSERT INTO sqlite_sequence VALUES('users',10);
INSERT INTO sqlite_sequence VALUES('products',130);
INSERT INTO sqlite_sequence VALUES('cart_items',6);
INSERT INTO sqlite_sequence VALUES('orders',4);
INSERT INTO sqlite_sequence VALUES('order_items',6);
COMMIT;
