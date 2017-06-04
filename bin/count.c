#include <stdio.h>

int main( void )
{
    int c;
    int count = 0;

    //turn off buffering
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    c = fgetc(stdin);
    while(c != EOF)
    {
	if (c=='.' || c=='E' || c=='F') count++;
	fputc(c, stdout);
	fflush(stdout);
	if ( count % 76 == 0) {
	    fprintf(stderr, "%4d", count);
	    fflush(stderr);
	}
	c = fgetc(stdin);
    }
    return 0;
}
