## DATA CLEANING: procesamiento y preparación de los datos 

El  proceso  de  limpieza  y  preparación  tuvo  como  objetivo  dejar  el  dataset  en  un 
formato  coherente,  homogéneo  y  listo  para  la  fase  de  análisis  y  búsqueda  de 
indicadores. A continuación se describen los pasos realizados, siguiendo un orden 
lógico desde la carga inicial hasta la generación del archivo procesado final. 

### 1.  Carga y exploración inicial 

En primer lugar, importamos el conjunto de datos original y realizamos una revisión 
general  de  su  estructura  para  comprobar  la  correcta  lectura  de  las  columnas  y 
detectar  posibles  irregularidades.  Verificamos  el  número de registros, los tipos de 
datos  y  visualizamos  algunos  ejemplos  para  confirmar  que  el  contenido  textual 
estuviera correctamente identificado. 

### 2.  Estandarización de variables 

Para mantener coherencia con las convenciones de análisis de datos, tradujimos los 
nombres  de  las  columnas  del  español  al  inglés.  De  esta  forma,  las  variables 
temporales (año, mes, día) y la variable de texto principal quedaron unificadas bajo 
nombres más estándar. Además, homogeneizamos el idioma del contenido textual, 
sustituyendo etiquetas o palabras que aparecían en español por su equivalente en 
inglés. 

### 3.  Unificación de la dimensión temporal 

A  partir  de  las  tres  variables  temporales  (año,  mes  y  día)  creamos  una  única 
columna con formato de fecha completa. Esta transformación nos permitió trabajar 
con un solo campo temporal y facilitó la agrupación posterior por días, semanas o 
meses.  Una  vez  generada  la  nueva  variable,  las  columnas  originales  fueron 
eliminadas para evitar redundancias. 

### 4.  Limpieza del texto 

Eliminamos todos los enlaces y direcciones web, tanto los que aparecían en formato 
incrustado como los que figuraban de forma directa dentro del texto. Esta operación 
redujo el ruido y garantizó que el análisis de sentimiento y el modelado de tópicos se 
centraran únicamente en el contenido semántico relevante. 
También  eliminamos  caracteres  especiales  y  aplicamos  una  limpieza  general  del 
texto, dejando únicamente información útil y legible. 

### 5.  Separación entre publicaciones y comentarios 

El  texto  original  contenía  tanto  el  mensaje  principal  del  post  como  el  comentario 
asociado  dentro  de  una  misma  celda.  Para  mejorar  la  estructura,  dividimos  esta 
información en dos columnas independientes: una para el contenido del post y otra 
para el comentario. Esta separación permitió un análisis más granular y diferenciado 
entre el discurso inicial y las respuestas generadas por los usuarios. 
Posteriormente,  comprobamos  la  existencia  de  comentarios  vacíos  o  nulos  para 
identificar posibles registros sin contenido relevante. 

### 6.  Organización cronológica y estructuración final 

Calculamos la fecha más antigua asociada a cada publicación con el fin de ordenar 
las conversaciones de forma cronológica. A cada post se le asignó un identificador 
numérico  único  que  refleja  su  posición  temporal.  Posteriormente,  el  conjunto  de 
datos se ordenó de manera jerárquica: primero por el identificador del post y, dentro 
de cada grupo, por la fecha de cada comentario. 
Creamos  además  un  índice  consecutivo  global  para  garantizar la unicidad de los 
registros  y  facilitar  su  trazabilidad.  Finalmente,  reorganizamos  las  columnas  para 
obtener un formato lógico y legible. 

### 7.  Exportación del dataset procesado 

Tras  completar  las  transformaciones,  el  dataset  resultante  fue  guardamos  con  el 
nombre  charlie_kirk_comments_cleaned.csv  dentro  del  directorio  de  datos 
procesados.  El  archivo  final  presenta  un  formato  limpio,  estructurado  y  libre  de 
duplicados, con las variables necesarias para los análisis de sentimiento, de tópicos 
y de evolución temporal que se desarrollarán en las siguientes fases del proyecto.