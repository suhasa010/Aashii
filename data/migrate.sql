CREATE TEMPORARY TABLE tempinvite (
    user_id BIGINT,
    message_id INTEGER,
    links_count INTEGER,
    pending BOOL
);

INSERT INTO tempinvite (SELECT user_id, MAX(message_id), COUNT(message_id), FALSE FROM invite_links GROUP BY user_id);

DROP TABLE invite_links;

CREATE TABLE invite_links (
    user_id BIGINT PRIMARY KEY REFERENCES users,
    message_id INTEGER NOT NULL,
    links_count INTEGER NOT NULL DEFAULT 1,
    pending BOOL NOT NULL DEFAULT FALSE
);

INSERT INTO invite_links (SELECT * from tempinvite);
DROP TABLE tempinvite;
