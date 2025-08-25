#!/bin/sh
# entrypoint.sh

# Ждём, пока база поднимется
echo "Ожидаем запуска Postgres..."
sleep 5  # можно заменить на loop с проверкой порта для надёжности

# Применяем миграции Alembic
echo "Применяем миграции..."
alembic upgrade head

# Запускаем приложение
echo "Запуск приложения..."
exec python main.py