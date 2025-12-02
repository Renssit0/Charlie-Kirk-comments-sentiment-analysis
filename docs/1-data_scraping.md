## DATA SCRAPPING: recolección, filtrado y balanceo

El script automatiza la recolección de comentarios en Reddit, aplicando filtros de calidad y asegurando un equilibrio mensual en los datos obtenidos. A continuación se resume el funcionamiento principal.

### 1. Limpieza y validación del texto

Se normaliza el contenido eliminando espacios extra y se descartan comentarios de baja calidad: textos muy cortos, eliminados, con spam, exceso de enlaces o patrones no informativos.

### 2. Construcción del contexto del post

Para cada publicación se genera un contexto combinando título y contenido del post, siempre que este tenga suficiente información. Esta referencia se añade a cada comentario aceptado.

### 3. Selección de comentarios relevantes

Los comentarios se filtran según:

- validez del texto,

- puntuación (upvotes − downvotes),

- ausencia de spam.

Solo se conservan los mejor valorados por post.

### 4. Extracción y estructuración de entradas

Cada comentario válido se convierte en una entrada con:

- contexto del post,

- texto del comentario,

- fecha (año, mes, día),

- score y subreddit.

Se controla un ID incremental.

### 5. Balance mensual de datos

El proceso mantiene un contador por mes y solo permite nuevas entradas si el mes no supera su límite máximo. También verifica que cada mes alcance un mínimo requerido para asegurar una distribución equilibrada.

### 6. Búsqueda en subreddits específicos y generales

Primero se buscan posts en subreddits políticos seleccionados; si no se alcanza el objetivo total, se amplía la búsqueda a all usando múltiples queries relacionadas con el tema.

### 7. Control del flujo y reportes

Durante la búsqueda se evalúa continuamente si continuar o detenerse según:

- total de entradas recolectadas,

- cumplimiento del mínimo mensual,

- disponibilidad de espacio en meses incompletos.

Se muestran reportes del progreso y del balance por mes.

### 8. Generación del dataset final

Los datos se consolidan en un DataFrame, se eliminan duplicados, se ordenan por fecha y se exportan a CSV. Al final se muestra un resumen de distribución mensual, subreddits incluidos y estadísticas básicas del score.