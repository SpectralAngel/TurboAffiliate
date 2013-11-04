-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.CuentaRetrasada
-- Database: mysql
CREATE TABLE cuenta_retrasada (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    mes INT,
    anio INT
)

-- Constraints:
ALTER TABLE cuenta_retrasada ADD CONSTRAINT cuenta_retrasada_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
