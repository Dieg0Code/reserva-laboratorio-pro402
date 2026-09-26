# Requisitos del sistema de reserva de laboratorio

| ID | Requisito |
|---|---|
| RF-01 | La jornada tiene ocho bloques, numerados del 1 al 8. Una solicitud para un bloque fuera de ese rango se rechaza. |
| RF-02 | Un bloque que ya tiene una reserva no puede volver a reservarse. |
| RF-03 | Un estudiante puede tener como maximo 3 reservas activas por semana. |
| RF-04 | La sala admite entre 1 y 30 personas. Una solicitud fuera de ese rango se rechaza. |
| RF-05 | Una reserva puede cancelarse hasta 2 horas antes del inicio de su bloque. |
| RF-06 | Una reserva aceptada devuelve un comprobante con el nombre, el RUT, el correo y el bloque. |
| RF-07 | Ejecutada una solicitud de supresion, ninguna tabla del sistema conserva datos que identifiquen al titular. |
| RF-08 | El titular puede obtener todos los datos personales que el sistema trata sobre el. |
| RF-09 | Los datos que se entregan al titular van en un formato electronico estructurado, generico y de uso comun. |
| RF-10 | Mientras una solicitud de supresion no se resuelva, el sistema no trata los datos del titular. |
