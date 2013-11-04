-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.PagoBancarioBanhcafe
-- Database: mysql
CREATE TABLE pago_bancario_banhcafe (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identidad VARCHAR(13),
    cantidad DECIMAL(10, 2),
    fecha DATETIME,
    referencia INT,
    agencia INT,
    cajero VARCHAR(10),
    terminal VARCHAR(1),
    aplicado BOOL
)
