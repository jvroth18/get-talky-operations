CREATE SCHEMA "get_talky_enum";

CREATE TABLE "configuration" (
  "id" int PRIMARY KEY,
  "client_id" uuid,
  "name" varchar(255),
  "elevenlabs_model" varchar(255),
  "elevenlabs_voice_id" varchar(255),
  "client_internal_id" varchar(255),
  "client_type_id" int,
  "about_us" varchar(255),
  "services" varchar(255),
  "locations" varchar(255)
);

CREATE TABLE "providers" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "first_name" varchar(255),
  "last_name" varchar(255),
  "phone_number" varchar(255),
  "email" varchar(255),
  "date_added" timestamp,
  "date_updated" timestamp,
  "active" bool
);

CREATE TABLE "request_types" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "name" varchar(255),
  "description" varchar(255),
  "length" int,
  "display_order" int,
  "active" bool
);

CREATE TABLE "interaction_types" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "phone_number" varchar(255),
  "phone_number_sid" varchar(255)
);

CREATE TABLE "locations" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "name" varchar(255),
  "phone_number" varchar(255),
  "operating_hours" varchar(255),
  "address" varchar(255)
);

CREATE TABLE "client_api_keys" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "name" varchar(255),
  "api_key" varchar(255),
  "active" bool,
  "date_added" timestamp
);

CREATE TABLE "billing_information" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "plaid_access_token" varchar(255),
  "date_added" timestamp,
  "active" bool
);

CREATE TABLE "users" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "first_name" varchar(255),
  "last_name" timestamp,
  "phone_number" varchar(255),
  "email" varchar(255),
  "role_id" int,
  "date_added" timestamp,
  "active" bool
);

CREATE TABLE "interaction" (
  "id" int PRIMARY KEY,
  "configuration_id" int,
  "interaction_type_id" int,
  "interaction_summary" varchar(255),
  "interactor_name" varchar(255),
  "interaction_category_id" int,
  "interactor_id" int,
  "request_id" int,
  "pet_id" int
);

CREATE TABLE "interactor" (
  "id" int PRIMARY KEY,
  "first_name" varchar(255),
  "last_name" varchar(255),
  "phone_number" varchar(255),
  "email" varchar(255),
  "verified" bool,
  "date_added" timestamp
);

CREATE TABLE "request" (
  "id" int PRIMARY KEY,
  "request_type_id" int,
  "provider_id" int,
  "request_time" timestamp
);

CREATE TABLE "pet" (
  "id" int PRIMARY KEY,
  "pet_type_id" int,
  "name" varchar(255),
  "age" int,
  "sex_id" int
);

CREATE TABLE "content" (
  "id" int PRIMARY KEY,
  "interaction_id" int,
  "interactor_role_id" int,
  "text" varchar(255),
  "timestamp" timestamp
);

CREATE TABLE "funnel" (
  "id" int PRIMARY KEY,
  "interaction_id" int,
  "entry_time" timestamp,
  "exit_time" timestamp,
  "interaction_block" varchar(255)
);

CREATE TABLE "get_talky_enum"."client_type" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "description" varchar(255),
  "active" bool,
  "display_order" int
);

CREATE TABLE "get_talky_enum"."user_role" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "description" varchar(255),
  "active" bool,
  "display_order" int
);

CREATE TABLE "get_talky_enum"."interactor_role" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "description" varchar(255),
  "active" bool,
  "display_order" int
);

CREATE TABLE "get_talky_enum"."pet_types" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "description" varchar(255),
  "active" bool,
  "display_order" int
);

CREATE TABLE "get_talky_enum"."sex" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "description" varchar(255),
  "active" bool,
  "display_order" int
);

CREATE TABLE "get_talky_enum"."interaction_category" (
  "id" int PRIMARY KEY,
  "name" varchar(255),
  "description" varchar(255),
  "active" bool,
  "display_order" int
);

ALTER TABLE "configuration" ADD FOREIGN KEY ("client_type_id") REFERENCES "get_talky_enum"."client_type" ("id");

ALTER TABLE "providers" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "request_types" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "locations" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "client_api_keys" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "billing_information" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "get_talky_enum"."user_role" ("id");

ALTER TABLE "interaction" ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");

ALTER TABLE "interaction" ADD FOREIGN KEY ("interaction_type_id") REFERENCES "interaction_types" ("id");

ALTER TABLE "interaction" ADD FOREIGN KEY ("interaction_category_id") REFERENCES "get_talky_enum"."interaction_category" ("id");

ALTER TABLE "interaction" ADD FOREIGN KEY ("interactor_id") REFERENCES "interactor" ("id");

ALTER TABLE "interaction" ADD FOREIGN KEY ("request_id") REFERENCES "request" ("id");

ALTER TABLE "interaction" ADD FOREIGN KEY ("pet_id") REFERENCES "pet" ("id");

ALTER TABLE "request" ADD FOREIGN KEY ("request_type_id") REFERENCES "request_types" ("id");

ALTER TABLE "request" ADD FOREIGN KEY ("provider_id") REFERENCES "providers" ("id");

ALTER TABLE "pet" ADD FOREIGN KEY ("pet_type_id") REFERENCES "get_talky_enum"."pet_types" ("id");

ALTER TABLE "pet" ADD FOREIGN KEY ("sex_id") REFERENCES "get_talky_enum"."sex" ("id");

ALTER TABLE "content" ADD FOREIGN KEY ("interaction_id") REFERENCES "interaction" ("id");

ALTER TABLE "content" ADD FOREIGN KEY ("interactor_role_id") REFERENCES "get_talky_enum"."interactor_role" ("id");

ALTER TABLE "funnel" ADD FOREIGN KEY ("interaction_id") REFERENCES "interaction" ("id");
