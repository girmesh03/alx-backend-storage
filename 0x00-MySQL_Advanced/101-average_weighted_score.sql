-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

-- Requirements:
	-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_var INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_weighted_score FLOAT;

    -- Cursor to iterate over users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Loop through each user
    OPEN user_cursor;
    user_loop: LOOP
        FETCH user_cursor INTO user_id_var;
        IF user_id_var IS NULL THEN
            LEAVE user_loop;
        END IF;

        -- Calculate the total weighted score and total weight for the user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id_var;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_score / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;

        -- Update the user's average_score in the users table
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id_var;
    END LOOP;
    CLOSE user_cursor;

END$$

DELIMITER ;
