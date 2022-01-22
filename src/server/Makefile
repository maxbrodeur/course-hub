target=main
cybridge=caller

CC=gcc
CFLAGS= `python3-config --cflags`
LDFLAGS=`python3-config --ldflags`

all:
        cython $(cybridge).pyx
        $(CC) $(CFLAGS) -c *.c
        $(CC) $(LDFLAGS) *.o -o $(target)

clean:
        rm -f $(cybridge).{c,h,o} $(target).o $(target)
        rm -rf __pycache__