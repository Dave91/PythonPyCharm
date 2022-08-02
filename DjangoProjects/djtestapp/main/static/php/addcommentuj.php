<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<style>
html {
  background: url("vintage-933793_1920.jpg") no-repeat center center fixed;
  background-size: cover;
}
body {text-align:center;}
</style>
</head>
<body>
<br>
<a href="guestbookuj.php">Tovább az üzenőfalhoz!</a>
<hr><br>
<?php
$gbtexti = fopen("vendegkonyv.txt", "a") or die("Hiba: a fájl nem elérhető!");
$neve = $_POST['neve'];
$email = $_POST['email'];
$ideje = date("Y-m-d H:i:s") . PHP_EOL;
$komment = $_POST['komment'] . PHP_EOL;
$newstring = PHP_EOL . $neve . " (" . $email . ")" . PHP_EOL;
fwrite($gbtexti, $newstring);
fwrite($gbtexti, $ideje);
fwrite($gbtexti, $komment);
$newstring = PHP_EOL . "=============================" . PHP_EOL;
fwrite($gbtexti, $newstring);
fclose($gbtexti);
echo "Üzenet sikeresen elküldve!";
?>
<br>
<img src="Ok-icon.png">
</body>
</html>