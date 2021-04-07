<?php
$directorio = "C:\Users\pc1\Desktop\Codes\Ozone\prueba1\converted_files";
#carpeta con archivos
$contador = 0;

$archivos = glob("$directorio/*");
introducir el código aquí

foreach ($archivos as $archivo) {   
     echo "nombre: <strong> $archivo </strong></br>" ;
                            }
?>