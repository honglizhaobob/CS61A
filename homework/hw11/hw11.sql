CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;

-------------------------------------------------------------
-- PLEASE DO NOT CHANGE ANY SQL STATEMENTS ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name,size FROM dogs, sizes WHERE dogs.height > sizes.min AND dogs.height <= sizes.max;

-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT parents.child from parents, dogs where dogs.name=parents.parent order by height desc;

-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child as sib1, b.child as sib2 from parents as a, parents as b where a.parent = b.parent AND a.child < b.child;
-- sib1 |||| sib2
-- abraham|delano
-- abraham|grover
-- barack|clinton
-- delano|grover

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT a.name || ' and ' || b.name || ' are ' || a.size || ' siblings' from size_of_dogs as a, size_of_dogs as b, siblings where a.name < b.name and a.size=b.size and a.name = siblings.sib1 and b.name = siblings.sib2 ORDER BY a.name desc;
  -- SELECT name || " and " || name from dogs
  -- abraham and abraham ...

-- Ways to stack 4 dogs to a height of at least 170, ordered by total height
CREATE TABLE stacks_helper(dogs, stack_height, last_height);

-- Add your INSERT INTOs here
insert into stacks_helper select name,height,height from dogs;
-- for testing:
-- select * from stacks_helper;

-- two stacks
insert into stacks_helper
  SELECT
  a.dogs || ", " || b.name,
  a.stack_height + b.height, -- increase total
  b.height
  from stacks_helper as a, dogs as b
      WHERE a.dogs != b.name -- each dog only once
      AND a.last_height < b.height
      -- increasing height within stack
      ;

-- three stacks
insert into stacks_helper
  SELECT
  a.dogs || ", " || b.name,
  a.stack_height + b.height, -- increase total
  b.height
  from stacks_helper as a, dogs as b
      WHERE a.dogs != b.name -- each dog only once
      AND a.last_height < b.height
      -- increasing height within stack
      ;

-- four stacks
insert into stacks_helper
  SELECT
  a.dogs || ", " || b.name,
  a.stack_height + b.height, -- increase total
  b.height
  from stacks_helper as a, dogs as b
      WHERE a.dogs != b.name -- each dog only once
      AND a.last_height < b.height
      -- increasing height within stack
      ;

CREATE TABLE stacks AS
  SELECT dogs, stack_height FROM stacks_helper
  WHERE stack_height >= 170
  ORDER BY stack_height;


