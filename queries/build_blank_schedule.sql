INSERT INTO schedule (`season`, `week`, `subdivision`, `team`)
SELECT 9 AS `season`, `week`, `subdivision`, `team`
FROM `schedule` where `season` = 8;