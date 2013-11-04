-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.OtherAccount
-- Database: mysql
CREATE TABLE other_account (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    quantity INT,
    amount DECIMAL(10, 2),
    other_report_id INT
)

-- Constraints:
ALTER TABLE other_account ADD CONSTRAINT other_account_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
ALTER TABLE other_account ADD CONSTRAINT other_account_other_report_id_exists FOREIGN KEY (other_report_id) REFERENCES other_report (id) 
