.read lab11_data.sql


CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = 'blue' AND pet = 'dog';

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = 'blue' AND pet = 'dog';

CREATE TABLE smallest_int_having AS
  SELECT time, smallest FROM students GROUP BY smallest HAVING COUNT(*) = 1;


CREATE TABLE matchmaker AS
  SELECT a.pet, b.song, a.color, b.color FROM students AS a, students AS b WHERE a.pet = b.pet AND a.song = b.song AND a.time < b.time;


CREATE TABLE sevens AS
  SELECT a.seven FROM students AS a, numbers AS b WHERE a.time = b.time AND a.number = 7 AND b."7" = "True";


CREATE TABLE avg_difference AS
  SELECT ROUND(AVG(ABS(number - smallest))) FROM students;

-- CREATE TABLE students AS
--    SELECT "11/17/2021 10:52:40" AS time, 3 AS number, "black" AS color, "the number 7 below." AS seven, "Smells Like Teen Spirit" as song, "10/31" as date, "dog" as pet, "2" AS instructor, 1 AS smallest UNION

-- CREATE TABLE numbers AS
--    SELECT "11/17/2021 10:52:40" AS time, "True" AS "0", "True" AS "1", "True" AS "2", "True" AS "3", "True" AS "4", "True" AS "5", "True" AS "6", "True" AS "7", "True" AS "8", "True" AS "9", "False" AS "10", "True" AS "2021", "True" AS "2022", "True" AS "9000", "False" AS "9001" UNION