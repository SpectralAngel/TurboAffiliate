-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Devolucion
-- Database: mysql
CREATE TABLE devolucion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    afiliado_id INT,
    concepto VARCHAR(200),
    fecha DATE,
    monto DECIMAL(10, 2),
    cheque VARCHAR(20),
    banco VARCHAR(50)
)

-- Constraints:
ALTER TABLE devolucion ADD CONSTRAINT devolucion_afiliado_id_exists FOREIGN KEY (afiliado_id) REFERENCES affiliate (id) 
