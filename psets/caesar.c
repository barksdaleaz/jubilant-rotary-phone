#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[])
{

    if (argc != 2) // check if there is an argument on the command line or not
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int i, digits;
    i = digits = 0;

    while ((argv[1][i]) != '\0')
    {
        if ((argv[1][i]) >= '0' && (argv[1][i]) <= '9') // Checking for digits
        {
            digits ++;
        }
        else if ((argv[1][i]) != '0' && (argv[1][i]) != '9')// Checking for other special characters
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

        i++;
    }

    int k = atoi(argv[1]); // change the character variable into an integer
    printf("%i\n", k);

    string plaintext = get_string("plaintext: \n");
    int l = strlen(plaintext); // I don't think i actually need this, it was for a previous for loop


    int n = 0;
    char ciphertext[500] = "ciphertext: ";

    while (plaintext[n] != '\0')
    {
        if ((plaintext[n]) >= 'a' && (plaintext[n]) <= 'z')
        {
            char y = (plaintext[n] - 96);  // changing the plaintext ascii code into a 1 - 26 value range
            char z = ((y + k) % 26) + 96;  // changing the plaintext letter into the new letter
            strncat(ciphertext, &z, 1);    // adding the new, changed character to the ciphertext string
        }
        else if ((plaintext[n]) >= 'A' && (plaintext[n]) <= 'Z')
        {
            char Y = (plaintext[n] - 64);
            char Z = ((Y + k) % 26) + 64;
            strncat(ciphertext, &Z, 1);
        }
        else
        {
            strncat(ciphertext, &plaintext[n], 1);  // adding the spaces, special characters, etc. to the ciphertext string
        }

        n++;

    }

    printf("%s\n", ciphertext);

}
