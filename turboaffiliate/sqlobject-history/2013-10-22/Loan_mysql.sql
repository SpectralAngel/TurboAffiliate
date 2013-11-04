-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Loan
-- Database: mysql
CREATE TABLE loan (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    casa_id INT,
    capital DECIMAL(10, 2) NOT NULL,
    letters VARCHAR(100),
    debt DECIMAL(10, 2) NOT NULL,
    payment DECIMAL(10, 2) NOT NULL,
    interest DECIMAL(4, 2) NOT NULL,
    months INT,
    last DATE,
    number INT,
    offset INT,
    start_date DATE NOT NULL,
    aproved BOOL,
    fecha_mora DATE NOT NULL,
    aproval_id INT,
    cobrar BOOL
)

-- Constraints:
ALTER TABLE loan ADD CONSTRAINT loan_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
ALTER TABLE loan ADD CONSTRAINT loan_casa_id_exists FOREIGN KEY (casa_id) REFERENCES casa (id) 
ALTER TABLE loan ADD CONSTRAINT loan_aproval_id_exists FOREIGN KEY (aproval_id) REFERENCES tg_user (id) 
