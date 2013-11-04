-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.OldPay
-- Database: mysql
CREATE TABLE old_pay (
    id INT PRIMARY KEY AUTO_INCREMENT,
    payed_loan_id INT,
    day DATE,
    capital DECIMAL(10, 2) NOT NULL,
    interest DECIMAL(10, 2) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    receipt VARCHAR(50),
    description VARCHAR(100)
)

-- Constraints:
ALTER TABLE old_pay ADD CONSTRAINT old_pay_payed_loan_id_exists FOREIGN KEY (payed_loan_id) REFERENCES payed_loan (id) 
