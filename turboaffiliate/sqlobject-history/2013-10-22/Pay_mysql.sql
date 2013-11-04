-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Pay
-- Database: mysql
CREATE TABLE pay (
    id INT PRIMARY KEY AUTO_INCREMENT,
    loan_id INT,
    day DATE,
    capital DECIMAL(10, 2) NOT NULL,
    interest DECIMAL(10, 2) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    deposito BOOL,
    receipt VARCHAR(50),
    description VARCHAR(100)
)

-- Constraints:
ALTER TABLE pay ADD CONSTRAINT pay_loan_id_exists FOREIGN KEY (loan_id) REFERENCES loan (id) 
