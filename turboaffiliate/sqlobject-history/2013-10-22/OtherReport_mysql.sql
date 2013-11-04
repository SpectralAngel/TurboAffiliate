-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.OtherReport
-- Database: mysql
CREATE TABLE other_report (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    month INT,
    cotizacion_id INT
)

-- Constraints:
ALTER TABLE other_report ADD CONSTRAINT other_report_cotizacion_id_exists FOREIGN KEY (cotizacion_id) REFERENCES cotizacion (id) 
