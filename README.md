# Обзор приложения

Это приложение на FastAPI предоставляет простую функциональность электронной коммерции, включающую аутентификацию пользователей, управление продуктами и корзиной. Приложение поддерживает базовые CRUD-операции и управление пользователями, позволяя пользователям создавать учетную запись, входить в систему, добавлять продукты в корзину и оформлять заказ.

## Основные функции
- **Аутентификация пользователей**: Пользователи могут регистрироваться, входить в систему и выходить из приложения.
- **Управление продуктами**: Продукты могут быть добавлены, обновлены, удалены и перечислены для просмотра пользователями.
- **Управление корзиной**: Пользователь может иметь только одну активную корзину одновременно, которую можно обновлять, добавлять продукты и оформлять заказ.

## API эндпоинты

### Аутентификация пользователей
- **POST /auth/register**: Регистрация нового пользователя с указанием электронной почты, имени пользователя и пароля.
- **POST /auth/login**: Вход в систему и получение токена доступа в виде cookie.
- **POST /auth/logout**: Выход текущего пользователя путем удаления cookie с токеном.
- **GET /auth/current-user**: Получение информации о текущем аутентифицированном пользователе.

### Управление продуктами
- **POST /products/**: Создание нового продукта.
- **GET /products/**: Получение списка всех продуктов с поддержкой пагинации.
- **GET /products/{product_id}**: Получение информации о продукте по его ID.
- **PUT /products/{product_id}**: Обновление информации о продукте.
- **DELETE /products/{product_id}**: Удаление продукта по его ID.

### Управление корзиной
- **POST /baskets/**: Получение или создание активной корзины для текущего пользователя.
- **POST /baskets/items**: Добавление продукта в корзину или обновление количества, если продукт уже есть в корзине.
- **DELETE /baskets/items/{item_id}**: Удаление продукта из корзины или уменьшение его количества.
- **PUT /baskets/checkout**: Изменение статуса корзины на "неактивный" после оформления заказа.

## Как запустить
1. Клонируйте репозиторий.
2. Установите зависимости с помощью команды `pip install -r req.txt`.
3. Запустите приложение с помощью команды `uvicorn app.main:app`.

## Требования
- **Python 3.9+**
- **FastAPI**
- **SQLAlchemy**
- **asyncpg** (для PostgreSQL)
- **Pydantic**

## Дополнительные заметки
- Убедитесь, что PostgreSQL база данных настроена, и данные для подключения указаны в настройках окружения.
- Это приложение использует асинхронные сессии SQLAlchemy для управления транзакциями в базе данных, и все основные взаимодействия с базой данных обрабатываются через классы репозиториев для лучшего разделения ответственности.
- При добавлении, удалении поштучно или полностью: меняется цена и количество в самой корзинке, также при оформлении заказа ( переход корзины с состояния True на False); все продукты, которые были заказаны, уменьшаются в количестве в БД
- При добавление продукта в корзину, почти не задействован параметр price (который указан в модельке BasketItem), понимаю, что это скидка, но не до конца понял, как это реализовать


![](eren.gif)
