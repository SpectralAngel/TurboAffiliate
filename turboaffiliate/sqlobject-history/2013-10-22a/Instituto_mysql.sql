-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Instituto
-- Database: mysql
CREATE TABLE instituto (
    id INT PRIMARY KEY AUTO_INCREMENT,
    municipio_id INT,
    nombre VARCHAR(50)
)

-- Constraints:
ALTER TABLE instituto ADD CONSTRAINT instituto_municipio_id_exists FOREIGN KEY (municipio_id) REFERENCES municipio (id) 
