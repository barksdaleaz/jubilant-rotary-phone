#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    bool exist = false;

    for (int i = 0; i < candidate_count; i++)
    {
        if (!strcmp(candidates[i].name, name))
        {
            candidates[i].votes += 1;
            exist = true;
            break;
        }
    }

    return exist;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int votes[candidate_count];
    char winner[candidate_count][50];

    // Copy candidate vote information to seperate array
    for (int i = 0; i < candidate_count; i++)
    {
        votes[i] = candidates[i].votes;
        strcpy(winner[i], candidates[i].name);
    }

    // Bubble sort array
    for (int outer = 0; outer < candidate_count; outer++)
    {
        for (int inner = outer; inner < candidate_count; inner++)
        {
            if (votes[inner] < votes[outer])
            {
                // Sort vote count
                int temp = votes[inner];
                votes[inner] = votes[outer];
                votes[outer] = temp;

                // Sort candidate name to match sorted vote count
                char temp2[50];
                strcpy(temp2, winner[inner]);
                strcpy(winner[inner], winner[outer]);
                strcpy(winner[outer], temp2);
            }
        }
    }

    // Determine if there are any ties.
    for (int i = candidate_count - 1; i >= 0; i--)
    {
        if (votes[i] == votes[i - 1] && votes[i] != votes[i - 2])
        {
            printf("%s\n", winner[i]);
            printf("%s\n", winner[i - 1]);
            break;
        }
        else if (votes[i] == votes[i - 2])
        {
            printf("%s\n", winner[i]);
            printf("%s\n", winner[i - 1]);
            printf("%s\n", winner[i - 2]);
            break;
        }
        else
        {
            printf("%s\n", winner[i]);
            break;
        }
        break;
    }
}

