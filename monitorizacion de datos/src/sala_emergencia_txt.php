<html>

<?php 
	$line='10';
	echo "Correo enviado !! ";
	echo "</br>";
	$query="sudo python /home/pi/Proyecto_ssddaa_2php.py .$line";
	exec($query);
?>

<a href="/sala_emergencia.html">Volver </a>
</html>
