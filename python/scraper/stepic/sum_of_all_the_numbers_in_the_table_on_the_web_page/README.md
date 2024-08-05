###Task:
The file https://stepik.org/media/attachments/lesson/209723/3.html contains one table. Add up all the numbers in it 
and enter one number as the answer - this sum. Use BeautifulSoup's features to access the cells.

When the code runs, it sends a request to the web page represented by the URL 
"https://stepik.org/media/attachments/lesson/209723/3.html".
If the request is successful and the page is accessible (code status is 200), the code starts analysing the contents of 
the HTML page.
It looks for all cells (<td>) in the table and extracts numbers from each cell.
The numbers are added to the numbers_in_table list.
Once all the numbers have been extracted, the programme calculates their sum using the sum() function and stores the 
result in the total_sum variable.
Finally, the programme displays the obtained sum on the screen.

If the page contains only one table with numbers, the result of the programme will be a single number - the sum of all
numbers in this table. If there are other elements on the page that are not tables or numbers, they will be ignored, and
the programme will only calculate the sum of the numbers in the table.





