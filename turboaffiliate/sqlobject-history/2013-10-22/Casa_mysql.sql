-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Casa
-- Database: mysql
CREATE TABLE casa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20),
    direccion VARCHAR(255),
    telefono VARCHAR(11),
    activa BOOL
)
