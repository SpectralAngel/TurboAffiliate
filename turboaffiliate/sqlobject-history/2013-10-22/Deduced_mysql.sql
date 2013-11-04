-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Deduced
-- Database: mysql
CREATE TABLE deduced (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    amount DECIMAL(10, 2),
    account_id INT,
    detail TEXT,
    month INT,
    year INT
)

-- Constraints:
ALTER TABLE deduced ADD CONSTRAINT deduced_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
ALTER TABLE deduced ADD CONSTRAINT deduced_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
