    SELECT City, Street FROM schools Order BY City DESC LIMIT 11

<!--  -->
    SELECT City, Street FROM schools Order BY City ASC LIMIT 11

<!--  -->
    SELECT Street as T, City FROM schools Order BY City DESC LIMIT 10

<!--  -->
    SELECT * FROM ( SELECT City, Street FROM schools ORDER BY City DESC LIMIT 11 ) subquery ORDER BY City ASC

 <!-- gold -->
    SELECT City, Street, school FROM frpm INNER JOIN schools ON frpm.cdscode = schools.cdscode WHERE `county` = "Los Angeles" AND `gsserved` = "K-12" AND `free meal count (k-12)` > 400 AND `free meal count (k-12)` < 800;

<!-- gen -->
    SELECT school, City, Street FROM frpm INNER JOIN schools ON frpm.cdscode = schools.cdscode WHERE `county` = "Los Angeles" AND `gsserved` = "K-12" AND `free meal count (k-12)` > 500 AND `free meal count (k-12)` < 700;
