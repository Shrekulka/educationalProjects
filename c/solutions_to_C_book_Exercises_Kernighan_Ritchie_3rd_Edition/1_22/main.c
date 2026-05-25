#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define LINE_WIDTH 5
#define MAX_WORD_LENGTH 10

int column = 0; // Глобальная переменная для отслеживания позиции в строке.
int last_space = 0; // Глобальная переменная для отслеживания последнего пробела.
int last_non_space = 0; // Глобальная переменная для отслеживания последнего символа-разделителя.
char prev_char = ' '; // Глобальная переменная для отслеживания предыдущего символа.

const char* abbreviations[] = {
		"Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "Rev.", "Fr.", "Sr.", "Jr.",
		"Capt.", "Col.", "Maj.", "Adm.", "Cmdr.", "Lt.", "Mt.", "Ft.",
		"Ave.", "Blvd.", "Rd.", "St.", "Mon.", "Tue.", "Wed.", "Thu.",
		"Fri.", "Sat.", "Sun.", "Jan.", "Feb.", "Mar.", "Apr.", "Jun.",
		"Jul.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec.", "lbs.", "in.",
		"ft.", "yd.", "pk.", "al.", "etc.", "e.g.", "i.e.", "ca.", "cf.",
		"ibid.", "viz.", "et al.", "c.", "approx.", "am", "pm", "ASAP",
		"PS", "RSVP", "AKA", "AWOL", "FAQ", "ASAP", "VIP", "IOU", "MIA",
		"POW", "RADAR", "SONAR", "LASER", "NATO", "UNESCO", "VAT", "HIV",
		"DNA", "GDP", "CEO", "CFO"
};

bool isVowel(char ch)
{
	ch = tolower(ch);
	return (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u');
}

bool isAlphabet(char ch)
{
	return isalpha(ch);
}

bool isConsonant(char ch)
{
	ch = tolower(ch);
	return (isAlphabet(ch) && !isVowel(ch));
}

bool isPreposition(char ch, char prev, char next)
{
	char prepositions[] = "aeiou";
	ch = tolower(ch);
	for (int i = 0; prepositions[i] != '\0'; i++)
	{
		if (ch == prepositions[i] && (prev == ' ' || prev == '\t') && (next == ' ' || next == '\t'))
			return true;
	}
	return false;
}

char peekNextChar()
{
	int next = getchar();
	ungetc(next, stdin);
	return (char)next;
}

void handleSpace()
{
	for (int i = 0; i <= last_space; i++)
	{
		putchar(' ');
		column++;
	}
	putchar('\n');
	column = 0;
	last_space = 0;
	last_non_space = 0;
}

void handleCharacter(char character)
{
	if (column >= LINE_WIDTH)
	{
		if (isVowel(character) && isConsonant(prev_char))
		{
			putchar('-');
			putchar('\n');
			column = 0;
			last_space = 0;
			last_non_space = 0;
		}
	}
	else if (character == '\n')
	{
		putchar(character);
		column = 0;
		last_space = 0;
		last_non_space = 0;
	}
	else
	{
		putchar(character);
		column++;
		if (character == ' ' || character == '\t')
		{
			last_space = column - 1;
		}
		else
		{
			last_non_space = column - 1;
		}

		// Перенос слов, которые не помещаются в заданной ширине строки
		if (column >= LINE_WIDTH)
		{
			int space_index = last_space;
			if (space_index == 0)
			{
				space_index = last_non_space;
			}
			if (space_index != 0 || character == '-')
			{
				putchar('-');
				putchar('\n');
				column = 0;
				last_space = 0;
				last_non_space = space_index;
			}
			else
			{
				// Разрываем слово по гласным буквам
				int current_index = last_non_space;
				int syllables = 0;
				while (current_index >= 0)
				{
					if (isVowel(prev_char))
					{
						syllables++;
					}
					if (column + syllables > LINE_WIDTH)
					{
						break;
					}
					current_index--;
					prev_char = character;
					character = getchar();
					if (current_index < 0 || character == ' ' || character == '\t' || character == '\n' ||
						character == '-')
					{
						break;
					}
					putchar(character);
					column++;
				}
				if (syllables >= 2)
				{
					putchar('-');
					putchar('\n');
					column = 0;
				}
				else if (character == '-' && isVowel(peekNextChar()))
				{
					putchar('-');
				}
				last_space = 0;
				last_non_space = current_index;
			}
		}
	}
}


bool isAbbreviationWords(char ch, char prev, char next)
{
	if (ch == '.' && isalpha(prev))
	{
		char word[MAX_WORD_LENGTH + 1];
		int i = 0;
		word[i++] = prev;
		word[i++] = ch;
		word[i] = '\0';

		for (int i = 0; i < sizeof(abbreviations) / sizeof(abbreviations[0]); i++)
		{
			if (strcmp(word, abbreviations[i]) == 0)
			{
				return true;
			}
		}
	}
	return false;
}

int main()
{
	int character;
	while ((character = getchar()) != EOF)
	{
		if (character == 'q') break;

		if (character == ' ' || character == '\t')
		{
			handleSpace();
		}
		else if (isAlphabet(character))
		{
			char current = character;
			char next = peekNextChar();

			if (isConsonant(current) && isConsonant(next) && column == last_non_space + 1)
			{
				handleCharacter(current);
			}
			else if (!isPreposition(current, prev_char, next))
			{
				handleCharacter(current);
			}
			else if (isAbbreviationWords(current, prev_char, next))
			{
				// Обработка сокращения
			}

			prev_char = current;
		}
		else
		{
			handleCharacter(character);
		}
	}

	return 0;
}
