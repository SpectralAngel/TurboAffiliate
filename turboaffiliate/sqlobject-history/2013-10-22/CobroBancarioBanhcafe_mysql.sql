-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.CobroBancarioBanhcafe
-- Database: mysql
CREATE TABLE cobro_bancario_banhcafe (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identidad VARCHAR(13),
    cantidad DECIMAL(10, 2),
    consumido BOOL
)
