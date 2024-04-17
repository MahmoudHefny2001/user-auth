CREATE TABLE "users" (
  "id" int PRIMARY KEY,
  "role" varchar(50) NOT NULL,
  "full_name" varchar(100) NOT NULL,
  "email" varchar UNIQUE,
  "password" varchar(128),
  "phone_number" varchar(20) UNIQUE,
  "is_superuser" boolean DEFAULT false,
  "is_staff" boolean DEFAULT false,
  "created_at" timestamp
);

CREATE TABLE "customers" (
  "id" int PRIMARY KEY,
  "address" text,
  "created_at" timestamp
);

CREATE TABLE "customer_profiles" (
  "id" int PRIMARY KEY,
  "customer_id" int UNIQUE,
  "birth_date" date,
  "image" varchar,
  "bio" text,
  "created_at" timestamp
);

CREATE TABLE "merchants" (
  "id" int PRIMARY KEY,
  "address" text,
  "payment_information" text,
  "terms_agreement" boolean DEFAULT false,
  "created_at" timestamp
);

CREATE TABLE "merchant_profiles" (
  "id" int PRIMARY KEY,
  "merchant_id" int UNIQUE,
  "image" varchar,
  "merchant_zip_code" varchar(100),
  "tax_id" varchar(20),
  "logo" varchar,
  "website_url" varchar,
  "facebook_url" varchar,
  "twitter_url" varchar,
  "instagram_url" varchar,
  "linkedin_url" varchar,
  "shipping_address" text,
  "shipping_options" varchar(100),
  "about_us" text,
  "return_policy" text,
  "created_at" timestamp
);

CREATE TABLE "wishlists" (
  "id" int PRIMARY KEY,
  "customer_id" int,
  "product_id" int,
  "created_at" timestamp
);

CREATE TABLE "product_reviews" (
  "id" int PRIMARY KEY,
  "product_id" int,
  "customer_id" int,
  "rating" int,
  "review" text,
  "created_at" timestamp
);

CREATE TABLE "categories" (
  "id" int PRIMARY KEY,
  "name" varchar(255) NOT NULL,
  "description" text NOT NULL,
  "created_at" timestamp
);

CREATE TABLE "products" (
  "id" int PRIMARY KEY,
  "bar_code" varchar(255) UNIQUE,
  "name" varchar(255) NOT NULL,
  "description" text NOT NULL,
  "price" decimal(10,2) NOT NULL,
  "quantity" int NOT NULL,
  "image" varchar,
  "category_id" int,
  "available" boolean DEFAULT true,
  "on_sale" boolean DEFAULT false,
  "sale_percent" int DEFAULT 0,
  "price_after_sale" decimal(10,2),
  "colors" jsonb,
  "created_at" timestamp
);

CREATE TABLE "product_attachments" (
  "id" int PRIMARY KEY,
  "product_id" int,
  "attachment" varchar,
  "created_at" timestamp
);

CREATE TABLE "orders" (
  "id" int PRIMARY KEY,
  "status" varchar(50) NOT NULL,
  "user_id" int,
  "total_price" decimal(10,2) DEFAULT 0,
  "created_at" timestamp
);

CREATE TABLE "order_items" (
  "id" int PRIMARY KEY,
  "order_id" int,
  "product_id" int,
  "sub_total_price" decimal(10,2) DEFAULT 0,
  "created_at" timestamp
);

CREATE TABLE "contact_form" (
  "id" int PRIMARY KEY,
  "name" varchar(100) NOT NULL,
  "email" varchar NOT NULL,
  "phone_number" varchar(12),
  "message" text NOT NULL,
  "created_at" timestamp
);

CREATE TABLE "carts" (
  "id" int PRIMARY KEY,
  "customer_id" int,
  "product_id" int,
  "created_at" timestamp
);

ALTER TABLE "customers" ADD FOREIGN KEY ("id") REFERENCES "users" ("id");

ALTER TABLE "customer_profiles" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "customer_profiles" ADD FOREIGN KEY ("image") REFERENCES "merchant_profiles" ("id");

ALTER TABLE "merchants" ADD FOREIGN KEY ("id") REFERENCES "users" ("id");

ALTER TABLE "merchant_profiles" ADD FOREIGN KEY ("merchant_id") REFERENCES "merchants" ("id");

ALTER TABLE "wishlists" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "wishlists" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "product_reviews" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "product_reviews" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "products" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id");

ALTER TABLE "product_attachments" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("user_id") REFERENCES "customers" ("id");

ALTER TABLE "order_items" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");

ALTER TABLE "order_items" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");

ALTER TABLE "carts" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "carts" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id");