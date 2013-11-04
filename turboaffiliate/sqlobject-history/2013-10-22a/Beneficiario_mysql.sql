-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Beneficiario
-- Database: mysql
CREATE TABLE beneficiario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    seguro_id INT,
    nombre VARCHAR(50),
    monto DECIMAL(10, 2),
    cheque VARCHAR(20),
    banco VARCHAR(50),
    fecha DATE
)

-- Constraints:
ALTER TABLE beneficiario ADD CONSTRAINT beneficiario_seguro_id_exists FOREIGN KEY (seguro_id) REFERENCES seguro (id) 
