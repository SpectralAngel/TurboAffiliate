-- Exported definition from 2013-10-22T10:03:57
-- Class turboaffiliate.model.ReportAccount
-- Database: mysql
CREATE TABLE report_account (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    quantity INT,
    amount DECIMAL(10, 2),
    post_report_id INT
)

-- Constraints:
ALTER TABLE report_account ADD CONSTRAINT report_account_post_report_id_exists FOREIGN KEY (post_report_id) REFERENCES post_report (id) 
