import requests
import csv
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

print("Парсинг Hacker News...")

# Получаем список новых постов
top_stories = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json").json()[:10]

posts = []
for story_id in top_stories:
    story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()
    if story and "title" in story:
        posts.append({
            "title": story["title"],
            "score": story.get("score", 0),
            "author": story.get("by", "unknown")
        })
        print(f"Загружен: {story['title'][:50]}...")

# Сохраняем в CSV
with open("hn_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "score", "author"])
    writer.writeheader()
    writer.writerows(posts)

print(f"\nСохранено {len(posts)} постов в hn_posts.csv")

# Анализ через DeepSeek
if DEEPSEEK_API_KEY:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
    
    titles = "\n".join([f"- {p['title']}" for p in posts])
    prompt = f"""Ты — эксперт по Data Science. Проанализируй эти темы с Hacker News.
    
    Заголовки:
    {titles}
    
    Напиши ответ в таком формате:
    1. [Самая важная тема для Junior DS] - почему
    2. [Вторая по важности] - почему
    3. [Третья] - почему
    """
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    
    analysis = response.choices[0].message.content
    print("\n" + "="*50)
    print("АНАЛИЗ DEEPSEEK:")
    print("="*50)
    print(analysis)
    
    with open("analysis.txt", "w", encoding="utf-8") as f:
        f.write(analysis)
else:
    print("API ключ не найден. Проверь файл .env")