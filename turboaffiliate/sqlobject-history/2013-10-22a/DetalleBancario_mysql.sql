-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.DetalleBancario
-- Database: mysql
CREATE TABLE detalle_bancario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reporte_id INT,
    account_id INT,
    amount DECIMAL(10, 2)
)

-- Constraints:
ALTER TABLE detalle_bancario ADD CONSTRAINT detalle_bancario_reporte_id_exists FOREIGN KEY (reporte_id) REFERENCES reporte_bancario (id) 
ALTER TABLE detalle_bancario ADD CONSTRAINT detalle_bancario_account_id_exists FOREIGN KEY (account_id) REFERENCES account (id) 
