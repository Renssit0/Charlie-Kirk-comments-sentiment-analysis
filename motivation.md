# MOTIVATION: contenido y propósito del conjunto de datos

## 1. Propósito del conjunto de datos
El conjunto de datos final tiene como objetivo analizar la evolución del discurso digital en torno a la figura del comentarista político **Charlie Kirk**, a partir de publicaciones y comentarios extraídos de distintos subreddits entre **noviembre de 2024 y octubre de 2025**.

El eje del análisis se centra en la hipótesis de trabajo:

> *“La animadversión hacia Charlie Kirk disminuye tras su muerte en septiembre.”*

A partir de esta premisa, se construyó una base de datos estructurada por intervalos mensuales que permite observar cómo cambian el tono, los temas y la riqueza del lenguaje en los debates de la comunidad antes y después de ese evento.

---

## 2. Contenido del dataset
Cada fila del dataset representa un mes del período analizado y recoge el valor medio de los principales indicadores derivados del procesamiento textual.  
El resultado final contiene **14 filas (un mes por intervalo)** y las siguientes variables:

| Variable | Descripción | Tipo |
|-----------|--------------|------|
| **year_month** | Mes y año de referencia (intervalo temporal) | Categórica temporal |
| **count_month** | Volumen promedio de publicaciones y comentarios registrados en el mes | Numérica |
| **sentiment_score** | Intensidad media de la polaridad emocional (0–1) | Numérica |
| **sentiment_num** | Polaridad media codificada (0 = negativo, 1 = neutro, 2 = positivo) | Numérica |
| **mean_sentiment_month** | Promedio mensual del sentimiento agregado | Numérica |
| **lexical_entropy_month** | Entropía léxica mensual, indicador de diversidad y riqueza de vocabulario | Numérica |
| **topic_id** | Identificador del tópico predominante en el mes según el modelo LDA | Categórica numérica |

---

## 3. Indicadores y significado

- **Volumen temporal de publicaciones (count_month):** mide la actividad de los usuarios y permite detectar picos de conversación o momentos de especial interés.  

- **Sentimiento medio (sentiment_score, sentiment_num, mean_sentiment_month):** refleja la tendencia emocional del discurso, permitiendo evaluar si las opiniones negativas o positivas se intensifican o se moderan a lo largo del tiempo.  

- **Distribución de tópicos (topic_id):** sintetiza los temas dominantes en cada mes, identificando la proporción de conversaciones centradas en humor, política o referencias directas a Kirk.  

- **Diversidad léxica (lexical_entropy_month):** cuantifica la variedad del lenguaje empleado, indicador indirecto del nivel de argumentación y riqueza del debate.  

---

## 4. Hipótesis y objetivo analítico
El análisis temporal de estos indicadores busca comprobar si, tras el fallecimiento de Charlie Kirk en **septiembre de 2025**, se produce un cambio significativo en el tono emocional de las conversaciones online.  
En concreto, se pretende verificar si el sentimiento medio hacia su figura muestra una disminución de la animadversión y un aumento de los mensajes neutros o conciliadores en los meses posteriores.

El dataset resultante proporciona una representación cuantitativa del discurso digital antes y después del evento, facilitando el estudio de cómo las comunidades virtuales reconfiguran su lenguaje y su tono cuando desaparece la persona que genera el conflicto discursivo.

---

## 5. Conclusión
El conjunto de datos mensual obtenido integra de forma coherente los indicadores de **actividad, sentimiento, temas y diversidad lingüística**, permitiendo un análisis comparativo claro y medible a lo largo del tiempo.  
Este enfoque temporal y multivariable constituye la base para contrastar la hipótesis planteada y observar de manera empírica la evolución del sentimiento hacia Charlie Kirk tras su muerte.
