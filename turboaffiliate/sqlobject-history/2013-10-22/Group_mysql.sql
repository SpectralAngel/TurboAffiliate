-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Group
-- Database: mysql
CREATE TABLE tg_group (
    id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(16) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    created DATETIME
);
CREATE TABLE user_group (
group_id INT NOT NULL,
user_id INT NOT NULL
);
CREATE TABLE group_permission (
group_id INT NOT NULL,
permission_id INT NOT NULL
)
