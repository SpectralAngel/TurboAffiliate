-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.Affiliate
-- Database: mysql
CREATE TABLE affiliate (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    card_id VARCHAR(15),
    gender CHAR(1),
    birthday DATE,
    birth_place VARCHAR(100),
    address TEXT,
    phone TEXT,
    departamento_id INT,
    municipio_id INT,
    instituto_id INT,
    state VARCHAR(50),
    school VARCHAR(255),
    town VARCHAR(50),
    joined DATE,
    active BOOL NOT NULL,
    reason VARCHAR(50),
    escalafon VARCHAR(11),
    inprema VARCHAR(11),
    jubilated DATE,
    payment VARCHAR(20),
    cotizacion_id INT,
    muerte DATE,
    desactivacion DATE,
    cuenta TEXT,
    banco INT,
    email TEXT,
    autorizacion BOOL NOT NULL
)

-- Constraints:
ALTER TABLE affiliate ADD CONSTRAINT affiliate_departamento_id_exists FOREIGN KEY (departamento_id) REFERENCES departamento (id) 
ALTER TABLE affiliate ADD CONSTRAINT affiliate_municipio_id_exists FOREIGN KEY (municipio_id) REFERENCES municipio (id)
ALTER TABLE affiliate ADD CONSTRAINT affiliate_cotizacion_id_exists FOREIGN KEY (cotizacion_id) REFERENCES cotizacion (id) 
