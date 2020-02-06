// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table , used to be const unsigned int N = 1995;
#define N 32

// Hash table
node *table[N] = {};

int wordcount = 0;


// Returns true if word is in dictionary else false

bool check(const char *word)
{
    bool exist = false;
    //char buff[LENGTH + 1];
    //int wordlength = strlen(word);

    //for (int i = 0; i < wordlength; i++)
    //{
        //buff[i] = tolower(word[i]); // make letters lowercase
    //}

    int index = hash(word); // originally hash(buff) % N

    node *head = table[index];
    if (head == NULL)
    {
        return false;
    }

    //for (node *cursor = head; cursor != NULL; cursor = cursor->next)

    else
    {
        node *cursor = table[index];
        while (cursor != NULL)
        {
            if (strcasecmp(cursor->word, word) == 0)
            {
                exist = true;
                break;
            }
            else
            {
                cursor = cursor->next;
            }
        }
        return exist;
    }
}

// Hashes word to a number
unsigned long hash(const char *str)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *str++))
    hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash % N;
}

// Hash function is from http://www.cse.yorku.ca/~oz/hash.html

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r"); // Opening the dictionary file
    if (file == NULL)
    {
        return false;
        printf("Cannot open dictionary.\n");
    }

    char word[LENGTH + 1];

    for (int i = 0; i < N; i++) // Initialize all members of the hashtable to NULL
    {
        table[i] = NULL;
    }

    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node)); // Creating a temporary node
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);

        unsigned long hashindex = hash(word); // Hashing the word to get a hash index, maybe hash(n->word)? originally hash(buffer)

        if (table[hashindex] == NULL)
        {
            table[hashindex] = n;
            n->next = NULL;
        }
        else
        {
            n->next = table[hashindex]; // Put the node into the hashtable
            table[hashindex] = n; // Change the pointer (?)
        }

        wordcount++; // Keeps track of how many words are being loaded (for the size function)
    }

    fclose(file);
    return true;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor; // Create temporary node
            cursor = cursor->next; // Move cursor to the next one so it still points to linked list
            free(temp); // Free temp and then repeat the process, moving temp to cursor and cursor up one more
        }
    }
    return true;
}
