CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL,
  name VARCHAR(50) NOT NULL,
  password VARCHAR(128) NOT NULL,
  role ENUM('admin', 'teacher') NOT NULL DEFAULT 'teacher'
);

CREATE TABLE personal_development_areas (
  id INT NOT NULL AUTO_INCREMENT,
  content TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE schools (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL
);

CREATE TABLE teachers (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  mobile_number VARCHAR(20) NOT NULL,
  school_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (school_id) REFERENCES schools (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);

ALTER TABLE users ADD password_reset_token VARCHAR(35), ADD password_reset_token_created_at DATETIME DEFAULT NULL;

CREATE TABLE tests (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(30), teacher_id INT , FOREIGN KEY(teacher_id) REFERENCES teachers(id));

CREATE TABLE questions (id INT AUTO_INCREMENT PRIMARY KEY,question_text VARCHAR(30), test_id INT , FOREIGN KEY(test_id) REFERENCES tests(id));

CREATE TABLE choices (id INT AUTO_INCREMENT PRIMARY KEY,choice_text VARCHAR(30), is_correct BOOLEAN, question_id INT , FOREIGN KEY(question_id) REFERENCES questions(id));