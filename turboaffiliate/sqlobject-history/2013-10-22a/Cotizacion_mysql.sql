-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Cotizacion
-- Database: mysql
CREATE TABLE cotizacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    jubilados BOOL
);
CREATE TABLE cotizacion_tg_user (
cotizacion_id INT NOT NULL,
tg_user_id INT NOT NULL
)
