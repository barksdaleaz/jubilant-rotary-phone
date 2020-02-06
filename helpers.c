#include "helpers.h"
#include <math.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width]) // so far, so good (?) as of 3:45 pm
{

    // nested loop: each row of the image, and within each row, each pixel
    // average each pixel, make sure to round to nearest integer, then set each RGB to the average
    // image[2][3].rgbtRed = 0 (or whatever) <- an example of

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float floatavg = (((float)image[h][w].rgbtRed) + ((float)image[h][w].rgbtBlue) + ((float)image[h][w].rgbtGreen)) / 3;
            int roundavg = round(floatavg);
            image[h][w].rgbtRed = image[h][w].rgbtBlue = image[h][w].rgbtGreen = roundavg;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    //sepiaRed = 0.393(originalRed) + 0.769(originalG) + 0.189(originalB)
    //sepiaGreen = 0.349(ogR) + 0.686(ogG) + 0.168(ogB)
    //sepiaBlue = 0.272(ogR) + 0.534(ogG) + 0.131(ogB)

    //if values > 255, just set to 255. must be between 0 and 255


    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float sepiaRed = (0.393 * (image[h][w].rgbtRed)) + (0.769 * (image[h][w].rgbtGreen)) + (0.189 * (image[h][w].rgbtBlue));
            float sepiaGreen = (0.349 * (image[h][w].rgbtRed)) + (0.686 * (image[h][w].rgbtGreen)) + (0.168 * (image[h][w].rgbtBlue));
            float sepiaBlue = (0.272 * (image[h][w].rgbtRed)) + (0.534 * (image[h][w].rgbtGreen)) + (0.131 * (image[h][w].rgbtBlue));

            int sepR = round(sepiaRed);
            int sepG = round(sepiaGreen);
            int sepB = round(sepiaBlue);


            if (sepR > 255)
            {
                sepR = 255;
                image[h][w].rgbtRed = sepR;
            }
            if (sepG > 255)
            {
                sepG = 255;
                image[h][w].rgbtGreen = sepG;
            }
            if (sepB > 255)
            {
                sepB = 255;
                image[h][w].rgbtBlue = sepB;
            }
            image[h][w].rgbtRed = sepR;
            image[h][w].rgbtGreen = sepG;
            image[h][w].rgbtBlue = sepB;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temporary[((width - 1) / 2) + 1]; // Making a temporary array

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j <= round(width / 2); j++) // Assign the first half of the pixels to the temp array
        {
            temporary[j] = image[i][j];
        }

        for (int j = 0; j < round(width / 2); j++) // Move the second half of the pixels to the first half
        {
            image[i][j] = image[i][width + (-j - 1)];
        }

        for (int j = 0; j < round(width / 2); j++) // Move the pixels from temp to the second half
        {
            image[i][width + (-j - 1)] = temporary[j];
        }

    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ogImage[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ogImage[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++) // Are you ready for a whole mess
    {
        for (int j = 0; j < width; j++)
        {
            if (i == 0 && j == 0)
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i + 1][j].rgbtRed + ogImage[i][j + 1].rgbtRed + ogImage[i + 1][j +
                                             1].rgbtRed) / 4.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i + 1][j].rgbtGreen + ogImage[i][j + 1].rgbtGreen + ogImage[i +
                                               1][j +
                                                    1].rgbtGreen) / 4.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i + 1][j].rgbtBlue + ogImage[i][j + 1].rgbtBlue + ogImage[i + 1][j +
                                              1].rgbtBlue) / 4.0);
            }
            else if (i == 0 && j == width - 1)
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i + 1][j].rgbtRed + ogImage[i][j - 1].rgbtRed + ogImage[i + 1][j -
                                             1].rgbtRed) / 4.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i + 1][j].rgbtGreen + ogImage[i][j - 1].rgbtGreen + ogImage[i +
                                               1][j -
                                                    1].rgbtGreen) / 4.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i + 1][j].rgbtBlue + ogImage[i][j - 1].rgbtBlue + ogImage[i + 1][j -
                                              1].rgbtBlue) / 4.0);
            }
            else if (i == 0)
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i][j - 1].rgbtRed + ogImage[i][j + 1].rgbtRed + ogImage[i +
                                             1][j].rgbtRed + ogImage[i + 1][j - 1].rgbtRed + ogImage[i + 1][j + 1].rgbtRed) / 6.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i][j - 1].rgbtGreen + ogImage[i][j + 1].rgbtGreen + ogImage[i +
                                               1][j].rgbtGreen + ogImage[i + 1][j - 1].rgbtGreen + ogImage[i + 1][j + 1].rgbtGreen) / 6.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i][j - 1].rgbtBlue + ogImage[i][j + 1].rgbtBlue + ogImage[i +
                                              1][j].rgbtBlue + ogImage[i + 1][j - 1].rgbtBlue + ogImage[i + 1][j + 1].rgbtBlue) / 6.0);
            }
            else if (i == height - 1 && j == 0)
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i - 1][j].rgbtRed
                                             + ogImage[i][j + 1].rgbtRed + ogImage[i - 1][j + 1].rgbtRed) / 4.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i - 1][j].rgbtGreen
                                               + ogImage[i][j + 1].rgbtGreen + ogImage[i - 1][j + 1].rgbtGreen) / 4.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i - 1][j].rgbtBlue
                                              + ogImage[i][j + 1].rgbtBlue + ogImage[i - 1][j + 1].rgbtBlue) / 4.0);
            }
            else if (j == 0) // Oh it keeps going
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i - 1][j].rgbtRed + ogImage[i + 1][j].rgbtRed
                                             + ogImage[i][j + 1].rgbtRed + ogImage[i - 1][j + 1].rgbtRed + ogImage[i + 1][j + 1].rgbtRed) / 6.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i - 1][j].rgbtGreen + ogImage[i + 1][j].rgbtGreen
                                               + ogImage[i][j + 1].rgbtGreen + ogImage[i - 1][j + 1].rgbtGreen + ogImage[i + 1][j + 1].rgbtGreen) / 6.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i - 1][j].rgbtBlue + ogImage[i + 1][j].rgbtBlue
                                              + ogImage[i][j + 1].rgbtBlue + ogImage[i - 1][j + 1].rgbtBlue + ogImage[i + 1][j + 1].rgbtBlue) / 6.0);
            }
            else if (i == height - 1 && j == width - 1)
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i - 1][j].rgbtRed
                                             + ogImage[i][j - 1].rgbtRed + ogImage[i - 1][j - 1].rgbtRed) / 4.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i - 1][j].rgbtGreen
                                               + ogImage[i][j - 1].rgbtGreen + ogImage[i - 1][j - 1].rgbtGreen) / 4.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i - 1][j].rgbtBlue
                                              + ogImage[i][j - 1].rgbtBlue + ogImage[i - 1][j - 1].rgbtBlue) / 4.0);
            }
            else if (i == height - 1)
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i][j - 1].rgbtRed + ogImage[i][j + 1].rgbtRed
                                             + ogImage[i - 1][j].rgbtRed + ogImage[i - 1][j - 1].rgbtRed + ogImage[i - 1][j + 1].rgbtRed) / 6.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i][j - 1].rgbtGreen + ogImage[i][j + 1].rgbtGreen
                                               + ogImage[i - 1][j].rgbtGreen + ogImage[i - 1][j - 1].rgbtGreen + ogImage[i - 1][j + 1].rgbtGreen) / 6.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i][j - 1].rgbtBlue + ogImage[i][j + 1].rgbtBlue
                                              + ogImage[i - 1][j].rgbtBlue + ogImage[i - 1][j - 1].rgbtBlue + ogImage[i - 1][j + 1].rgbtBlue) / 6.0);
            }
            else if (j == width - 1) // No, it hasn't stopped yet
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i - 1][j].rgbtRed + ogImage[i + 1][j].rgbtRed
                                             + ogImage[i][j - 1].rgbtRed + ogImage[i - 1][j - 1].rgbtRed + ogImage[i + 1][j - 1].rgbtRed) / 6.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i - 1][j].rgbtGreen + ogImage[i + 1][j].rgbtGreen
                                               + ogImage[i][j - 1].rgbtGreen + ogImage[i - 1][j - 1].rgbtGreen + ogImage[i + 1][j - 1].rgbtGreen) / 6.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i - 1][j].rgbtBlue + ogImage[i + 1][j].rgbtBlue
                                              + ogImage[i][j - 1].rgbtBlue + ogImage[i - 1][j - 1].rgbtBlue + ogImage[i + 1][j - 1].rgbtBlue) / 6.0);
            }
            else
            {
                image[i][j].rgbtRed = round((ogImage[i][j].rgbtRed + ogImage[i][j - 1].rgbtRed + ogImage[i][j + 1].rgbtRed
                                             + ogImage[i - 1][j].rgbtRed + ogImage[i - 1][j - 1].rgbtRed + ogImage[i - 1][j + 1].rgbtRed
                                             + ogImage[i + 1][j].rgbtRed + ogImage[i + 1][j - 1].rgbtRed + ogImage[i + 1][j + 1].rgbtRed) / 9.0);

                image[i][j].rgbtGreen = round((ogImage[i][j].rgbtGreen + ogImage[i][j - 1].rgbtGreen + ogImage[i][j + 1].rgbtGreen
                                               + ogImage[i - 1][j].rgbtGreen + ogImage[i - 1][j - 1].rgbtGreen + ogImage[i - 1][j + 1].rgbtGreen
                                               + ogImage[i + 1][j].rgbtGreen + ogImage[i + 1][j - 1].rgbtGreen + ogImage[i + 1][j + 1].rgbtGreen) / 9.0);

                image[i][j].rgbtBlue = round((ogImage[i][j].rgbtBlue + ogImage[i][j - 1].rgbtBlue + ogImage[i][j + 1].rgbtBlue
                                              + ogImage[i - 1][j].rgbtBlue + ogImage[i - 1][j - 1].rgbtBlue + ogImage[i - 1][j + 1].rgbtBlue
                                              + ogImage[i + 1][j].rgbtBlue + ogImage[i + 1][j - 1].rgbtBlue + ogImage[i + 1][j + 1].rgbtBlue) / 9.0);
            }
        }
    }

    return;
}
