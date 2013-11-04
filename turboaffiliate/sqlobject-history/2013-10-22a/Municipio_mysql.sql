-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Municipio
-- Database: mysql
CREATE TABLE municipio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    departamento_id INT,
    nombre VARCHAR(50)
)

-- Constraints:
ALTER TABLE municipio ADD CONSTRAINT municipio_departamento_id_exists FOREIGN KEY (departamento_id) REFERENCES departamento (id) 
