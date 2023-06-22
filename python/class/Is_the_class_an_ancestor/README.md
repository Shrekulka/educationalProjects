Is the class an ancestor

You are given a description of class inheritance in the following format.
<class name 1> : <class name 2> <class name 3> ... <class name k>
This means that class 1 inherits from class 2, class 3, etc.

Or equivalent to writing:
class Class1(Class2, Class3 ... ClassK):
    pass
Class A is the direct ancestor of class B if B is inherited from A:

class B(A):
    pass

A is the direct ancestor of class B if

- A = B;
- A is a direct ancestor of B
- there exists a class C such that C is a direct ancestor of B and A is an ancestor of C

For example:
```
class B(A):
    pass

 class C(B):
    pass

A is an ancestor of C
```
You need to answer queries about whether one class is the ancestor of another class

Important note:
There is no need to create classes.
We ask you to simulate this process and understand if there is a path from one class to another.

The format of the input data
The first line of input contains an integer n - the number of classes.
The next n lines contain description of class inheritance. The i-th line specifies from which classes the i-th class
is inherited from. Note that the class may not inherit from anyone. It is guaranteed that the class does not inherit 
from itself (directly or indirectly), that a class is not explicitly inherited from a class more than once.
The next line contains number q - the number of queries.
The following q lines contain a description of queries in the format <class name 1> <class name 2>.
Class name is a string of Latin characters, maximum length 50.
Output format
For each query, print on a separate line the word "Yes" if class 1 is the ancestor of class 2, and "No" if it is not.
```
Sample Input:
4
A
B : A
C : A
D : B C
4
A B
B D
C D
D A

Sample Output:
Yes
Yes
Yes
No
```




Является ли класс предком

Вам дано описание наследования классов в следующем формате.
<имя класса 1> : <имя класса 2> <имя класса 3> ... <имя класса k>
Это означает, что класс 1 унаследован от класса 2, класса 3, и т. д.

Или эквивалентно записи:
class Class1(Class2, Class3 ... ClassK):
    pass
Класс A является прямым предком класса B, если B унаследован от A:

class B(A):
    pass

Класс A является предком класса B, если

•	A = B;
•	A - прямой предок B
•	существует такой класс C, что C - прямой предок B и A - предок C

Например:
```
class B(A):
    pass

class C(B):
    pass

A -- предок С
```
Вам необходимо отвечать на запросы, является ли один класс предком другого класса

Важное примечание:
Создавать классы не требуется.
Мы просим вас промоделировать этот процесс, и понять существует ли путь от одного класса до другого.

Формат входных данных
В первой строке входных данных содержится целое число n - число классов.
В следующих n строках содержится описание наследования классов. В i-й строке указано от каких классов наследуется i-й
класс. Обратите внимание, что класс может ни от кого не наследоваться. Гарантируется, что класс не наследуется сам от
себя (прямо или косвенно), что класс не наследуется явно от одного класса более одного раза.
В следующей строке содержится число q - количество запросов.
В следующих q строках содержится описание запросов в формате <имя класса 1> <имя класса 2>.
Имя класса – строка, состоящая из символов латинского алфавита, длины не более 50.
Формат выходных данных
Для каждого запроса выведите в отдельной строке слово "Yes", если класс 1 является предком класса 2, и "No", если не
является.
```
Sample Input:
4
A
B : A
C : A
D : B C
4
A B
B D
C D
D A

Sample Output:
Yes
Yes
Yes
No
```