-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Banco
-- Database: mysql
CREATE TABLE banco (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    depositable BOOL,
    asambleista BOOL,
    parser VARCHAR(100),
    generator VARCHAR(100),
    cuenta VARCHAR(100),
    codigo VARCHAR(100)
)
