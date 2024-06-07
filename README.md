# Postulación a Abaqus

Para correr el servidor deben correr el comando: `python3 manager.py runserver`.

Para probar el endpoint tipo API rest del punto 5 del enunciado, el servidor debe estar corriendo y realizar por ejemplo, un GET mediante postman al link `http://localhost:8000/valores/?fecha_inicio=2022-02-15&fecha_fin=2022-02-16`. Se pueden reemplazar las fechas de `fecha_inicio` y `fecha_fin` para recibir los datos según lo que quieran buscar.

La función que carga los datos del Excel al modelo esta ubicada en ```portafolios/management/commands/load_data.py```
