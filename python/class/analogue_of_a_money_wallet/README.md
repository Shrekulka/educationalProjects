Implement a Wallet class, analogous to a money wallet, containing information about the currency and balance of the 
available funds in the account. This class should implement:
- The _init_ method, which creates the currency and balance attributes. The values of the currency and balance 
  attributes come when calling the _init_ method is called. The value of the currency attribute must be a string of only
  three capital letters. To it is necessary to make the following checks in this sequence
- In case when not a string is passed, Exception TureError should be thrown with text "Invalid currency type":
- In the case where a string whose length is not equal to three characters is passed, it is necessary to raise a 
  NameError exception with the text with the text "Invalid currency name length".
- If a string of three characters consists of non-capital letters, raise a ValueError exception with the text
  "The name should only consist of uppercase letters".
- The _eq_ method to be able to compare wallet balances. Comparison operation is only available for wallets with
  same currency. If the currencies differ, a ValueError exception should be thrown, saying "Can't compare
  different currencies". If you try to compare a Wallet instance with other objects, then you need to throw exception
  ValueError exception with the text "Wallet doesn't support comparison to an 'object'";
- The _add_ and _sub_ methods to add and subtract wallets. We can only add and subtract with
  another instance of the Wallet class and only if they have the same currency (currency attributes). The result
  of such addition must be a new instance of Wallet class, whose currency coincides with the currency of the operands 
  and the balance is equal to the sum/subtraction of their balances. If an attempt is made to add with an object which 
  is not a Wallet instance or if the currency values do not match, it is necessary to raise ValueError exception with 
  text "This operation is not allowed

wallet1 = Wallet ('USD', 50)
wallet2 = Wallet('UAH', 100)
wallet3 = Wallet ('UAH', 150)
wallet4 = Wallet ('12, 150) # Exception TureError("Invalid currency type")
wallet5 = Wallet('qwerty', 150) # Exception NameError ('Invalid currency name length')
wallet6 = Wallet ('abc', 150) # valueError exception ("The name must be in uppercase letters only")
print (wallet2 == wallet3) # False
print (wallet2 == 100) # TypeError ("wallet does not support comparison to 100")
print (wallet2 == wallet1) # ValueError ("Different currencies cannot be compared")
wallet7 = wallet2 + wallet3
print (wallet7.currency, wallet7.balance) # print 'UAH 250
wallet2 + 45 # ValueError ("This operation is not allowed")




Реализуйте класс Wallet, аналог денежного кошелька, содержащий информацию о валюте и остатке имеющихся средств на
счете. В данном классе должны быть реализованы:
• метод _init_, который создает атрибуты currency и balance. Значения атрибутов currency и balance поступают при вызове
  метода _init_. При этом значение атрибута currency должно быть строкой, состоящей только из трех заглавных букв. Для
  этого необходимо сделать именно в такой последовательности следующие проверки
• В случае, если передается не строка, нужно возбуждать исключение ТуреЕrror с текстом "Неверный тип валюты":
• В случае, если передается строка, длина которой не равна трем символам, нужно возбуждать исключение NameError с
  текстом "Неверная длина названия валюты"
• В случае, если строка из трех символов состоит из незаглавных букв, нужно возбуждать исключение ValueError с текстом
  "Название должно состоять только из заглавных букв"
• метод _eq_ для возможности сравнивания балансов кошельков. Операция сравнения доступна только для кошельков с
  одинаковой валютой. Если валюты различаются, необходимо возбудить исключение ValueError с текстом "Нельзя сравнить
  разные валюты". При попытке сравнить экземпляр класса Wallet с другими объектами необходимо возбудить исключение
  ТуреЕrror с текстом "Wallet не поддерживает сравнение с «объектом»";
• методы _add_ и _sub_ для возможности суммирования и вычитания кошельков. Складывать и вычитать мы можем только с
  другим экземпляром класса Wallet и только в случае, когда у них совпадает валюта (атрибуты currency). Результатом
  такого сложения должен быть новый экземпляр класса Wallet, у которого валюта совпадает с валютой операндов и значение
  баланса равно сумме/вычитанию их балансов. Если попытаются сложить с объектом не являющимся экземпляром Wallet или
  значения валют у объектов не совпадают, необходимо возбудить исключение ValueError с текстом "Данная операция запрещена"

wallet1 = Wallet ('USD', 50)
wallet2 = Wallet('UAH', 100)
wallet3 = Wallet ('UAH', 150)
wallet4 = Wallet (12, 150) # исключение ТуреЕrror("Неверный тип валюты")
wallet5 = Wallet('qwerty', 150) # исключение NameError ("Неверная длина названия валюты")
wallet6 = Wallet ('abc', 150) # исключение ValueError ("Название должно состоять только из заглавных букв")
print (wallet2 == wallet3) # False
print (wallet2 == 100) # TypeError ("Wallet не поддерживает сравнение с 100")
print (wallet2 == wallet1) # ValueError ("Нельзя сравнить разные валюты")
wallet7 = wallet2 + wallet3
print (wallet7.currency, wallet7.balance) #печатает 'UAH 250'
wallet2 + 45 # ValueError ("Данная операция запрещена")