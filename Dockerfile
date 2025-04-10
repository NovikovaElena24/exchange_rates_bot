# Используем официальный образ Python
FROM python:3.12.9-slim

# Установим рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Укажите команду для запуска бота
CMD ["python", "/app/bot.py"]