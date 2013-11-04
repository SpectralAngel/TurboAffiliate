-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Inscripcion
-- Database: mysql
CREATE TABLE inscripcion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    afiliado_id INT,
    asamblea_id INT,
    viatico_id INT,
    enviado BOOL,
    envio DATE,
    ingresado DATETIME
)

-- Constraints:
ALTER TABLE inscripcion ADD CONSTRAINT inscripcion_afiliado_id_exists FOREIGN KEY (afiliado_id) REFERENCES affiliate (id) 
ALTER TABLE inscripcion ADD CONSTRAINT inscripcion_asamblea_id_exists FOREIGN KEY (asamblea_id) REFERENCES asamblea (id) 
ALTER TABLE inscripcion ADD CONSTRAINT inscripcion_viatico_id_exists FOREIGN KEY (viatico_id) REFERENCES viatico (id) 
