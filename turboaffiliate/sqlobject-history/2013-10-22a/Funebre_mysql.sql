-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Funebre
-- Database: mysql
CREATE TABLE ayuda_funebre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    afiliado_id INT,
    fecha DATE,
    monto DECIMAL(10, 2),
    cheque VARCHAR(20),
    pariente VARCHAR(100),
    banco VARCHAR(50)
)

-- Constraints:
ALTER TABLE ayuda_funebre ADD CONSTRAINT ayuda_funebre_afiliado_id_exists FOREIGN KEY (afiliado_id) REFERENCES affiliate (id) 
