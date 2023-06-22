You are given a description of a pyramid of cubes in XML format.
Cubes can be of three colors: red (red), green (green) and blue (blue).
For each cube, its color is known, and the cubes located directly below it are known.

Example:
```xml
<cube color="blue">
  <cube color="red">
    <cube color="green">
    </cube>
  </cube>
  <cube color="red">
  </cube>
</cube>
```
Let us introduce the concept of value for cubes. The topmost cube corresponding to the root of the XML document has a 
value of 1. The cubes, immediately below it have a value of 2. Dice directly below the underlying dice have a value of 3.
Etc.

The value of a color is equal to the sum of the values of all the cubes of that color.

Output three numbers separated by a space: the values of red, green and blue colors.
sample input:

<cube color="blue"><cube color="red"><cube color="green"></cube></cube><cube color="red"></cube></cube>

sample output:
4 3 1




Вам дано описание пирамиды из кубиков в формате XML.
Кубики могут быть трех цветов: красный (red), зеленый (green) и синий (blue).
Для каждого кубика известны его цвет, и известны кубики, расположенные прямо под ним.

Пример:
```xml
<cube color="blue">
  <cube color="red">
    <cube color="green">
    </cube>
  </cube>
  <cube color="red">
  </cube>
</cube>
```
Введем понятие ценности для кубиков. Самый верхний кубик, соответствующий корню XML документа имеет ценность 1. Кубики, 
расположенные прямо под ним, имеют ценность 2. Кубики, расположенные прямо под нижележащими кубиками, имеют ценность 3. 
И т. д.

Ценность цвета равна сумме ценностей всех кубиков этого цвета.

Выведите через пробел три числа: ценности красного, зеленого и синего цветов.
Sample Input:

<cube color="blue"><cube color="red"><cube color="green"></cube></cube><cube color="red"></cube></cube>

Sample Output:
4 3 1