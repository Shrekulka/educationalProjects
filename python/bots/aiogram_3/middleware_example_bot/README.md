# Most common tasks solved by bot developers (and not only bots) using middlewares.

1. Querying the database to fetch user roles
   Often it's necessary to classify users based on certain roles to provide different functionalities depending on these
   roles. Regular users might have basic functionality, users who have fulfilled certain conditions or paid for a status
   change might have extended functionality, while admins might have god-mode. User updates themselves do not inform us 
   about the user's role in our system. Such classification can only be done autonomously by changing user statuses 
   based on certain conditions. However, when an update comes in, it would be useful to know the role of the user 
   generating that update to direct them along a role-specific path. Let's consider at which stage we'd like to know the
   user's role. The simplest would be to use filters on routers. That is, we can create a specific router for each role 
   and register handlers on this router to process updates from users with that role. Consequently, we need to know the 
   role in the filters, and thus the optimal place to determine the role is in an external middleware.
2. Shadow Ban
   Telegram bots themselves don't have functionality to ban users in a way that prevents them from messaging the bot. 
   However, such a need arises, especially in group chats. There are many groups where users can request various image,
   music, or text generations using artificial intelligence, and these bots "live" in groups alongside regular users who
   can request generations from them. Generating something with neural networks is resource-intensive, so bot admins 
   limit users to a certain number of generations within a specific time frame to reduce computational load and provide
   equal generation opportunities for all group members. Thus, sometimes it's necessary to restrict users' access to bot
   functionality, and since directly banning a user is either impossible or simply not advisable, a mechanism called 
   shadow banning is implemented, where the bot simply ignores updates from users with specific IDs. Similar to the 
   previous point, it's important to understand that update processing doesn't need to happen at the earliest stage to 
   reduce the number of actions with the update. Therefore, an external middleware for Update events is needed.
3. Passing database connection to filters and handlers
   One of the most common uses of middlewares in Telegram bots is passing a database connection from the connection pool
   to filters, handlers, and/or other middlewares. Sometimes it's not just a connection but an instance of a class that 
   provides database access with an already open connection using predefined methods. If your bot needs to work with the
   database in external middlewares or filters, creating an instance of the class should be done in one of the external 
   middlewares. If your bot doesn't need to fetch any information from the database before the update passes through the
   filters, then the optimal place to create the class instance would be in an internal middleware, where we already 
   know that the filters have been passed and the update will reach a handler where database work might be necessary.
4. Determining user language for preparing translations
   This task is similar to determining the user's role because at the early stage of update processing, it's necessary 
   to determine the language set by the user in settings to send them texts in the corresponding language.
5. Determining user timezone
   Similarly to language settings, sometimes user timezone settings matter to set up some notification at a specific 
   time or to schedule a message not when it's deep night for the user.
6. Logging
   Middlewares can be used for logging specific events. One might think, why not just write logs in filters and handlers,
   why use middlewares? To avoid touching the handler and filter code. The bot works as intended, why interfere with the
   already working code just to log something? Almost any information can be obtained from the update without the need 
   to log directly in handlers. We write a middleware and connect it with a single line where needed. Collect the 
   necessary logs.
7. Measuring execution time to identify bottlenecks
   With middlewares, you can measure bot performance at different stages with minimal interference with the main code. 
   Separate middlewares with time measurement functionality are written and connected in the necessary places to collect
   statistics and track the most resource-intensive parts of the pipeline for optimization.
8. Caching
   It doesn't always make sense to make the same requests to some external service or to the database every time 
   information from them is needed. Sometimes it's possible to store previously obtained results in a cache and read 
   them from there. Middlewares are convenient for working with caches, saving bot resources.
9. Throttling
   Sometimes it's not necessary to completely ignore updates from a specific user, but it's desirable to reduce the 
   number of user requests to the bot within a unit of time. For example, to prevent a user from clicking an inline 
   button too frequently or sending a certain command too often.

## Example 2. Shadow Ban

Let's demonstrate how a middleware implementing shadow banning for users might look like. We assume that in the 
database, we store the user's status (banned/not banned) and can cache this status for users to minimize database 
queries. Based on the user's status, we decide whether to process updates from the user or not.

Since in this example, we don't want to handle any updates from shadow-banned users at all, we'll attach the middleware 
to the root router (dispatcher) for Update events.

One possible implementation of middleware for shadow banning could look like this:
```bash
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

# Cache of banned user IDs
CACHE = {'banned': [254443334, 214454432, 112221212],}

class ShadowBanMiddleware(BaseMiddleware):
    """
    Middleware for handling shadow bans.

    This middleware checks if the user sending the event is banned.
    If banned, it stops further event processing.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Execute the event handler, checking for shadow bans.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): Event handler.
            event (TelegramObject): Event object.
            data (Dict[str, Any]): Event data.

        Returns:
            Any: Result of executing the handler or None if the user is banned.
        """
        # Get the user from the event data
        user: User = data.get('event_from_user')
        # Check if the user is banned
        if user is not None:
            if user.id in CACHE.get('banned'):
                # If banned, stop further event processing
                return

        # Continue event processing
        return await handler(event, data)
```

And the middleware is connected in the familiar way:
```bash
dp.update.middleware(ShadowBanMiddleware())
```
Here, it's important to note that the CACHE dictionary is only for demonstration purposes and should not be stored in 
the same module as the middleware, let alone be a global variable. In practice, the cache is often initialized in the 
entry point and passed to other objects using a special storage in the dispatcher called workflow_data.

## Example 9. Throttling

Throttling is the reduction of the number of processed requests relative to their total number. In the previous example,
we implemented middleware that drops all updates from banned users altogether. But sometimes, we just want to let the 
user know that if they poke the bot too often, the process may not only not speed up but even slow down.

Here, you need to be careful not to give users who are using the bot correctly the feeling that the bot has hung up and 
is no longer working, so you also need to devise a warning system. But the general idea of throttling middleware is as 
follows. We take any key-value pair cache with the ability to set the key's lifetime (Redis, NATS, or even just TTLCache
from the cachetools library), and for each update from the user, we put their ID (user's, not update's) in the cache and 
set the lifetime for such a key. In the middleware, we check for the presence of the key assigned to the user whose 
update has just arrived. If the key is not there, we add the key to the cache and let the update pass further down the 
processing chain. But if the key exists, we simply drop the update. The cache will automatically delete the key when its 
lifetime expires. Thus, not all user updates will be processed, only those that come no more often than a certain time 
interval.
```bash
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

# Creating a cache with TTL (time to live) for keys
CACHE = TTLCache(maxsize=10_000, ttl=5)  # Maximum cache size - 10000 keys, and the key's time to live - 5 seconds

class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware for rate limiting.

    This middleware prevents the handler from being executed again
    if it is called too frequently.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Execute the event handler with rate limiting.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): Event handler.
            event (TelegramObject): Event object.
            data (Dict[str, Any]): Event data.

        Returns:
            Any: Result of executing the handler or None if the event is being executed too frequently.
        """
        # Get the user from the event data
        user: User = data.get('event_from_user')

        # Check if the event has already been processed
        if user.id in CACHE:
            return

        # Set the event processing flag in the cache
        CACHE[user.id] = True

        # Execute the event handler
        return await handler(event, data)
```

The middleware should also be registered with the dispatcher if you want to throttle any user actions or on a specific 
router if you want to slow down processing within handlers of a specific router.
```bash
dp.update.middleware(ThrottlingMiddleware())
```

And don't forget to install the cachetools library if you experiment with the proposed method:
```bash
pip install cachetools
```

Now, for each user action, a key with their ID will be added to the cache if it wasn't there before, and if the key 
existed, the update from that user will be dropped.

## Dependency Injection Example

If an object in your project is created only once (for example, a Config class object, or a database connection pool, or
some API tokens for external services), you can pass them without using middlewares. It's enough to put these objects in
a special storage called workflow_data in the main file, which can be accessed through the dispatcher.

### Workflow_data Storage
The dispatcher has a special storage called workflow_data, which works like an ordinary dictionary. This means that you 
can use it to pass data shared across the entire project, including some configuration data from the entry point.

It works like this:
```bash
from aiogram import Bot, Dispatcher

# ...

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()

some_var_1 = 1
some_var_2 = 'Some text'

dp.workflow_data.update({'my_int_var': some_var_1, 'my_text_var': some_var_2})

# or like this
dp['my_int_var'] = some_var_1
dp['my_text_var'] = some_var_2

# ...
```

Somewhere in the handlers, we can directly specify the corresponding keys in the handler signature:
```bash
@router.message(CommandStart())
async def process_start_command(message: Message, my_int_var, my_text_var):
    await message.answer(text=str(my_int_var))
    await message.answer(text=my_text_var)
```

In the handler signature, we simply specify the arguments that match the keys in the dictionary we put in the main.py 
module into the dp.workflow_data dictionary, and now within the handler, the values will be accessible via these keys.

However, if you need to pass data that you don't have at the time the bot starts or that may dynamically change during 
the process, middlewares become a convenient tool.

#### Here's an example of how you can inject a dictionary with the required language into middleware to make it 
#### available in handlers.

So, the general idea is as follows. In our project, we have modules with dictionaries that store key-value pairs. The 
keys are translation identifiers, and the values are the actual translations. This is clear. The keys in all 
dictionaries are the same, but the values depend on the language for which the dictionary is prepared. In middleware, we
can get the user's language (from the update or from the database, it doesn't matter) and put the dictionary containing
the texts in the user's language under the key 'i18n' - this is often called the object responsible for 
internationalization, the dictionary that stores texts in the user's language. After that, in the handlers, a reference 
to the required dictionary becomes available to us.

Let's say in the lexicon package we have two modules: lexicon_ru.py and lexicon_en.py, inside which there are 
dictionaries of the same structure but with texts in different languages. 
Here's an example:

1. 📁 lexicon/lexicon_ru.py
```bash
LEXICON_RU: dict[str, str] = {
    '/start': 'Привет!\n\nЯ эхо-бот для демонстрации работы миддлварей!\n\n'
              'Если хотите - можете мне что-нибудь прислать',
    'no_echo': 'Данный тип апдейтов не поддерживается '
               'методом send_copy',
    'button': 'Кнопка',
    'button_pressed': 'Вы нажали кнопку!'
}
```
2. 📁 lexicon/lexicon_en.py
```bash
LEXICON_EN: dict[str, str] = {
    '/start': "Hello!\n\nI'm an echo bot to demonstrate how middleware works!\n\n"
              "If you want, you can send me something",
    'no_echo': 'This type of update is not supported by the send_copy method',
    'button': 'Button',
    'button_pressed': "You've pressed the button!"
}
```
3. In the entry point main.py, we can gather all translations into one dictionary and pass it when starting polling 
   using the dispatcher: (main.py)
```bash
from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU

# ...

# Dictionary for storing translations
translations = {
    'default': 'ru',  # Setting the default language
    'en': LEXICON_EN,  # English lexicon
    'ru': LEXICON_RU,  # Russian lexicon
}

async def main():

# ...

# Start polling with passing the translation dictionary
await dp.start_polling(bot, _translations=translations)
```
4. Well, we also need middleware that will determine the user's language and inject the necessary translation. It will 
   be stored in the middleware package in the i18n.py module. (📁 middlewares/i18n.py)
```bash
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User

class TranslatorMiddleware(BaseMiddleware):
    """
        Middleware for translating text depending on the user's language.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]):
                Event handler.
            event (TelegramObject):
                Event source.
            data (Dict[str, Any]):
                Event data.

        Returns:
            Any: Result of executing the event handler.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],  # Event handler
        event: TelegramObject,  # Event
        data: Dict[str, Any]    # Data
    ) -> Any:
        """
           Call middleware.

           Args:
               handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]):
                   Event handler.
               event (TelegramObject):
                   Event source.
               data (Dict[str, Any]):
                   Event data.

           Returns:
               Any: Result of executing the event handler.
        """
        # Get the user from the event data
        user: User = data.get('event_from_user')

        # If there is no user, skip the handler
        if user is None:
            return await handler(event, data)

        user_lang = user.language_code            # Get the user's language
        translations = data.get('_translations')  # Get the translation dictionary

        i18n = translations.get(user_lang)        # Get translations for the user's language

        # If there are no translations for the specified language
        if i18n is None:
            # Take the default translations
            data['i18n'] = translations[translations['default']]
        else:
            # Use translations for the specified language
            data['i18n'] = i18n

        # Pass the handler with updated data
        return await handler(event, data)
```
5. Now, when we register the middleware in the main function of the main.py module:
```bash
from middlewares.i18n import TranslatorMiddleware

# ...

async def main():
    
    # ...
    # Registering middleware here
    dp.update.middleware(TranslatorMiddleware())
```
6. In handlers, access to the dictionary with the translation for the specific user's language, whose update we 
   currently want to process in the handler, will be available. Here's an example of a handler for the /start command:
```bash
# This handler responds to the /start command and supports 2 languages (Russian and English).
@user_router.message(CommandStart(), MyTrueFilter())
async def process_start_command(message: Message, i18n: dict[str, str]) -> None:
    """
        Handler for the /start command.
    
        Args:
            message (Message):
                Message object.
            i18n (dict[str, str]):
                Dictionary with translations.
    
        Returns:
            None
    """
    # Create an inline button object
    button = InlineKeyboardButton(
        text=i18n.get('button'),        # Button text
        callback_data='button_pressed'  # Callback data
    )
    # Create an inline keyboard object
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Send a message to the user
    await message.answer(text=i18n.get('/start'), reply_markup=markup)
```

## Key Points about Middleware:
1. Middleware is intermediate software that can be embedded into the main process of a service to modify or enrich data, 
   validate it, reject further processing, and so on.
2. In aiogram, middleware is divided into external and internal. External ones start working before the update enters 
   the filters, while internal ones work after leaving the filters and before entering the handlers.
3. Each middleware can be configured to execute some code on entering the middleware and exiting it.
4. In any middleware, you can drop an update, stopping its further movement along the processing chain.
5. Middleware is attached to routers for specific types of events.
6. Middleware can be implemented as classes and as functions.
7. Each middleware implemented based on a class must inherit from BaseMiddleware and contain an implementation of the 
   call method.
8. The call method, in addition to a reference to the class instance, accepts 3 mandatory arguments:
   - handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
   - event: TelegramObject,
   - data: Dict[str, Any].
9. The construction for connecting a class-based middleware looks like this:
```bash
<router_name>.<event_type>.<middleware_type>(<middleware_name>())
```
10. The construction for connecting a function-based middleware differs in that you don't need to write a call operator 
    after the middleware name:
```bash
<router_name>.<event_type>.<middleware_type>(<middleware_name>)
```
However, it's more convenient to register function-based middlewares using decorators in the same modules where routers 
are initialized and to which middlewares are attached.

11. Function-based middlewares are convenient to use at the level of individual modules for small tasks.
12. If you need a middleware into which all updates will fall, you should attach it to the dispatcher for the Update 
    event type. In this case, there is no difference whether to connect this middleware as external or internal.
13. There is no difference in connecting external and internal middlewares only for the Update event; for other event 
    types, you need to understand whether you want to connect an external or internal middleware.
14. Structurally, external and internal middlewares do not differ from each other. The stage at which they will work 
    depends on how they are connected.
15. If you need to drop an update in middleware, you must either explicitly return None (simply return), or not execute the await handler(event, data) instruction at all (implicit return).
16. If you need to execute some code on exiting the middleware, then you should proceed as follows:
```bash
result = await handler(event, data)

# Here is some code that will be executed on exiting the middleware
# ...

return result
```
17. If you don't return result in middleware, the update processing will end at the current router and will not go to 
    middlewares, filters, or handlers of any other routers. Therefore, always explicitly specify return result to avoid 
    unexpected behavior.
18. If you don't return result in middleware, the update processing will end at the current router, and it won't reach 
    any middleware, filters, or handlers of any other routers. Therefore, always explicitly specify return result to 
    avoid unexpected behavior.
19. ### Most common tasks solved with middleware:
    - Fetching additional user data from the database for use in the subsequent processing chain (e.g., user role or 
      timezone).
    - Fetching a database connection from a connection pool so that subsequent objects in the chain can work with a 
      ready connection.
    - Shadow banning users. Bots don't have a direct way to ban users via Telegram, but updates from specific users can 
      be ignored at the earliest stage of processing.
    - Throttling. Slowing down the processing of updates from specific (or all) users.
    - Determining the language set by the user and preparing translations for that language in the context of
      multilingual bots.
    - Event logging.
    - Caching.
    - Timing measurements at different stages of the update processing.
20. If you need to execute some code before it's clear that the update will reach a handler, use external middleware. 
    If only when it's certain that the filters have been passed and there definitely is a handler, use internal 
    middleware.

## Project Structure:
```bash
📁 middleware_example_bot                   # Root directory of the project
 │
 ├── .env                                   # File with environment variables (secret data) for bot configuration.
 │
 ├── .env.example                           # File with example secrets for GitHub.
 │
 ├── .gitignore                             # File telling Git which files and directories to ignore.
 │
 ├── bot.py                                 # Main executable file - entry point to the bot.
 │
 ├── requirements.txt                       # File with project dependencies.
 │
 ├── logger_config.py                       # Logger configuration.
 │
 ├── README.md                              # File with project description.
 │
 ├── 📁 config_data/                        # Directory with the bot configuration module.
 │   ├── __init__.py                        # Package initializer file.
 │   └── config_data.py                     # Module for bot configuration.
 │
 ├── 📁 filters/                            # Package with custom filters.
 │   ├── __init__.py                        # Package initializer file.      
 │   └── filters.py                         # Module with filters we'll write for specific bot tasks.
 │ 
 ├── 📁 handlers/                           # Package with handlers.
 │   ├── __init__.py                        # Package initializer file.
 │   ├── user_handlers.py                   # Module with user handlers - main update handlers of the bot.
 │   └── other_handlers.py                  # Module with handlers for other user messages.
 │                                                 
 ├── 📁 middlewares/                        # Directory for storing middlewares.
 │   ├── __init__.py                        # Package initializer file.            
 │   ├── inner.py                           # Module for internal middlewares.
 │   └── outer.py                           # Module for external middlewares.
 │ 
 └── 📁 lexicon/                            # Directory for storing bot dictionaries.      
     ├── __init__.py                        # Package initializer file.                      
     └── lexicon.py                         # File with a dictionary mapping commands and queries to displayed texts.
```




# Наиболее типовые задачи, решаемые разработчиками ботов (да и не только ботов), с помощью миддлварей.

1. Обращение в базу данных для получения роли пользователя
    Часто бывает нужно классифицировать пользователей по каким-либо ролям, чтобы затем, в зависимости от этих ролей, 
    предоставлять пользователям разный функционал. Обычному пользователю только базовый функционал, пользователю, 
    который выполнил определенные условия или заплатил за изменение статуса - расширенный, админу - режим бога. Сами по 
    себе апдейты от пользователей никак нам не сообщают о роли пользователя в нашей системе. Такой учет мы можем 
    проводить только самостоятельно, изменяя статус пользователей, в зависимости от каких-либо условий. Но когда
    какой-то апдейт приходит, хотелось бы знать какая роль у пользователя, сгенерировавшего данный апдейт, чтобы 
    направить его по определенному для роли маршруту.

    Давайте подумаем на каком этапе нам хотелось бы знать, что за роль у пользователя. Начать надо с того, чтобы понять 
    где именно мы будем использовать знание о роли. Самое простое, что может прийти на ум - это фильтры на роутерах. То
    есть, можно создать определенный роутер под определенную роль и на этом роутере регистрировать хэндлеры, 
    обрабатывающие апдейты от пользователей с этой ролью. Соответственно, уже в фильтрах нам требуется знание о роли. А 
    значит, оптимальное место для определения роли - внешняя миддлварь.

2. Теневой бан
    Непосредственно у телеграм-ботов нет функционала, позволяющего банить пользователей так, чтобы пользователи не могли
    писать боту. Но такая необходимость бывает. Особенно это может быть актуально в групповых чатах. Сейчас появилось 
    много групп, в которых пользователи могут заказать какие-либо генерации картинок, музыки или текстов с помощью 
    искусственного интеллекта, такие боты "живут" в группах вместе с обычными пользователями и пользователи могут к ним 
    обращаться за генерациями. Обычно что-то сгенерировать с помощью нейросетей - это ресурсозатратный процесс и 
    администраторы таких ботов ограничивают пользователей каким-то количеством генераций в какой-то временной промежуток,
    чтобы с одной стороны, снизить нагрузку на вычислительные ресурсы, а с другой - дать более менее равные возможности 
    для генерации для всех участников группы. Соответственно, иногда требуется ограничивать пользователям доступ к 
    функционалу бота, а так как выше я говорил, что напрямую забанить пользователя нельзя, а чаще и просто не надо, 
    реализуется механизм так называемого теневого бана, когда бот просто игнорирует апдейты от пользователей с 
    определенным id. Здесь, как и в предыдущем пункте, важно понять, что апдейт не требует обработки на самом раннем 
    этапе, чтобы уменьшить количество действий с апдейтом. То есть нужна внешняя миддлварь на тип событий Update.

3. Передача коннекта к базе данных в фильтры и хэндлеры
    Одно из самых распространенных применений миддлварей в телеграм-ботах - это передача соединения с базой данных из 
    пула соединений в фильтры, хэндлеры и/или другие миддлвари. Или даже не просто соединения, а сразу экземпляра класса, 
    который обеспечивает доступ к базе данных с открытым уже соединением с помощью готовых методов. Если вашему боту 
    нужно работать с базой во внешних миддлварях или фильтрах - создание экземпляра класса нужно делать в одной из 
    внешних миддлварей, а если вашему боту не требуются получать какую-то информацию из базы данных до того, как апдейт 
    преодолел фильтры, то оптимальным местом создания экземпляра класса будет внутренняя миддлварь, когда мы уже точно 
    знаем, что фильтры пройдены и апдейт попадет в хэндлер, где работа с базой может понадобиться.

4. Определение языка пользователя для подготовки переводов
    Эта задача похожа на определение роли пользователя, потому что на раннем этапе обработки апдейта нужно выяснить 
    какой язык установлен у пользователя в настройках, чтобы отправлять ему тексты на соответствующем языке. 

5. Определение часового пояса пользователя
    Так же, как и с настройками языка, иногда имеют значение настройки часового пояса пользователя, чтобы, например, 
    настроить какое-либо оповещение в конкретное время или сделать рассылку хотя бы не тогда, когда у пользователя 
    глубокая ночь.

6. Логирование
    Можно использовать миддлвари для логирования определенных событий. Возможно, кто-то мог подумать, что можно ведь и в
    фильтрах логи писать и в хэндлерах, почему именно миддлвари? А чтобы не трогать код хэндлеров и фильтров. Бот 
    работает как надо, зачем нам влезать в уже рабочий код, чтобы что-то залогировать? Практически любую информацию 
    можно получить из апдейта, без необходимости логирования непосредственно в хэндлерах. Пишем миддлварь и одной 
    строчкой подключаем ее в нужном месте. Собираем нужные логи.

7. Замер времени выполнения для поиска узких мест
    С помощью миддлварей можно замерять производительность бота на разных участках, почти не трогая основной код. 
    Пишутся отдельные миддлвари с функционалом измерения времени и подключаются в нужных местах для сбора статистики и 
    отслеживания наиболее ресурсозатратных участков пайплайна с целью их оптимизировать.

8. Кеширование 
    Не всегда имеет смысл делать одинаковые запросы к какому-нибудь стороннему сервису или к базе данных каждый раз, 
    когда требуется информация от них. Иногда можно складывать ранее полученные результаты в кеш и читать их оттуда. С 
    помощью миддлварей удобно работать с кешем, экономя ресурсы бота.

9. Троттлинг
    Иногда не требуется полное игнорирование апдейтов конкретного пользователя, но хочется уменьшить пользователю 
    количество обращений к боту в единицу времени. Например, чтобы не позволять пользователю очень часто нажимать на 
    инлайн-кнопку или отправлять какую-нибудь команду.


## Пример 2. Теневой бан

Покажу как может выглядеть код миддлвари, реализующей теневой бан пользователя. Предполагается, что в базе данных мы
храним статус пользователя (забанен/не забанен), можем кешировать этот статус для пользователей, чтобы реже обращаться 
к базе, и на основании статуса принимать решение обрабатывать апдейты от пользователя или нет.

Так как в данном примере мы не хотим обрабатывать никакие апдейты от забаненных пользователей вообще, будем подключать 
миддлварь на корневой роутер (диспетчер) на тип событий Update.

Один из вариантов кода миддлвари для теневого бана может выглядеть следующим образом:
```bash
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

# Кэш заблокированных идентификаторов пользователей
CACHE = {
    'banned': [254443334, 214454432, 112221212],
}


class ShadowBanMiddleware(BaseMiddleware):
    """
        Промежуточное ПО для обработки теневой блокировки.

        Это промежуточное ПО проверяет, заблокирован ли пользователь, отправивший событие.
        Если заблокирован, оно прекращает дальнейшую обработку события.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
            Выполняет обработчик, проверяя наличие теневых блокировок.

            Args:
                handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): Обработчик события.
                event (TelegramObject): Объект события.
                data (Dict[str, Any]): Данные события.

            Returns:
                Any: Результат выполнения обработчика или None, если пользователь заблокирован.
        """
        # Получаем пользователя из данных события
        user: User = data.get('event_from_user')
        # Проверяем, заблокирован ли пользователь
        if user is not None:
            if user.id in CACHE.get('banned'):
                # Если заблокирован, прекращаем дальнейшую обработку события
                return

        # Продолжаем обработку события
        return await handler(event, data)
```
А подключение миддлвари происходит уже знакомым нам образом:
```bash
dp.update.middleware(ShadowBanMiddleware())
```
Здесь хочу обратить внимание, что словарь CACHE носит лишь демонстрационный характер и не должен храниться в том же 
модуле, что и миддлварь и, тем более, быть глобальной переменной. На практике кеш часто инициализируется в точке входа и
передается остальным объектам с помощью специального хранилища в диспетчере workflow_data.

## Пример 9. Троттлинг

Троттлинг (дословно "удушение") - снижение количества обрабатываемых запросов, относительно их общего количества. В 
примере предыдущего шага мы реализовали миддлварь, которая дропает вообще все апдейты от забаненных пользователей, но 
иногда нам нужно лишь дать понять пользователю, что если он будет слишком часто дергать бота, процесс не только не 
ускорится, но даже может замедлиться.

Тут нужно быть аккуратным, чтобы не вызывать у пользователей, корректно использующих бота, ощущения, что бот завис и 
больше не работает, потому еще надо продумать систему предупреждений. Но общий смысл работы троттлинг-миддлвари 
следующий. Берем какое-либо хранилище пар ключ-значение с возможностью установить время жизни ключа (Redis, NATS или 
даже просто TTLCache из библиотеки cachetools), при каждом апдейте от пользователя помещаем в хранилище его id (юзера, 
а не апдейта) и устанавливаем время жизни для такого ключа. В миддлвари проверяем наличие ключа, закрепленного за 
пользователем, чей апдейт пришел в данный момент. Если ключа нет - добавляем ключ в хранилище и пропускаем апдейт дальше
по цепочке обработки. А если ключ есть - просто дропаем апдейт. Хранилище само удалит ключ по истечении времени жизни 
этого ключа. Таким образом, будут обрабатываться не все апдейты пользователя, а только те, которые приходят не чаще 
определенного временного промежутка.
```bash
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

# Создание кэша с TTL (временем жизни) ключей
CACHE = TTLCache(maxsize=10_000, ttl=5)  # Максимальный размер кэша - 10000 ключей, а время жизни ключа - 5 секунд

class ThrottlingMiddleware(BaseMiddleware):
    """
        Промежуточное ПО для ограничения скорости.

        Это промежуточное ПО предотвращает повторное выполнение обработчика
        события, если оно вызывается слишком часто.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
            Выполняет обработчик события с учетом ограничения скорости.

            Args:
                handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): Обработчик события.
                event (TelegramObject): Объект события.
                data (Dict[str, Any]): Данные события.

            Returns:
                Any: Результат выполнения обработчика или None, если событие выполняется слишком часто.
        """
        # Получаем пользователя из данных события
        user: User = data.get('event_from_user')

        # Проверяем, было ли уже событие обработано
        if user.id in CACHE:
            return

        # Устанавливаем метку обработки события в кэше
        CACHE[user.id] = True

        # Выполняем обработчик события
        return await handler(event, data)
```
Зарегистрировать миддлварь также нужно на диспетчер, если вы хотите замедлять любые действия пользователя или на 
конкретный роутер, если хотите замедлить обработку в рамках хэндлеров конкретного роутера.

```bash
dp.update.middleware(ThrottlingMiddleware())
```
Ну, и если будете экспериментировать с предложенным способом - не забудьте установить библиотеку cachetools:
```bash
pip install cachetools
```

Теперь на каждое действие пользователя будет добавляться ключ с его id в кеш, если такого ключа там еще не было, а если
ключ был - то будет дропаться апдейт от этого пользователя. 

## Пример. Инъекция зависимостей

Eсли какой-то объект создается у вас в проекте один раз (например, объект класса Config, или пул соединений с базой 
данных, или какие-то API-токены для внешних сервисов), то их можно передать без использования миддлварей. Достаточно в 
main-файле положить эти объекты в специальное хранилище workflow_data, доступ к которому можно получить через диспетчер. 

### Хранилище workflow_data
У диспетчера реализовано специальное хранилище *workflow_data*, которое работает как обыкновенный словарь, а значит, 
можно через него передавать данные, общие для всего проекта, в том числе и какие-то конфигурационные данные из точки 
входа. 
Работает так:
```bash
from aiogram import Bot, Dispatcher

# ...

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()

some_var_1 = 1
some_var_2 = 'Some text'

dp.workflow_data.update({'my_int_var': some_var_1, 'my_text_var': some_var_2})

# либо так
dp['my_int_var'] = some_var_1
dp['my_text_var'] = some_var_2

# ...
```
Ну, и где-нибудь в хэндлерах мы можем напрямую указывать соответствующие ключи в сигнатуре хэндлера:
```bash
@router.message(CommandStart())
async def process_start_command(message: Message, my_int_var, my_text_var):
    await message.answer(text=str(my_int_var))
    await message.answer(text=my_text_var)
```
В сигнатуре хэндлера мы просто указываем аргументы, которые совпадают по названию с ключами словаря, который мы 
клали в модуле main.py в словарь dp.workflow_data и теперь внутри хэндлера нам будут доступны значения по этим 
ключам.

Но если вам нужно передать данные, которых у вас еще нет на момент старта бота или которые могут динамически меняться в 
процессе, миддлвари станут удобным инструментом. 

#### Вот пример как можно подкладывать в миддлвари словарь сразу с нужным языком, чтобы он был доступен в хэндлерах.
Итак общий принцип. У нас в проекте есть модули со словарями, в которых хранятся пары ключ-значение. Ключи - это 
идентификаторы переводов, а значения - сами переводы. Это понятно. Ключи во всех словарях одинаковые, а значения зависят
от языка, для которого подготовлен словарь. В миддлвари мы можем получить язык пользователя (из апдейта или из базы 
данных, не важно) и положить по ключу 'i18n' - так часто называется объект, отвечающий за интернационализацию, тот 
словарь, в котором хранятся тексты на языке пользователя. После этого в хэндлерах нам станет доступна ссылка на нужный 
словарь. 

Допустим в пакете lexicon у нас лежат два модуля lexicon_ru.py и lexicon_en.py, внутри которых словари одинаковой 
структуры, но с текстами на разных языках. Вот пример:

1) 📁 lexicon/lexicon_ru.py
```bash
LEXICON_RU: dict[str, str] = {
    '/start': 'Привет!\n\nЯ эхо-бот для демонстрации работы миддлварей!\n\n'
              'Если хотите - можете мне что-нибудь прислать',
    'no_echo': 'Данный тип апдейтов не поддерживается '
               'методом send_copy',
    'button': 'Кнопка',
    'button_pressed': 'Вы нажали кнопку!'
}
```
2) 📁 lexicon/lexicon_en.py
```bash
LEXICON_EN: dict[str, str] = {
    '/start': "Hello!\n\nI'm an echo bot to demonstrate how middleware works!\n\n"
              "If you want, you can send me something",
    'no_echo': 'This type of update is not supported by the send_copy method',
    'button': 'Button',
    'button_pressed': "You've pressed the button!"
}
```
3) В точке входа main.py мы можем собрать все переводы в один словарь и передать его при старте поллинга с помощью 
диспетчера: (main.py)
```bash
from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU

# ...

# Словарь для хранения переводов
translations = {
    'default': 'ru',  # Установка языка по умолчанию
    'en': LEXICON_EN,  # Английский лексикон
    'ru': LEXICON_RU,  # Русский лексикон
}

async def main():

# ...

# Начало опроса ботом с передачей словаря переводов
await dp.start_polling(bot, _translations=translations)
```
4) Ну, и нам понадобится миддлварь, которая будет определять язык пользователя и подкладывать нужный перевод. 
   Храниться она будет в пакете с миддлварями в модуле i18n.py. (📁 middlewares/i18n.py)
```bash
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User

class TranslatorMiddleware(BaseMiddleware):
    """
        Middleware для перевода текста в зависимости от языка пользователя.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]):
                Обработчик событий.
            event (TelegramObject):
                Событие, источник запроса.
            data (Dict[str, Any]):
                Данные запроса.

        Returns:
            Any: Результат выполнения обработчика.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],  # Обработчик событий
        event: TelegramObject,  # Событие
        data: Dict[str, Any]    # Данные
    ) -> Any:
        """
           Вызов миддлвари.

           Args:
               handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]):
                   Обработчик событий.
               event (TelegramObject):
                   Событие, источник запроса.
               data (Dict[str, Any]):
                   Данные запроса.

           Returns:
               Any: Результат выполнения обработчика.
        """
        # Получение пользователя из данных события
        user: User = data.get('event_from_user')

        # Если пользователя нет, пропускаем обработчик
        if user is None:
            return await handler(event, data)

        user_lang = user.language_code            # Получаем язык пользователя
        translations = data.get('_translations')  # Получаем словарь переводов

        i18n = translations.get(user_lang)        # Получаем переводы для языка пользователя

        # Если переводов нет для указанного языка
        if i18n is None:
            # Берем переводы по умолчанию
            data['i18n'] = translations[translations['default']]
        else:
            # Используем переводы для указанного языка
            data['i18n'] = i18n

        # Пропускаем обработчик с обновленными данными
        return await handler(event, data)
```
5) Теперь, когда мы зарегистрируем миддлварь в функции main модуля main.py:
```bash
from middlewares.i18n import TranslatorMiddleware

# ...

async def main():
    
    # ...
    # Здесь будем регистрировать миддлвари
    dp.update.middleware(TranslatorMiddleware())
```
6) В хэндлерах появится доступ к словарю с переводом для конкретного языка пользователя, апдейт которого мы в 
   текущий момент хотим обработать в хэндлере. Вот пример хэндлера на команду \start:
```bash
# Этот хэндлер срабатывает на команду /start и поддерживает 2 языка (русский и английский).
@user_router.message(CommandStart(), MyTrueFilter())
async def process_start_command(message: Message, i18n: dict[str, str]) -> None:
    """
        Обработчик команды /start.
    
        Args:
            message (Message):
                Объект сообщения.
            i18n (dict[str, str]):
                Словарь с переводами.
    
        Returns:
            None
    """
    # Создаем объект инлайн-кнопки
    button = InlineKeyboardButton(
        text=i18n.get('button'),        # Текст кнопки
        callback_data='button_pressed'  # Данные обратного вызова
    )
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Отправляем сообщение пользователю
    await message.answer(text=i18n.get('/start'), reply_markup=markup)
```

# Важные моменты Middleware:

1. Middleware - это промежуточное программное обеспечение, которое может встраиваться в основной процесс работы сервиса 
   с целью модификации или обогащения данных, валидации их, отклонения дальнейшей их обработки и так далее.

2. В aiogram миддлвари делятся на внешние и внутренние. Внешние начинают работать до попадания апдейта в фильтры, а 
   внутренние после выхода из фильтров перед попаданием в хэндлер.

3. Каждую миддлварь можно настроить так, чтобы выполнялся какой-то код на входе в миддлварь и на выходе из нее.

4. В любой миддлвари можно дропнуть апдейт, остановив его дальнейшее движение по цепочке обоработки.

5. Миддлвари подключаются к роутерам на определенные типы событий.

6. Миддлвари могут быть реализованы как классы и как функции.

7. Каждая миддлварь, реализованная на базе класса, должна наследоваться от BaseMiddleware и содержать имплементацию 
   метода __call__.

8. Метод __call__ помимо ссылки на экземпляр класса, принимает 3 обязательных аргумента:
    ```bash
    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: TelegramObject,
    data: Dict[str, Any].
    ```
9. Конструкция подключения миддлвари-класса выглядит следующим образом:
    ```bash
    <имя_роутера>.<тип_события>.<тип_миддлвари>(<имя_миддлвари>())
    ```
10. Конструкция подключения миддлвари-функции отличается тем, что не нужно писать оператор вызова после имени миддлвари:
    ```bash
    <имя_роутера>.<тип_события>.<тип_миддлвари>(<имя_миддлвари>)
    ```
    Но удобнее регистрировать миддлвари-функции с помощью декораторов в тех же модулях, где проиницилизированы роутеры,
    на которые навешиваются миддлвари.

11. Миддлвари как функции удобно использовать на уровне отдельного модуля для небольших задач.

12. Если нужна миддлварь, в которую будут попадать вообще все апдейты - ее надо подключать к диспетчеру на тип событий 
    Update. При этом нет разницы между тем подключить эту миддлварь как внешнюю или как внутреннюю.

13. Такой разницы подключения нет только для события Update, для остальных типов событий надо хорошо понимать внешнюю 
    миддлварь вы хотите подключить или внутреннюю.

14. Структурно внешние и внутренние миддлвари не отличаются друг от друга. На каком этапе они будут работать зависит от 
    способа их подключения.

15. Если в миддлвари требуется пропустить апдейт дальше по цепочке обработки, то обязательно должна быть конструкция 
    await handler(event, data), причем, если вам требуется выполнение кода в миддлвари только до передачи апдейта дальше
    по цепочке - return можно сделать сразу:
    ```bash
    return await handler(event, data)
    ```
16. А если вам требуется еще какой-то код на выходе из миддлвари, тогда следует поступить так:
    ```bash
    result = await handler(event, data)
    
    # Здесь какой-то код, который будет выполняться на выходе из миддлвари
    # ...
    
    return result
    ```
17. Если требуется дропнуть апдейт в миддлвари, то необходимо до инструкции await handler(event, data) либо сделать 
    явный return None (просто return), либо не выполнять инструкцию await handler(event, data) вообще (неявный return).

18. Если в миддлвари не сделать return result, обработка апдейта закончится на текущем роутере и не попадет ни в 
    миддлвари, ни в фильтры, ни в хэндлеры любых других роутеров. Поэтому всегда явно прописывайте return result, чтобы 
    избежать неожиданного поведения.

19. ### Наиболее частые задачи, решаемые с помощью миддлварей:
- Получение дополнительных данных о пользователе из БД для использования их в дальнейшей цепочке обработки (например, 
  роль пользователя или его часовой пояс).
- Получение соединения с базой данных из пула соединений, чтобы в объектах дальнейшей цепочки можно было работать с 
  готовым соединением.
- Теневой бан пользователей. У ботов нет прямой возможности забанить пользователя средствами Telegram, но можно 
  игнорировать апдейты от конкретных пользователей на самой ранней стадии обработки.
- Троттлинг. Замедление обработки апдейтов конкретных (или всех) пользователей.
- Определение языка, установленного у пользователя, и подготовка переводов для этого языка в рамках мультиязычных ботов.
- Логирование событий.
- Кеширование.
- Замеры времени на разных участках процесса обработки апдейта.
20. Если вам требуется выполнение какого-то кода еще до того, как стало понятно, что апдейт попадет в хэндлер - 
    используйте внешние миддлвари, а если только в том случае, когда фильтры уже пройдены и дальше точно есть хэндлер -
    внутренние.


## Структура проекта:
```bash
📁 middleware_example_bot                   # Корневая директория всего проекта
 │
 ├── .env                                   # Файл с переменными окружения (секретными данными) для конфигурации бота.
 │
 ├── .env.example                           # Файл с примерами секретов для GitHub
 │
 ├── .gitignore                             # Файл, сообщающий гиту какие файлы и директории не отслеживать
 │
 ├── bot.py                                 # Основной исполняемый файл - точка входа в бот
 │
 ├── requirements.txt                       # Файл с зависимостями проекта.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта.
 │
 ├── 📁 config_data/                        # Директория с модулем конфигурации бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета. 
 │   └── config_data.py                     # Модуль для конфигурации бота.
 │
 ├── 📁 filters/                            # Пакет с пользовательскими фильтрами.
 │   ├── __init__.py                        # Файл-инициализатор пакета.      
 │   └── filters.py                         # Модуль с фильтрами, которые мы напишем для конкретных задач бота.
 │ 
 ├── 📁 handlers/                           # Пакет с обработчиками.
 │   ├── __init__.py                        # Файл-инициализатор пакета.
 │   ├── user_handlers.py                   # Модуль с обработчиками пользователя. Основные обработчики обновлений бота.
 │   └── other_handlers.py                  # Модуль с обработчиком остальных сообщений пользователя.
 │                                                 
 ├── 📁 middlewares/                        # Директория для хранения миддлварей.
 │   ├── __init__.py                        # Файл-инициализатор пакета.            
 │   ├── inner.py                           # Модуль для внутренних миддлварей.
 │   └── outer.py                           # Модуль для внешних миддлварей.
 │ 
 └── 📁 lexicon/                            # Директория для хранения словарей бота.      
     ├── __init__.py                        # Файл-инициализатор пакета.                      
     └── lexicon.py                         # Файл со словарем соответствий команд и запросов отображаемым текстам.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus