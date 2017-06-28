<html>
	<?php
		$fp = fopen("/home/pi/medidas_sala_emergencia.txt", "r");
		while(!feof($fp)){
			$linea = fgets($fp);
			echo $linea . "<br />";
		}
		fclose($fp);
	?>

<a href="/sala_emergencia.html">Volver</a> 
</html> 
