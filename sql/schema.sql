PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL,
  created DATETIME,
  PRIMARY KEY(username)
);

CREATE TABLE posts(
  postid INTEGER AUTOINCREMENT,
  filename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL,
  created DATETIME,

  PRIMARY KEY(postid)
  FOREIGN KEY(owner) REFERENCES users(username)
  ON DELETE CASCADE
);

CREATE TABLE following(
  username1 VARCHAR(20) NOT NULL,
  username2 VARCHAR(20) NOT NULL,
  created DATETIME,
  FOREIGN KEY(username1,username2)
  REFERENCES users(username)
  ON DELETE CASCADE
);


CREATE TABLE comments(
  commentid INTEGER AUTOINCREMENT,
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  text VARCHAR(1024) NOT NULL,
  created DATETIME,

  PRIMARY KEY(commentid)
  FOREIGN KEY(postid) REFERENCES posts(postid)
  FOREIGN KEY(owner) REFERENCES users(username)
  ON DELETE CASCADE
);


CREATE TABLE likes(
  likeid INTEGER AUTOINCREMENT,
  owner VARCHAR(20) NOT NULL,
  postid INTEGER NOT NULL,
  created DATETIME,
  PRIMARY KEY(likeid),
  FOREIGN KEY(owner) REFERENCES users(username)
  ON DELETE CASCADE
);
