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
<a href="guestbook.php">Tovább az üzenőfalhoz!</a>
<hr><br>
<img src="images/Ok-icon.png">
<br>

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
$neve=$_POST['neve'];
$email=$_POST['email'];
$ideje=date("Y-m-d H:i:s");
$komment=$_POST['komment'];
$sql="INSERT INTO guestbook(neve,email,ideje,komment) VALUES('$neve','$email','$ideje','$komment')";
if (!mysqli_query($con,$sql))
{
die('Hiba: ' . mysqli_error($con));
}
else
echo "Üzenet sikeresen elküldve!";
mysqli_close($con);
?>

</body>
</html>