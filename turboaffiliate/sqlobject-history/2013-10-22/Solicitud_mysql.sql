-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Solicitud
-- Database: mysql
CREATE TABLE solicitud (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    ingreso DATE,
    entrega DATE,
    monto DECIMAL(10, 2) NOT NULL,
    periodo INT
)

-- Constraints:
ALTER TABLE solicitud ADD CONSTRAINT solicitud_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
