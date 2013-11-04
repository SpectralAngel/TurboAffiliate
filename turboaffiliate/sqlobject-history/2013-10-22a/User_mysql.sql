-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.User
-- Database: mysql
CREATE TABLE tg_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(16) NOT NULL UNIQUE,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    password VARCHAR(40),
    created DATETIME,
    casa_id INT
)

-- Constraints:
ALTER TABLE tg_user ADD CONSTRAINT tg_user_casa_id_exists FOREIGN KEY (casa_id) REFERENCES casa (id) 
