<?php
    exec('sudo cp /home/pi/proyecto/reporte.txt /var/www/html');
    $fp = fopen ("reporte.txt", "r");
    while(!feof($fp)){
            $linea= fgets($fp);
            echo $linea."<br />";
    }
    fclose($fp);
?>
