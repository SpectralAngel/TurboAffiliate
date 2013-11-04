-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.DepositoAnonimo
-- Database: mysql
CREATE TABLE deposito_anonimo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    referencia VARCHAR(100),
    banco_id INT,
    concepto VARCHAR(50),
    fecha DATE,
    monto DECIMAL(10, 2)
)

-- Constraints:
ALTER TABLE deposito_anonimo ADD CONSTRAINT deposito_anonimo_banco_id_exists FOREIGN KEY (banco_id) REFERENCES banco (id) 
