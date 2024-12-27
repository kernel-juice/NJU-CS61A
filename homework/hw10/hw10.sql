.read hw10_data.sql

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, size FROM dogs, sizes WHERE height > min AND height <= max;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT for_child.name FROM parents, dogs AS for_parents, dogs AS for_child WHERE for_child.name = child AND parent = for_parents.name ORDER BY for_parents.height DESC;


CREATE TABLE sibl AS
  SELECT a.name AS "first", a.height AS "fir_height", b.name AS "second", b.height AS "sec_height" FROM dogs AS a, dogs AS b, parents AS par_for_a, parents AS par_for_b WHERE a.name = par_for_a.child AND b.name = par_for_b.child AND par_for_a.parent = par_for_b.parent AND a.name < b.name;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT 'The two siblings, ' || first || ' plus ' || second || ' have the same size: ' || a.size FROM sibl, sizes AS a, sizes AS b WHERE fir_height > a.min AND fir_height <= a.max AND sec_height > b.min AND sec_height <= b.max AND a.size = b.size;
