/*

        adjust_channels :: adjust red/green/blue colour channels in an image
        
        The function returns an adjusted image in the original location.
        
        Copyright (C)2022 Seneca College of Applied Arts and Technology
        Written by Chris Tyler
        Distributed under the terms of the GNU GPL v2
        
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// ----------------------------------------------------------------- Naive implementation in C

#include <sys/param.h>

void adjust_channels(unsigned char *image, int x_size, int y_size, 
        float red_factor, float green_factor, float blue_factor) {

        printf("Using adjust_channels() implementation #1 - Naive (autovectorizable)\n");
        
/*

        The image is stored in memory as pixels of 3 bytes, representing red/green/blue values.
        Each of these values is multiplied by the corresponding adjustment factor, with 
        saturation, and then stored back to the original memory location.
        
        This simple implementation causes int to float to int conversions.
        
*/

        for (int i = 0; i < x_size * y_size * 3; i += 3) {
                image[i]   = MIN((float)image[i]   * red_factor,   255);
                image[i+1] = MIN((float)image[i+1] * blue_factor,  255);
                image[i+2] = MIN((float)image[i+2] * green_factor, 255);
        }
}

