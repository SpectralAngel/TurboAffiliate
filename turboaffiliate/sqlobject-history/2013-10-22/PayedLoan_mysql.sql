-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.PayedLoan
-- Database: mysql
CREATE TABLE payed_loan (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    casa_id INT,
    capital DECIMAL(10, 2) NOT NULL,
    letters TEXT,
    payment DECIMAL(10, 2) NOT NULL,
    interest DECIMAL(4, 2) NOT NULL,
    months INT,
    last DATE,
    start_date DATE NOT NULL,
    debt DECIMAL(10, 2) NOT NULL
)

-- Constraints:
ALTER TABLE payed_loan ADD CONSTRAINT payed_loan_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
ALTER TABLE payed_loan ADD CONSTRAINT payed_loan_casa_id_exists FOREIGN KEY (casa_id) REFERENCES casa (id) 
