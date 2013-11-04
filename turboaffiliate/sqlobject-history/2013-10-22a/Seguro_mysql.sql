-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Seguro
-- Database: mysql
CREATE TABLE seguro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    indemnizacion_id INT,
    fecha DATE,
    fallecimiento DATE
)

-- Constraints:
ALTER TABLE seguro ADD CONSTRAINT seguro_indemnizacion_id_exists FOREIGN KEY (indemnizacion_id) REFERENCES indemnizacion (id) 
