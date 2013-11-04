-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Viatico
-- Database: mysql
CREATE TABLE viatico (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asamblea_id INT,
    municipio_id INT,
    monto DECIMAL(10, 2),
    transporte DECIMAL(10, 2),
    previo DECIMAL(10, 2),
    posterior DECIMAL(10, 2)
)

-- Constraints:
ALTER TABLE viatico ADD CONSTRAINT viatico_asamblea_id_exists FOREIGN KEY (asamblea_id) REFERENCES asamblea (id) 
ALTER TABLE viatico ADD CONSTRAINT viatico_municipio_id_exists FOREIGN KEY (municipio_id) REFERENCES municipio (id) 
