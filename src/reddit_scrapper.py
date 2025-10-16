import praw
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import time

class RedditScraper:
    def __init__(self):
        # iniciar sesión para scrappear
        self.reddit = praw.Reddit(
            client_id="___",
            client_secret="___",
            user_agent="script:buscador:v1.0 (by u/TU_USUARIO)"
        )
        
        # Configuración general
        self.MIN_TOTAL_COMMENTS = 5000
        self.MAX_TOTAL_COMMENTS = 10000
        self.MIN_WORDS = 5
        self.MIN_COMMENTS_PER_MONTH = 200
        
    # devuelve la fecha año-mes
    def get_month_key(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return f"{dt.year}-{dt.month:02d}"

    # ver si es un mensaje eliminado o si es lo minimo de largo para ser relevante y estudiable
    def is_valid_comment(self, comment: str) -> bool:
        if not comment or comment == "[deleted]" or comment == "[removed]":
            return False
        if len(comment.split()) < self.MIN_WORDS:
            return False
        return True

    # buscamos en subreddis relevantes, si no llegamos al objetivo buscamos en  reddit en general con 'all'
    def search_subreddits(self):
        relevant_subreddits = [
            'politics', 'Conservative', 'ToiletPaperUSA', 'news', 
            'PoliticalDiscussion', 'democrats', 'republicans'
        ]
        for subreddit in relevant_subreddits:
            yield self.reddit.subreddit(subreddit)
        yield self.reddit.subreddit('all')

    # ponemos distintas queries de charlie y buscamos los comentarios
    def scrape_comments(self):
        monthly_data = defaultdict(list)
        total_comments = 0
        
        # esto saca el rango de los 12 meses para colocar los comentarios
        current_date = datetime.now()
        month_ranges = []
        for i in range(12):
            end_date = current_date - timedelta(days=30*i)
            start_date = end_date - timedelta(days=30)
            month_ranges.append((start_date, end_date))

        # en vez de solo buscar charlie kirk, buscamos tambien algunas cosas relacionadas con el 
        search_queries = [
            'Charlie Kirk', 'CharlieKirk', 'TPUSA', 'Turning Point USA',
            'Kirk AND Conservative', 'Kirk AND TPUSA'
        ]

        # buscamos en los subredis
        for subreddit in self.search_subreddits():
            # si ya tenemos suficientes comentarios se para
            if all(len(monthly_data[self.get_month_key(mr[0].timestamp())]) >= self.MIN_COMMENTS_PER_MONTH 
                   for mr in month_ranges):
                break

            # para cada query
            for query in search_queries:
                try:
                    posts = subreddit.search(query, sort='comments', time_filter='year', limit=None)
                    
                    for post in posts:
                        post_month = self.get_month_key(post.created_utc)
                        
                        # Si ya tenemos suficientes comentarios para este mes, continuamos
                        if len(monthly_data[post_month]) >= self.MIN_COMMENTS_PER_MONTH:
                            continue

                        # procesamos el comentario y si es viable lo guardamos
                        post.comments.replace_more(limit=5)
                        for comment in post.comments.list():
                            if not self.is_valid_comment(comment.body):
                                continue

                            parent_text = comment.parent().body if comment.parent_id != comment.link_id else post.title
                            if not self.is_valid_comment(parent_text):
                                continue

                            data = {
                                'timestamp': datetime.fromtimestamp(comment.created_utc),
                                'score': comment.score,
                                'parent_text': parent_text,
                                'comment_text': comment.body,
                                'subreddit': str(subreddit)
                            }
                            
                            comment_month = self.get_month_key(comment.created_utc)
                            monthly_data[comment_month].append(data)
                            total_comments += 1

                except Exception as e:
                    time.sleep(2)  # Esperar en caso de rate limiting

                if total_comments >= self.MAX_TOTAL_COMMENTS:
                    break

        # Combinar todos los datos
        all_data = []
        for month_data in monthly_data.values():
            all_data.extend(month_data)

        # elimina duplicados y guarda
        df = pd.DataFrame(all_data)
        df_clean = df.drop_duplicates(subset=['comment_text', 'parent_text'])
        df.to_csv('charlie_kirk_comments.csv', index=False)
        
        monthly_stats = df.groupby(df['timestamp'].dt.to_period('M')).size()
        
        return df

scraper = RedditScraper()
df = scraper.scrape_comments()
        
print(f"\nTotal de comentarios: {len(df)}")
print("\nComentarios por mes:")
print(df.groupby(df['timestamp'].dt.to_period('M')).size())
        