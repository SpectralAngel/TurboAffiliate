-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.VisitIdentity
-- Database: mysql
CREATE TABLE visit_identity (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visit_key VARCHAR(40) NOT NULL UNIQUE,
    user_id INT
)
