CREATE TABLE teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_org_team (organization_id, name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
CREATE TABLE user_team (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    user_id INT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
    SET NULL,
        FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
        UNIQUE KEY unique_team_user (team_id, user_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;