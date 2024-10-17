-- This script contains a stored procedure that
-- computes and stores the weighted average score
-- for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INTEGER)
BEGIN
    DECLARE average FLOAT;
    DECLARE total_weight INTEGER;
    SELECT SUM(
        (SELECT projects.weight FROM projects
        WHERE id = corrections.project_id)
    ) INTO total_weight FROM corrections
    WHERE corrections.user_id = user_id;

    SELECT SUM(((
        SELECT projects.weight FROM projects 
        WHERE id = corrections.project_id
    ) / total_weight) * score)
    INTO average FROM corrections
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET average_score = average
    WHERE id = user_id;
END //
DELIMITER ;
