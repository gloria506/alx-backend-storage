-- a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.

DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER //
CREATE PROCEDURE AddBonus(user_id INTEGER, project_name VARCHAR(255), score INTEGER)
BEGIN
    DECLARE project_id INTEGER;
    SELECT id INTO project_id FROM projects WHERE projects.name = project_name;
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SELECT id INTO project_id FROM projects WHERE name = project_name;
    END IF;
    INSERT INTO corrections VALUES (user_id, project_id, score);
END //
DELIMITER ;
