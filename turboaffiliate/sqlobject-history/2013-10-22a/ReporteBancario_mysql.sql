-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.ReporteBancario
-- Database: mysql
CREATE TABLE reporte_bancario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    banco_id INT,
    day DATE,
    month INT,
    year INT
)

-- Constraints:
ALTER TABLE reporte_bancario ADD CONSTRAINT reporte_bancario_banco_id_exists FOREIGN KEY (banco_id) REFERENCES banco (id) 
