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