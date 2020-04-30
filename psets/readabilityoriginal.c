#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>


int main(void)
{

    string text = get_string("Enter text: \n"); // Get input from the user
    int l = strlen(text);  // Denote the length of the user's string


    int letters, digits, other, words, sentences, i;
    letters = digits = other = words = sentences = i = 0;

    while ((text[i] != '\0')) // checking to see which characters are letters, digits, or other
    {
        if ((text[i]) >= 'A' && (text[i]) <= 'Z') // Count any capital letters
        {
            letters ++;
        }
        else if ((text[i]) >= 'a' && (text[i]) <= 'z') // Count any lower case letters
        {
            letters ++;
        }
        else if ((text[i]) >= '0' && (text[i]) <= '9') // Count (ignore) digits
        {
            digits ++;
        }
        else // Count (ignore) spaces, punctuation, and other special characters
        {
            other ++;
        }

        i++;

    }


    for (i = 0; text[i] != '\0'; i++) // Counting the number of words by detecting spaces
    {
        if ((text[i]) == ' ' && (text[i + 1]) != ' ')
        {
            words ++;
        }
    }


    for (i = 0; text[i] != '\0'; i++) // Counting the number of sentences by detecting punctuation
    {
        if ((text[i]) == '.' || (text[i]) == '!' || (text[i]) == '?')
        {
            sentences ++;
        }

    }


    float L = (letters * 100) / (words + 1);
    float S = (sentences * 100) / (words + 1);


    float CLI = (0.0588 * L) - (0.296 * S) - 15.8;


    int grade = nearbyintf(CLI);

    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

}
