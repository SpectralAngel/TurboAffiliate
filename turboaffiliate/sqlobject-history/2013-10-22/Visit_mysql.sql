-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Visit
-- Database: mysql
CREATE TABLE visit (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visit_key VARCHAR(40) NOT NULL UNIQUE,
    created DATETIME,
    expiry DATETIME
)
