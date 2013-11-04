-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Reintegro
-- Database: mysql
CREATE TABLE reintegro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    affiliate_id INT,
    emision DATE,
    monto DECIMAL(10, 2),
    cheque VARCHAR(10),
    planilla VARCHAR(10),
    motivo VARCHAR(100),
    forma_pago_id INT,
    pagado BOOL,
    cancelacion DATE,
    cuenta_id INT
)

-- Constraints:
ALTER TABLE reintegro ADD CONSTRAINT reintegro_affiliate_id_exists FOREIGN KEY (affiliate_id) REFERENCES affiliate (id) 
ALTER TABLE reintegro ADD CONSTRAINT reintegro_forma_pago_id_exists FOREIGN KEY (forma_pago_id) REFERENCES forma_pago (id) 
ALTER TABLE reintegro ADD CONSTRAINT reintegro_cuenta_id_exists FOREIGN KEY (cuenta_id) REFERENCES account (id) 
