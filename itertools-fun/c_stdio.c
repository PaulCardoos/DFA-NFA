#include <stdio.h>
#include <stdlib.h>

int main (){
    int ch;
    char word[100];

    for(int i = 0; (ch = getchar())!= EOF; i++){
        word[i] = ch;
    }
    for(int i = 0; i < 3; i++){
        printf("%s\n", word);
    }
    

    return 0;
}