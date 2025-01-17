PRAGMA foreign_keys = ON;
-- initial data for users --
INSERT INTO users(username, fullname, email, filename, password, created)
VALUES (
    'awdeorio', 
    'Andrew DeOrio', 
    'awdeorio@umich.edu',
    'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg',
    'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8',
    '2017-06-20 15:47:02'
);
INSERT INTO users(username, fullname, email, filename, password, created)
VALUES (
    'jflinn', 
    'Jason Flinn', 
    'jflinn@umich.edu',
    '505083b8b56c97429a728b68f31b0b2a089e5113.jpg',
    'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8',
    '2017-06-20 15:47:02'
);
INSERT INTO users(username, fullname, email, filename, password, created)
VALUES (
    'michjc', 
    'Michael Cafarella', 
    'michjc@umich.edu',
    '5ecde7677b83304132cb2871516ea50032ff7a4f.jpg',
    'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8',
    '2017-06-20 15:47:02'
);
INSERT INTO users(username, fullname, email, filename, password, created)
VALUES (
    'jag', 
    'H.V. Jagadish', 
    'jag@umich.edu',
    '73ab33bd357c3fd42292487b825880958c595655.jpg',
    'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8',
    '2017-06-20 15:47:02'
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
INSERT INTO likes(owner, postid, created)
VALUES(
    'awdeorio',
    1,
    '2017-06-20 15:47:02'
);
INSERT INTO likes(owner, postid, created)
VALUES(
    'michjc',
    1,
    '2017-06-20 15:47:02'
);
INSERT INTO likes(owner, postid, created)
VALUES(
    'jflinn',
    1,
    '2017-06-20 15:47:02'
);
INSERT INTO likes(owner, postid, created)
VALUES(
    'awdeorio',
    2,
    '2017-06-20 15:47:02'
);
INSERT INTO likes(owner, postid, created)
VALUES(
    'michjc',
    2,
    '2017-06-20 15:47:02'
);
INSERT INTO likes(owner, postid, created)
VALUES(
    'awdeorio',
    3,
    '2017-06-20 15:47:02'
);

--initial data for following --
INSERT INTO following(username1, username2, created)
VALUES(
    'awdeorio',
    'jflinn',
    '2017-06-20 15:47:02'
);
INSERT INTO following(username1, username2, created)
VALUES(
    'awdeorio',
    'michjc',
    '2017-06-20 15:47:02'
);
INSERT INTO following(username1, username2, created)
VALUES(
    'jflinn',
    'awdeorio',
    '2017-06-20 15:47:02'
);
INSERT INTO following(username1, username2, created)
VALUES(
    'jflinn',
    'michjc',
    '2017-06-20 15:47:02'
);
INSERT INTO following(username1, username2, created)
VALUES(
    'michjc',
    'awdeorio',
    '2017-06-20 15:47:02'
);
INSERT INTO following(username1, username2, created)
VALUES(
    'michjc',
    'jag',
    '2017-06-20 15:47:02'
);
INSERT INTO following(username1, username2, created)
VALUES(
    'jag',
    'michjc',
    '2017-06-20 15:47:02'
);

-- initial data for comments --
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'awdeorio',
    '#chickensofinstagram',
    3,
    '2017-06-20 15:47:02'
);
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'jflinn',
    'I <3 chickens',
    3,
    '2017-06-20 15:47:02'
);
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'michjc',
    'Cute overload!',
    3,
    '2017-06-20 15:47:02'
);
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'awdeorio',
    'Sick #crossword',
    2,
    '2017-06-20 15:47:02'
);
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'jflinn',
    'Walking the plank #chickensofinstagram',
    1,
    '2017-06-20 15:47:02'
);
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'awdeorio',
    'This was after trying to teach them to do a #crossword',
    1,
    '2017-06-20 15:47:02'
);
INSERT INTO comments(owner, text, postid, created)
VALUES(
    'jag',
    'Saw this on the diag yesterday!',
    4,
    '2017-06-20 15:47:02'
);
