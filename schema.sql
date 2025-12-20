DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS attendance;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    name TEXT NOT NULL,
    subject TEXT
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    subject TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES users (id),
    FOREIGN KEY (teacher_id) REFERENCES users (id)
); 