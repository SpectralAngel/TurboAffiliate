-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Logger
-- Database: mysql
CREATE TABLE logger (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action TEXT,
    day DATETIME
)

-- Constraints:
ALTER TABLE logger ADD CONSTRAINT logger_user_id_exists FOREIGN KEY (user_id) REFERENCES tg_user (id) 
