<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<style>
html {
  background: url("images/vintage-933793_1920.jpg") no-repeat center center fixed;
  background-size: cover;
}
body {text-align:center;}
</style>
</head>
<body>
<br>
<a href="rolam.htm">Vissza a kapcsolati oldalra!</a><br>
<hr><br>

<?php
$host="mysql.omega:3306";
$user="lewas1991";
$pass="lewas1991";
$dbname="lewas1991";
$con=mysqli_connect($host,$user,$pass,$dbname);
if (mysqli_connect_error($con))
{
echo "Hiba! Adatbázis nem elérhető: " . mysqli_connect_error();
}
$result = mysqli_query($con,"SELECT ideje,komment FROM guestbook");
while($row = mysqli_fetch_array($result))
{ ?>
<b> <?php echo $row['ideje']; ?> </b><br>
<?php echo $row['komment']; ?> <br><br>
<hr><br><br>
<?php
mysqli_close($con);
} ?>

</body>
</html>