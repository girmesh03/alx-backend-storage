-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

-- Requirements:
	-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE done INT DEFAULT FALSE;
    DECLARE current_user_id INT;

    -- Declare variables to store the total score and total weight for each user
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_weighted_score FLOAT;

    -- Declare continue handler for cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through users and calculate average weighted score
    user_loop: LOOP
        FETCH user_cursor INTO current_user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Calculate the total weighted score and total weight for the current user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = current_user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_score / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;

        -- Update the user's average_score in the users table
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = current_user_id;
    END LOOP user_loop;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;

