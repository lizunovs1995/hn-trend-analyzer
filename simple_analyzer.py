import requests
import csv
from openai import OpenAI

# ВСТАВЬ СЮДА СВОЙ КЛЮЧ (между кавычками)
DEEPSEEK_API_KEY = "sk-33b63b8690c24a30ba0ab0623fcf4189"

print("Загрузка постов с Hacker News...")

# Получаем посты
response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
posts = []
for post_id in response.json()[:10]:
    data = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json").json()
    if data and "title" in data:
        posts.append({"title": data["title"], "score": data.get("score", 0)})
        print(f"Загружен: {data['title'][:50]}...")

# Сохраняем CSV
with open("posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "score"])
    writer.writeheader()
    writer.writerows(posts)
print(f"\n✅ Сохранено {len(posts)} постов")

# Анализ DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
titles = "\n".join([f"- {p['title']}" for p in posts])

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": f"Ты эксперт по DS. Выдели 3 главные темы для Junior из:\n{titles}"}]
)

print("\n" + "="*50)
print("АНАЛИЗ DEEPSEEK:")
print("="*50)
print(resp.choices[0].message.content)