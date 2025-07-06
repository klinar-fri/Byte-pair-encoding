#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>


#define STB_DS_IMPLEMENTATION
#include "stb_ds.h"
#include <stdint.h>

typedef struct{
    uint32_t l;
    uint32_t r;
} Pair;

typedef struct{
    Pair* items;
    int count;
} Pairs;

typedef struct{
    Pair key;
    int value;
} Freq;


typedef struct{
    Freq* items;
    int count;
} Freqs;

typedef struct{
    uint32_t* items;
    int count;
} Tokens;


int compareFreqs(const void* a, const void* b){
    const Freq* af = a;
    const Freq* bf = b;
    return (int)bf->value - (int)af->value;
}

void renderTokens(Pairs pairs, Tokens tokens){
    for(int i = 0; i < tokens.count; i++){
        uint32_t currToken = tokens.items[i];
        assert(currToken < pairs.count);
        // if we reach the "leaf" node we just print normally
        // else we print the changed 2 characters as token
        if(pairs.items[currToken].l == currToken){
            printf("%c", currToken);
        }else{
            printf("[%d]", currToken);
        }
    }
    printf("\n");
}


int main(){
    const char* txt = "The original BPE algorithm operates by iteratively replacing the most common contiguous sequences of characters in a target text with unused 'placeholder' bytes. The iteration ends when no sequences can be found, leaving the target text effectively compressed. Decompression can be performed by reversing this process, querying known placeholder terms against their corresponding denoted sequence, using a lookup table. In the original paper, this lookup table is encoded and stored alongside the compressed text.";
    int textSize = strlen(txt);

    // hash table of frequency
    Freq* freq = NULL;
    // dinamic array of pairs -> bpe table
    Pairs pairs = {0};
    // tokens we are currently working on
    Tokens tokensIn = {0};
    Tokens tokensOut = {0};

    // 0   => {.l = 0, .r = ???}
    // 1   => {.l = 0, .r = ???}
    // ...
    // 41  => {.l = 41, .r = ???}
    // ...
    // 255 => {.l = 0, .r = ???}
    // 256 => {.l = 41, .r = 69}

    for(uint32_t i = 0; i < 256; i++){
        arrput(pairs.items, ((Pair){.l = i}));
        pairs.count += 1;
    }

    for(int i = 0; i < textSize; i++){
        arrput(tokensIn.items, txt[i]);
        tokensIn.count += 1;
    }

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

    // Freqs sortedFreqs = {0};
    // for(ptrdiff_t i = 0; i < hmlen(freq); i++){
    //     // printf("%c%c => %d\n", freq[i].key.l, freq[i].key.r, freq[i].value);
    //     arrput(sortedFreqs.items, freq[i]);
    //     sortedFreqs.count += 1;
    // }

    // sort the frequencies and display them
    // qsort(sortedFreqs.items, sortedFreqs.count, sizeof(*sortedFreqs.items), compareFreqs);
    // // sortedFreqs.count
    // for(int i = 0; i < 10; i++){
    //     printf("(%u, %u) => %d\n", sortedFreqs.items[i].key.l, sortedFreqs.items[i].key.r, sortedFreqs.items[i].value);
    // }

    // find max
    int maxIdx = 0;
    for(int i = 0; i < hmlen(freq); i++){
        if(freq[i].value > freq[maxIdx].value){
            maxIdx = i;
        }
    }
    // printf("(%u,%u) => %d\n", freq[maxIdx].key.l, freq[maxIdx].key.r, freq[maxIdx].value);

    arrput(pairs.items, freq[maxIdx].key);
    pairs.count += 1; // ! forgot to increase the pairs.count, tricky BUG!

    tokensIn.count = arrlenu(tokensIn.items);
    for(int i = 0; i < tokensIn.count;){
        if(i + 1 >= tokensIn.count){
            arrput(tokensOut.items, tokensIn.items[i]);
            tokensOut.count += 1;
            i += 1;
        }else{
            Pair pair = {.l = tokensIn.items[i], .r = tokensIn.items[i + 1]};
            if(memcmp(&pair, &freq[maxIdx].key, sizeof(pair)) == 0){
                arrput(tokensOut.items, pairs.count - 1);
                tokensOut.count +=1;
                i += 2;
            }else{
                arrput(tokensOut.items, tokensIn.items[i]);
                tokensOut.count +=1;
                i += 1;
            }
        }
        
    }

    renderTokens(pairs, tokensIn);
    printf("\n");
    renderTokens(pairs, tokensOut);
    printf("%d\n%d\n", tokensIn.count, tokensOut.count);
    return 0;
}