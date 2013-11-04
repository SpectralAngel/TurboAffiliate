-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Deduction
-- Database: mysql
CREATE TABLE deduction (
    id INT PRIMARY KEY AUTO_INCREMENT,
    loan_id INT,
    amount DECIMAL(10, 2),
    account_id INT,
    description VARCHAR(100)
)

-- Constraints:
ALTER TABLE deduction ADD CONSTRAINT deduction_loan_id_exists FOREIGN KEY (loan_id) REFERENCES loan (id) 
ALTER TABLE deduction ADD CONSTRAINT deduction_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
