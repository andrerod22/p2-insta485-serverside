PRAGMA foreign_keys = ON;
-- initial data for users --
INSERT INTO users(username, fullname, email, filename, password)
VALUES (
    'awdeorio', 
    'Andrew DeOrio', 
    'awdeorio@umich.edu',
    'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg',
    'password'
);
INSERT INTO users(username, fullname, email, filename, password)
VALUES (
    'jflinn', 
    'Jason Flinn', 
    'jflinn@umich.edu',
    '505083b8b56c97429a728b68f31b0b2a089e5113.jpg',
    'password'
);
INSERT INTO users(username, fullname, email, filename, password)
VALUES (
    'michjc', 
    'Michael Cafarella', 
    'michjc@umich.edu',
    '5ecde7677b83304132cb2871516ea50032ff7a4f.jpg',
    'password'
);
INSERT INTO users(username, fullname, email, filename, password)
VALUES (
    'jag', 
    'H.V. Jagadish', 
    'jag@umich.edu',
    '73ab33bd357c3fd42292487b825880958c595655.jpg',
    'password'
);

-- initial data for posts --
INSERT INTO posts(filename, owner)
VALUES(
    '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg',
    'awdeorio'
);
INSERT INTO posts(filename, owner)
VALUES(
    'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg',
    'jflinn'
);
INSERT INTO posts(filename, owner)
VALUES(
    '9887e06812ef434d291e4936417d125cd594b38a.jpg',
    'awdeorio'
);
INSERT INTO posts(filename, owner)
VALUES(
    '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg',
    'jag'
);

-- initial data for likes --
INSERT INTO likes(owner, postid)
VALUES(
    'awdeorio',
    1
);
INSERT INTO likes(owner, postid)
VALUES(
    'michjc',
    1
);
INSERT INTO likes(owner, postid)
VALUES(
    'jflinn',
    1
);
INSERT INTO likes(owner, postid)
VALUES(
    'awdeorio',
    2
);
INSERT INTO likes(owner, postid)
VALUES(
    'michjc',
    2
);
INSERT INTO likes(owner, postid)
VALUES(
    'awdeorio',
    3
);

--initial data for following --
INSERT INTO following(username1, username2)
VALUES(
    'awdeorio',
    'jflinn'
);
INSERT INTO following(username1, username2)
VALUES(
    'awdeorio',
    'michjc'
);
INSERT INTO following(username1, username2)
VALUES(
    'jflinn',
    'awdeorio'
);
INSERT INTO following(username1, username2)
VALUES(
    'jflinn',
    'michjc'
);
INSERT INTO following(username1, username2)
VALUES(
    'michjc',
    'awdeorio'
);
INSERT INTO following(username1, username2)
VALUES(
    'michjc',
    'jag'
);
INSERT INTO following(username1, username2)
VALUES(
    'jag',
    'michjc'
);

-- initial data for comments --
INSERT INTO comments(owner, text)
VALUES(
    'awdeorio',
    '#chickensofinstagram'
);
INSERT INTO comments(owner, text)
VALUES(
    'jflinn',
    'I <3 chickens'
);
INSERT INTO comments(owner, text)
VALUES(
    'michjc',
    'Cute overload!'
);
INSERT INTO comments(owner, text)
VALUES(
    'awdeorio',
    'Sick #crossword'
);
INSERT INTO comments(owner, text)
VALUES(
    'jflinn',
    'Walking the plank #chickensofinstagram'
);
INSERT INTO comments(owner, text)
VALUES(
    'awdeorio',
    'This was after trying to teach them to do a #crossword'
);
INSERT INTO comments(owner, text)
VALUES(
    'jag',
    'Saw this on the diag yesterday!'
);
