-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.DeduccionBancaria
-- Database: mysql
CREATE TABLE deduccion_bancaria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    afiliado_id INT,
    banco_id INT,
    account_id INT,
    amount DECIMAL(10, 2),
    detail TEXT,
    day DATE,
    month INT,
    year INT
)

-- Constraints:
ALTER TABLE deduccion_bancaria ADD CONSTRAINT deduccion_bancaria_afiliado_id_exists FOREIGN KEY (afiliado_id) REFERENCES affiliate (id) 
ALTER TABLE deduccion_bancaria ADD CONSTRAINT deduccion_bancaria_banco_id_exists FOREIGN KEY (banco_id) REFERENCES banco (id) 
ALTER TABLE deduccion_bancaria ADD CONSTRAINT deduccion_bancaria_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
