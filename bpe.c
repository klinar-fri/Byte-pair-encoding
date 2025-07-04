#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>


#define STB_DS_IMPLEMENTATION
#include "stb_ds.h"

typedef struct{
    char l;
    char r;
} Pair;

typedef struct{
    Pair key;
    int value;
} Freq;


typedef struct{
    Freq* items;
    int count;
} Freqs;


int compareFreqs(const void* a, const void* b){
    const Freq* af = a;
    const Freq* bf = b;
    return (int)bf->value - (int)af->value;
}


int main(){
    const char* txt = "The original BPE algorithm operates by iteratively replacing the most common contiguous sequences of characters in a target text with unused 'placeholder' bytes. The iteration ends when no sequences can be found, leaving the target text effectively compressed. Decompression can be performed by reversing this process, querying known placeholder terms against their corresponding denoted sequence, using a lookup table. In the original paper, this lookup table is encoded and stored alongside the compressed text.";
    int textSize = strlen(txt);

    Freq* freq = NULL;

    for(int i = 0; i < textSize - 1; i++){
        // printf("%c%c\n", txt[i], txt[i + 1]);
        Pair pair = {txt[i], txt[i + 1]};
        ptrdiff_t i = hmgeti(freq, pair);
        if(i < 0){
            hmput(freq, pair, 1);
        }else{
            freq[i].value += 1;
        }
    }

    Freqs sortedFreqs = {0};

    for(ptrdiff_t i = 0; i < hmlen(freq); i++){
        // printf("%c%c => %d\n", freq[i].key.l, freq[i].key.r, freq[i].value);
        arrput(sortedFreqs.items, freq[i]);
        sortedFreqs.count += 1;
    }

    // sort the frequencies and display them
    /*
    qsort(sortedFreqs.items, sortedFreqs.count, sizeof(*sortedFreqs.items), compareFreqs);

    for(int i = 0; i < sortedFreqs.count; i++){
        printf("%c%c => %d\n", sortedFreqs.items[i].key.l, sortedFreqs.items[i].key.r, sortedFreqs.items[i].value);
    }
    */

    // find max
    int max = 0;
    int maxIdx = 0;
    for(int i = 0; i < sortedFreqs.count; i++){
        if(sortedFreqs.items[i].value > max){
            max = sortedFreqs.items[i].value;
            maxIdx = i;
        }
    }
    printf("[%c%c] => %d\n", sortedFreqs.items[maxIdx].key.l, sortedFreqs.items[maxIdx].key.r, sortedFreqs.items[maxIdx].value);

    return 0;
}