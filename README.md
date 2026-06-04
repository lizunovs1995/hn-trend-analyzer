# Hacker News Trend Analyzer

## 📊 Что это
Автоматический анализатор трендов для Junior Data Scientist.  
Парсит Hacker News, анализирует заголовки через DeepSeek API и выделяет 3 самые важные темы.

## 🛠️ Стек
- Python (requests, OpenAI SDK)
- DeepSeek API (бесплатно, 1M контекста)
- Git + GitHub Actions

## 🎯 Результат
Ежедневный отчёт о том, на чём фокусироваться Junior DS, чтобы быть в тренде.

## 🚀 Как запустить
```bash
git clone https://github.com/lizunovs1995/hn-trend-analyzer.git
cd hn-trend-analyzer
pip install requests openai
python hn_analyzer.py
