<?php
$archivo='/home/pi/trabajo/fig1.png';
header("Content-type: image/png");
header("Content-length: ".filesize($archivo));
header("Content-Disposition: inline; filename=$archivo");
readfile($archivo);
// Fin crear imagen
// ?>
