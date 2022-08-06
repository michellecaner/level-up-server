SELECT 
    user.first_name || " " || user.last_name as full_name,
    user.id as user_id,
    game.*
FROM levelupapi_game as game
JOIN auth_user as user
ON user.id = game.gamer_id