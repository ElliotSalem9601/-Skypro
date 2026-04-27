# Автоматизация тестирования личных событий Skyeng

## Описание проекта

Проект содержит автоматизированные UI и API тесты для функциональности "Личные события" в расписании портала преподавателя Skyeng. Тесты основаны на [финальной работе по ручному тестированию](https://elliotsalem9601.yonote.ru/share/c5147b1d-c7f2-4428-8bde-53912e961e8b) и покрывают критическую функциональность CRUD операций с личными событиями.

## Структура проекта
skyeng_calendar_auto/
├── config/ # Конфигурационные файлы
├── pages/ # Page Object Models
│ ├── base_page.py
│ ├── login_page.py
│ └── calendar_page.py
├── tests/ # Тестовые файлы
│ ├── test_api.py # API тесты (5+)
│ └── test_ui.py # UI тесты (5+)
├── utils/ # Утилиты
│ └── api_client.py # API клиент
├── data/ # Тестовые данные
├── reports/ # Allure отчеты
├── .env.example # Пример конфигурации
├── requirements.txt # Зависимости
└── README.md