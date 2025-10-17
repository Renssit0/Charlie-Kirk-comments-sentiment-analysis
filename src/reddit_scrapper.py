import pandas as pd
import re
from datetime import datetime, timedelta
import time
from collections import defaultdict

def limpiar_texto(texto):
    """Limpia el texto de caracteres especiales y espacios múltiples."""
    if not texto:
        return ""
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()
    return texto

def es_texto_valido(texto, min_palabras=10):
    """
    Filtra comentarios de baja calidad:
    - Muy cortos (menos de min_palabras)
    - Spam obvio (muchos enlaces, emojis excesivos)
    - Anuncios
    """
    if not texto or len(texto.strip()) == 0:
        return False

    if texto.lower() in ["[deleted]", "[removed]", "deleted", "removed"]:
        return False

    palabras = texto.split()
    num_palabras = len(palabras)

    if num_palabras < min_palabras:
        return False

    num_enlaces = len(re.findall(r'http[s]?://', texto))
    if num_enlaces > 3:
        return False

    spam_keywords = [
        'click here', 'buy now', 'limited offer', 'subscribe',
        'check out my', 'follow me', 'dm me', 'upvote if'
    ]
    texto_lower = texto.lower()
    if any(keyword in texto_lower for keyword in spam_keywords):
        return False

    texto_sin_espacios = texto.replace(' ', '')
    if len(texto_sin_espacios) > 0:
        ratio_alfanumerico = sum(c.isalnum() for c in texto_sin_espacios) / len(texto_sin_espacios)
        if ratio_alfanumerico < 0.5:
            return False

    return True

def obtener_contexto_post(post):
    contexto_partes = []

    if post.title:
        contexto_partes.append(f"POST: {limpiar_texto(post.title)}")

    if post.selftext and post.selftext not in ["[deleted]", "[removed]", ""]:
        texto_post = limpiar_texto(post.selftext)
        if len(texto_post.split()) > 5:  # Solo incluir si tiene suficiente contenido
            contexto_partes.append(texto_post)

    return " | ".join(contexto_partes) if contexto_partes else "POST: [Sin título]"

def seleccionar_mejores_comentarios(comentarios, max_comentarios=30):
    """
    Selecciona los mejores comentarios basándose en:
    - Score (likes)
    - Validez del texto
    Devuelve máximo max_comentarios ordenados por relevancia.
    """
    comentarios_validos = []

    for comentario in comentarios:
        if not hasattr(comentario, 'body') or not comentario.body:
            continue

        texto = limpiar_texto(comentario.body)
        if not es_texto_valido(texto):
            continue

        # Solo incluir comentarios con al menos 1 upvote para calidad
        if comentario.ups < 1:
            continue

        comentarios_validos.append({
            'objeto': comentario,
            'texto': texto,
            'up': comentario.ups,
            'down': comentario.downs,
            'score': comentario.ups - comentario.downs
        })

    # Ordenar por score y tomar los mejores
    comentarios_validos.sort(key=lambda x: x['score'], reverse=True)
    return comentarios_validos[:max_comentarios]

def procesar_post(post, fecha_limite, contador_por_mes, id_counter, min_por_mes, max_por_mes):
    """
    Procesa un post individual y extrae comentarios válidos
    """
    try:
        contexto_post = obtener_contexto_post(post)
        if not contexto_post or contexto_post == "POST: [Sin título]":
            return None

        # Expandir comentarios
        post.comments.replace_more(limit=1)
        mejores_comentarios = seleccionar_mejores_comentarios(
            post.comments.list(),
            max_comentarios=50
        )

        entradas_mes = []
        for com_data in mejores_comentarios:
            comentario = com_data['objeto']
            texto_comentario = com_data['texto']

            fecha_comentario = datetime.utcfromtimestamp(comentario.created_utc)
            if fecha_comentario < fecha_limite:
                continue

            mes_key = (fecha_comentario.year, fecha_comentario.month)

            # VERIFICACIÓN ESTRICTA DE COTA SUPERIOR
            if mes_key not in contador_por_mes:
                continue

            if contador_por_mes[mes_key] >= max_por_mes:
                continue  # Saltar comentarios de meses que ya alcanzaron el máximo

            mensaje_completo = f"{contexto_post} || COMENTARIO: {texto_comentario}"

            entrada = {
                "id": id_counter,
                "mensaje": mensaje_completo,
                "año": fecha_comentario.year,
                "mes": fecha_comentario.month,
                "dia": fecha_comentario.day,
                "score": com_data["score"],
                "subreddit": post.subreddit.display_name
            }

            entradas_mes.append(entrada)
            id_counter += 1
            contador_por_mes[mes_key] += 1

        return {'entradas': entradas_mes, 'nuevo_id': id_counter}

    except Exception as e:
        print(f"Error procesando post: {e}")
        return None

def deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
    """
    Decide si debemos continuar buscando basado en:
    1. Objetivo total alcanzado
    2. Todos los meses tienen al menos el mínimo
    """
    if len(dataset) >= objetivo_entradas:
        return False

    # Verificar si TODOS los meses tienen al menos el mínimo
    for count in contador_por_mes.values():
        if count < min_por_mes:
            return True  # Continuar si algún mes no alcanzó el mínimo

    # Si todos tienen al menos el mínimo, verificar si alcanzamos el objetivo
    if len(dataset) < objetivo_entradas:
        # Pero solo continuar si algún mes no alcanzó el máximo
        for count in contador_por_mes.values():
            if count < max_por_mes:
                return True

    return False

def verificar_y_reportar_balance(contador_por_mes, min_por_mes, max_por_mes):
    """Reporta el estado actual del balance mensual"""
    print("\n" + "="*50)
    print("ESTADO ACTUAL DEL BALANCE MENSUAL:")
    print("="*50)

    meses_completos = 0
    meses_en_progreso = 0
    meses_faltantes = 0

    for mes in sorted(contador_por_mes.keys()):
        count = contador_por_mes[mes]
        if count >= max_por_mes:
            estado = "COMPLETO ✓"
            meses_completos += 1
        elif count >= min_por_mes:
            estado = f"EN PROGRESO ({count}/{max_por_mes})"
            meses_en_progreso += 1
        else:
            estado = f"FALTANTE ({count}/{min_por_mes})"
            meses_faltantes += 1

        print(f"  {mes[0]}-{mes[1]:02d}: {estado}")

    print(f"\nResumen: {meses_completos} completos, {meses_en_progreso} en progreso, {meses_faltantes} faltantes")
    return meses_faltantes > 0

def buscar_en_subreddits_especificos(tema, fecha_limite, contador_por_mes, dataset, id_counter,
                                   objetivo_entradas, min_por_mes, max_por_mes):
    """
    Busca en subreddits específicos de política con control de cotas
    """
    subreddits_politica = [
        "politics", "Conservative", "PoliticalDiscussion", "news",
        "Republican", "democrats", "PoliticalHumor", "moderatepolitics",
        "Libertarian", "centrist", "neoliberal", "AskThe_Donald",
        "walkaway", "louderwithcrowder", "trump", "BidenBuzz"
    ]

    for subreddit_name in subreddits_politica:
        if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
            break

        print(f"Buscando en r/{subreddit_name}...")
        try:
            posts_encontrados = 0
            posts_procesados = 0

            # Buscar con diferentes time_filters para cubrir diferentes períodos
            time_filters = ["year", "month", "week"]

            for time_filter in time_filters:
                if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
                    break

                print(f"  Time filter: {time_filter}")

                for post in reddit.subreddit(subreddit_name).search(tema, time_filter=time_filter, limit=100):
                    if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
                        break

                    fecha_post = datetime.utcfromtimestamp(post.created_utc)
                    if fecha_post < fecha_limite:
                        continue

                    posts_encontrados += 1
                    resultado = procesar_post(post, fecha_limite, contador_por_mes,
                                            id_counter, min_por_mes, max_por_mes)
                    if resultado:
                        dataset.extend(resultado['entradas'])
                        id_counter = resultado['nuevo_id']
                        posts_procesados += 1

                    # Verificar estado actual cada 10 posts
                    if posts_procesados % 10 == 0:
                        print(f"    Progreso: {len(dataset)} entradas")
                        verificar_y_reportar_balance(contador_por_mes, min_por_mes, max_por_mes)

                    time.sleep(0.1)

            print(f"  {subreddit_name}: {posts_procesados} posts procesados")

        except Exception as e:
            print(f"Error en r/{subreddit_name}: {e}")
            continue

    return dataset, id_counter

def buscar_en_todos_subreddits(tema, fecha_limite, contador_por_mes, dataset, id_counter,
                             objetivo_entradas, min_por_mes, max_por_mes):
    """
    Busca en todos los subreddits (all) con control de cotas
    """
    print("Buscando en todos los subreddits...")

    if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
        return dataset, id_counter

    posts_encontrados = 0
    posts_procesados = 0

    # Lista expandida de temas relacionados con Charlie Kirk
    temas_relacionados = [
        "charlie kirk", "\"charlie kirk\"", "charlie kirk turnpoint",
        "charlie kirk turn point", "charlie kirk twitter", "charlie kirk interview",
        "charlie kirk controversy", "charlie kirk debate", "charlie kirk speech",
        "charlie kirk campus", "charlie kirk tpusa", "charlie kirk turning point",
        "charlie kirk fox news", "charlie kirk podcast", "charlie kirk student",
        "charlie kirk protest", "charlie kirk university", "charlie kirk college",
        "turning point usa", "tpusa", "charliekirk"
    ]

    # Usar diferentes time_filters para cubrir diferentes períodos temporales
    time_filters = ["year", "month", "week"]

    for time_filter in time_filters:
        if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
            break

        print(f"  Time filter: {time_filter}")

        for query in temas_relacionados:
            if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
                break

            print(f"    Query: '{query}'")
            try:
                for post in reddit.subreddit("all").search(query, time_filter=time_filter, limit=100):
                    if not deberia_continuar_busqueda(contador_por_mes, min_por_mes, max_por_mes, objetivo_entradas, dataset):
                        break

                    fecha_post = datetime.utcfromtimestamp(post.created_utc)
                    if fecha_post < fecha_limite:
                        continue

                    posts_encontrados += 1
                    resultado = procesar_post(post, fecha_limite, contador_por_mes,
                                            id_counter, min_por_mes, max_por_mes)
                    if resultado:
                        dataset.extend(resultado['entradas'])
                        id_counter = resultado['nuevo_id']
                        posts_procesados += 1

                    # Reporte periódico
                    if posts_procesados % 20 == 0:
                        print(f"      Procesados: {posts_procesados} posts | Entradas: {len(dataset)}")
                        verificar_y_reportar_balance(contador_por_mes, min_por_mes, max_por_mes)

                    time.sleep(0.1)

            except Exception as e:
                print(f"Error en búsqueda con query '{query}': {e}")
                continue

    print(f"  Total en 'all': {posts_procesados} posts procesados")
    return dataset, id_counter

def verificar_balance_mensual(contador_por_mes, min_por_mes):
    """
    Verifica si todos los meses tienen el mínimo requerido
    """
    meses_faltantes = []
    for mes, count in contador_por_mes.items():
        if count < min_por_mes:
            meses_faltantes.append((mes, count))

    return meses_faltantes

def recolectar_posts_y_comentarios(tema, meses=12, objetivo_entradas=10000, min_por_mes=500, max_por_mes=1500):
    """
    Recoge comentarios con contexto del post de manera balanceada por mes
    """
    fecha_limite = datetime.utcnow() - timedelta(days=30 * meses)
    dataset = []
    id_counter = 1

    # Inicializar contador para todos los meses en el rango
    contador_por_mes = defaultdict(int)
    fecha_actual = datetime.utcnow()
    for i in range(meses + 1):  # +1 para incluir mes actual
        fecha_mes = fecha_actual - timedelta(days=30 * i)
        mes_key = (fecha_mes.year, fecha_mes.month)
        contador_por_mes[mes_key] = 0

    print(f"Iniciando recolección para: '{tema}'")
    print(f"Período: {meses} meses (desde {fecha_limite.strftime('%Y-%m-%d')})")
    print(f"Objetivo: {objetivo_entradas} entradas")
    print(f"Balance mensual: {min_por_mes} - {max_por_mes} entradas/mes")
    print("-" * 60)

    # Mostrar meses que vamos a cubrir
    print("Meses objetivo:")
    for mes in sorted(contador_por_mes.keys()):
        print(f"  - {mes[0]}-{mes[1]:02d}")

    # Estrategia 1: Buscar en subreddits específicos de política
    dataset, id_counter = buscar_en_subreddits_especificos(
        tema, fecha_limite, contador_por_mes, dataset, id_counter,
        objetivo_entradas, min_por_mes, max_por_mes
    )

    # Estrategia 2: Buscar en todos los subreddits si aún necesitamos más
    if len(dataset) < objetivo_entradas:
        dataset, id_counter = buscar_en_todos_subreddits(
            tema, fecha_limite, contador_por_mes, dataset, id_counter,
            objetivo_entradas, min_por_mes, max_por_mes
        )

    # Verificar balance mensual
    meses_faltantes = verificar_balance_mensual(contador_por_mes, min_por_mes)
    if meses_faltantes:
        print(f"\n⚠  Meses con menos de {min_por_mes} entradas:")
        for mes, count in meses_faltantes:
            print(f"  - {mes[0]}-{mes[1]:02d}: {count} entradas")

    print(f"\nRecolección finalizada: {len(dataset)} entradas")
    print("Distribución final por mes:")
    for mes in sorted(contador_por_mes.keys()):
        count = contador_por_mes[mes]
        status = "✓" if count >= min_por_mes else "✗"
        print(f"  {mes[0]}-{mes[1]:02d}: {count} {status}")

    return pd.DataFrame(dataset)

if _name_ == "_main_":
    # Configuración inicial de Reddit (asegúrate de tener esto configurado)
    # reddit = praw.Reddit(client_id='...', client_secret='...', user_agent='...')

    tema_principal = "charlie kirk"

    datos = recolectar_posts_y_comentarios(
        tema=tema_principal,
        meses=12,
        objetivo_entradas=10000,
        min_por_mes=500,
        max_por_mes=1500
    )

    if len(datos) == 0:
        print("No se recolectaron datos. Verifica tus credenciales o amplía el período.")
        exit()

    # Post-procesamiento
    datos_unicos = datos.drop_duplicates(subset=['mensaje'], keep='first')
    print(f"\nDatos únicos después de eliminar duplicados: {len(datos_unicos)}")

    # Ordenar por fecha
    datos_unicos = datos_unicos.sort_values(['año', 'mes', 'dia']).reset_index(drop=True)

    # Guardar resultados
    nombre_archivo = "comentarios_charlie_kirk_balanceado.csv"
    datos_unicos.to_csv(nombre_archivo, index=False, encoding="utf-8")

    # Generar reporte final
    print(f"\n{'='*60}")
    print("RESUMEN FINAL:")
    print(f"{'='*60}")
    print(f"Total de entradas guardadas: {len(datos_unicos)}")

    distribucion = datos_unicos.groupby(['año', 'mes']).size()
    print(f"\nDistribución final por mes:")
    for (año, mes), count in distribucion.items():
        status = "✓" if count >= 500 else "✗"
        print(f"  {año}-{mes:02d}: {count} {status}")

    print(f"\nSubreddits incluidos: {sorted(datos_unicos['subreddit'].unique())}")
    print(f"\nRango de scores: {datos_unicos['score'].min()} - {datos_unicos['score'].max()}")
    print(f"Score promedio: {datos_unicos['score'].mean():.2f}")
    print(f"\nArchivo guardado: {nombre_archivo}")
