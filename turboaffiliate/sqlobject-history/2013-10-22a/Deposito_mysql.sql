-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Deposito
-- Database: mysql
CREATE TABLE deposito (
    id INT PRIMARY KEY AUTO_INCREMENT,
    afiliado_id INT,
    banco_id INT,
    concepto VARCHAR(50),
    fecha DATE,
    posteo DATE,
    monto DECIMAL(10, 2),
    descripcion VARCHAR(100)
)

-- Constraints:
ALTER TABLE deposito ADD CONSTRAINT deposito_afiliado_id_exists FOREIGN KEY (afiliado_id) REFERENCES affiliate (id) 
ALTER TABLE deposito ADD CONSTRAINT deposito_banco_id_exists FOREIGN KEY (banco_id) REFERENCES banco (id) 
