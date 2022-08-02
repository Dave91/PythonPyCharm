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
<a href="probagb.htm">Vissza a kapcsolati oldalra!</a><br>
<hr><br>
<?php
$gbtexto = fopen("vendegkonyv.txt", "r") or die("Hiba: a fájl nem elérhető!");
echo "<pre>" . fread($gbtexto,filesize("vendegkonyv.txt")) . "</pre>";
fclose($gbtexto);
?>
</body>
</html>