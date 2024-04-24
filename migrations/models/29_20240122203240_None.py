from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cat" VARCHAR(44) NOT NULL
);
CREATE TABLE IF NOT EXISTS "contactmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(44) NOT NULL,
    "email" VARCHAR(44) NOT NULL,
    "message" VARCHAR(104) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "usermodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(44) NOT NULL,
    "password" VARCHAR(404) NOT NULL,
    "avatar" VARCHAR(404)
);
CREATE TABLE IF NOT EXISTS "blogmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(44) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category" VARCHAR(44),
    "image" VARCHAR(404),
    "owner_id" INT NOT NULL REFERENCES "usermodel" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "comment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "blog" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT REFERENCES "usermodel" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
