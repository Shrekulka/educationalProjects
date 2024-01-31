# Агрегация и группировка записей 

## Агрегирующие функции в команде SELECT:

1. count - это агрегатная функция языка SQL, которая используется для подсчета количества строк, удовлетворяющих 
   определенному условию в запросе SELECT.

   Ключевое слово ***DISTINCT*** используется в языке SQL в контексте оператора SELECT для получения уникальных значений 
   в определенном столбце или наборе столбцов. Когда вы используете DISTINCT в запросе, система удаляет повторяющиеся 
   строки и возвращает только уникальные значения.

   #### Примеры:
   ```bash
   # Выполняем подсчет количества пользователей с мужским полом в таблице "users"
   result = cur.execute("SELECT count(user_id) FROM users WHERE  gender = 'Male'")
   print(f"Found {result.fetchone()[0]} male in the table")
   
   # Выполняем подсчет уникальных значений возраста в таблице "users"
   result = cur.execute("SELECT count(DISTINCT age) FROM users")
   print(f"\n{Fore.GREEN}Found {result.fetchone()[0]} unique ages in the table{Style.RESET_ALL}\n")
   ```
   
2. sum() - подсчет суммы указанного поля по всем записям выборки.
   #### Примеры:
   ```bash
   # Выполняем подсчет суммы баллов для пользователей с женским полом в таблице "users"
   result = cur.execute("SELECT sum(score) FROM users WHERE gender = 'Female'")
   print(f"{Fore.GREEN}Total score for females: {result.fetchone()[0]}{Style.RESET_ALL}")
   ```
   
3. avr() - вычисление среднего арифметического указанного поля.
   ```bash
   # Выполняем запрос для вычисления среднего значения возраста пользователей в таблице "users"
   result_avg_age = cur.execute("SELECT avg(age) FROM users")
   print(f"\n{Fore.GREEN}Average age in the table: {result_avg_age.fetchone()[0]:.2f}{Style.RESET_ALL}\n")
   ```

4. min() - нахождение минимального значения для указанного поля.
   ```bash
   # Выполняем запрос для выбора минимального значения возраста из таблицы "users"
   result_min_age = cur.execute("SELECT min(age) FROM users")
   print(f"{Fore.GREEN}Minimum age in the table: {result_min_age.fetchone()[0]}{Style.RESET_ALL}")
   ```
   
5. max() - нахождение максимального значения для указанного поля.
   ```bash
   # Выполняем запрос для выбора максимального значения баллов из таблицы "users"
   result_max_score = cur.execute("SELECT max(score) FROM users")
   print(f"{Fore.GREEN}Maximum score in the table: {result_max_score.fetchone()[0]}{Style.RESET_ALL}")
   ```
   
## Группировка записей
GROUP BY <name_column>

 #### Примеры:
   ```bash
   # Выполняем запрос для выбора суммы баллов сгруппированных по полу в таблице "user
   result_gender_score_sum = cur.execute("SELECT gender, sum(score) FROM users GROUP BY gender")  
   # Используем цикл for для обработки каждой строки результата                      
   for row in result_gender_score_sum.fetchall():                                    
      gender, total_score = row                                                     
      print(f"{Fore.GREEN}Total score for {gender}: {total_score}{Style.RESET_ALL}")
      
    # Выполняем запрос для выбора суммы баллов сгруппированных по полу в таблице "users", а затем используем
    # вложенный запрос с дополнительным GROUP BY sum для группировки результатов по уникальной сумме баллов
    result_gender_score_sum = cur.execute("SELECT gender, sum FROM (SELECT gender, SUM(score) "
                                          "AS sum FROM users GROUP BY gender) GROUP BY sum")
    # Используем цикл for для обработки каждой строки результата
    for row in result_gender_score_sum.fetchall():
        gender, total_score = row
        print(f"{Fore.GREEN}Total score for {gender}: {total_score}{Style.RESET_ALL}")
   ```