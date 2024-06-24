from typing import Dict
from fastapi import FastAPI, Request
import uvicorn
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

def create_app() -> FastAPI:
    app = FastAPI(title="Text Summarizer")

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    @app.post("/summarize")
    async def summarize(request: Request) -> Dict[str, str]:
        data = await request.json()
        text = data.get("text", "")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        return {"summary": summary}

    return app

# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("main:create_app", host='127.0.0.1', port=8000, reload=True)
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")