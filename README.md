# Приложение для предсказания трафика веб-сайта
Данное веб-приложение позволяет предсказывать трафик русскоязычной википедии за указанный период с использованием моделей SARIMA, Cat Boost и Prophet.
### Структура проекта
- `train` - содержит ноутбуки для разведочного анализа и обучения моделей
- `frontend` - содержит файл для запуска фронтенда приложения на основе Streamlit
- `backend` - содержит файл для запуска бэкенда приложения на основе Fast API
- `models` - содержит предобученные модели
- `media` - содержит медиафайлы для описания проекта
- `helpers.py`- содержит вспомогательные методы

Для запуска приложения используйте следующие команды:
```python
# Создание образа
docker-compose up -d --build
docker-compose up -d
```
## Демонстрация работы приложения
Для проверки рецензии на спойлеры введите текст рецензии и нажмите на кнопку "Проверить", далее произойдет перенаправление на страницу с результатом.
![Демо](https://github.com/ASoloveva01/Web_Traffic_Forecasting/blob/main/media/демо.gif)
  
## Результаты
### SARIMA
RMSE: 145339761.7
![Иллюстрация к проекту](https://github.com/ASoloveva01/Web_Traffic_Forecasting/blob/main/media/sarima_results.png)
## Cat Boost
RMSE: 145339761.7
![Иллюстрация к проекту](https://github.com/ASoloveva01/Web_Traffic_Forecasting/blob/main/media/catboost_results.png)
## Prophet
RMSE: 933651128.6
![Иллюстрация к проекту](https://github.com/ASoloveva01/Web_Traffic_Forecasting/blob/main/media/prophet_results.png)
