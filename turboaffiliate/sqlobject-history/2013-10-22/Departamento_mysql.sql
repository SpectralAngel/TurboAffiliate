-- Exported definition from 2013-10-22T10:01:43
-- Class turboaffiliate.model.Departamento
-- Database: mysql
CREATE TABLE departamento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50)
);
CREATE TABLE departamento_tg_user (
departamento_id INT NOT NULL,
tg_user_id INT NOT NULL
)
