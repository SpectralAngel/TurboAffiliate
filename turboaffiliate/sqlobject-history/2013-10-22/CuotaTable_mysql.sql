-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.CuotaTable
-- Database: mysql
CREATE TABLE cuota_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    year INT,
    month1 BOOL,
    month2 BOOL,
    month3 BOOL,
    month4 BOOL,
    month5 BOOL,
    month6 BOOL,
    month7 BOOL,
    month8 BOOL,
    month9 BOOL,
    month10 BOOL,
    month11 BOOL,
    month12 BOOL
);
ALTER TABLE cuota_table ADD UNIQUE affiliateYear (affiliate_id, year)

-- Constraints:
ALTER TABLE cuota_table ADD CONSTRAINT cuota_table_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
