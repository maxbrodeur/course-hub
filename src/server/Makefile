target=main
cybridge=caller

CC=g++-10
CFLAGS= `python3-config --cflags`
LDFLAGS=`python3-config --ldflags`
PYLIBS_DIR=`python3-config --libs`
PY__TEST="-L/Users/theofabilous/opt/anaconda3/pkgs/python-3.9.7-h88f2d9e_1/lib"

all:
	cython $(cybridge).pyx
	$(CC) $(CFLAGS) -c *.c
	$(CC) $(LDFLAGS) $(PY__TEST) -lpython3.9 *.o -o $(target) 

clean:
	rm -f $(cybridge).{c,h,o} $(target).o $(target)
	rm -rf __pycache__