-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Observacion
-- Database: mysql
CREATE TABLE observacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    texto TEXT,
    fecha DATE
)

-- Constraints:
ALTER TABLE observacion ADD CONSTRAINT observacion_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
