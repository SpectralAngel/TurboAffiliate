-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Extra
-- Database: mysql
CREATE TABLE extra (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    amount DECIMAL(10, 2),
    months INT,
    retrasada BOOL,
    account_id INT,
    mes INT,
    anio INT
)

-- Constraints:
ALTER TABLE extra ADD CONSTRAINT extra_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
ALTER TABLE extra ADD CONSTRAINT extra_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
