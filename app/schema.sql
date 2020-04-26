DROP TABLE IF EXISTS user;

CREATE TABLE user (
  username TEXT PRIMARY KEY NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  admin BIT /* 1 if admin, 0 if regular user*/
);

/* TO ADD: Questions, Comments, Results */