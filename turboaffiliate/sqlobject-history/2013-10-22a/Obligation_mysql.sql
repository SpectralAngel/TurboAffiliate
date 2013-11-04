-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Obligation
-- Database: mysql
CREATE TABLE obligation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    amount DECIMAL(10, 2) NOT NULL,
    inprema DECIMAL(10, 2) NOT NULL,
    month INT,
    year INT,
    account_id INT,
    filiales DECIMAL(10, 2) NOT NULL
)

-- Constraints:
ALTER TABLE obligation ADD CONSTRAINT obligation_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
