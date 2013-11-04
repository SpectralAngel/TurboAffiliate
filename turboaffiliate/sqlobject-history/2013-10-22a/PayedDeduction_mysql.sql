-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.PayedDeduction
-- Database: mysql
CREATE TABLE payed_deduction (
    id INT PRIMARY KEY AUTO_INCREMENT,
    payed_loan_id INT,
    amount DECIMAL(10, 2),
    account_id INT,
    description TEXT
)

-- Constraints:
ALTER TABLE payed_deduction ADD CONSTRAINT payed_deduction_payed_loan_id_exists FOREIGN KEY (payed_loan_id) REFERENCES payed_loan (id) 
ALTER TABLE payed_deduction ADD CONSTRAINT payed_deduction_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
