-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Permission
-- Database: mysql
CREATE TABLE permission (
    id INT PRIMARY KEY AUTO_INCREMENT,
    permission_name VARCHAR(16) NOT NULL UNIQUE,
    description VARCHAR(255)
)
