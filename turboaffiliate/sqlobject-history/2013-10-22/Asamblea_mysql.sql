-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Asamblea
-- Database: mysql
CREATE TABLE asamblea (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero INT,
    nombre VARCHAR(100),
    departamento_id INT,
    habilitado BOOL,
    fecha DATE
)

-- Constraints:
ALTER TABLE asamblea ADD CONSTRAINT asamblea_departamento_id_exists FOREIGN KEY (departamento_id) REFERENCES departamento (id) 
