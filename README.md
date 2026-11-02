# Pytests: Auth Signup

## Описание проекта

Проект содержит автоматизированные API-тесты для проверки работы эндпоинта регистрации пользователя:

`POST /api/Auth/signup`

Тестирование выполняется с помощью python, pytest и requests

В проекте проверяются:
- Успешная регистрация пользователя.
- Валидация некорректного email.
- Обработка пустого email.
- Обработка некорректного JSON.
- Повторная отправка запроса с одним и тем же email.

## Технологии

- Python
- pytest
- requests
- Faker

## Установка и запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/ToSky26/project.git
cd project
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

Активация виртуального окружения:

```bash
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск тестов

```bash
pytest tests/ -v
```

## Структура проекта

```text
project/
├── tests/
│   ├── __init__.py
│   ├── test_signup.py
│   └── conftest.py
├── requirements.txt
├── README.md
└── .gitignore
```

**Назначение файлов:**
- `test_signup.py` — тесты для эндпоинта /api/Auth/signup
- `conftest.py` — фикстуры и настройки для тестов
- `requirements.txt` — зависимости проекта
- `README.md` — инструкции по проекту
- `.gitignore` — игнорируемые файлы 

## Пример ожидаемого вывода тестов
Ожидаемый вывод при успешном прохождении всех тестов:

```text
tests/test_signup.py::TestAuthSignup::test_signup_success PASSED
tests/test_signup.py::TestAuthSignup::test_signup_email_validation[invalid-email-user.email.isInvalid-Invalid email format] PASSED
tests/test_signup.py::TestAuthSignup::test_signup_email_validation[-user.email.isRequired-Email is required.] PASSED
tests/test_signup.py::TestAuthSignup::test_signup_with_invalid_json PASSED
tests/test_signup.py::TestAuthSignup::test_signup_with_same_email_twice PASSED

============================== 5 passed ==============================
```

## Автор 
**ФИО:** Сакаева Александра 
GitHub: [ToSky26](https://github.com/ToSky26)