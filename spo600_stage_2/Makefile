
# Useful CFLAGS values:
#    Basic aarch64 target:	-march=armv8-a
#    aarch64 with SVE:		-march=armv8.5-a+sve
#    aarch64 with SVE2:		-march=armv8.5-a+sve2
#
# Note that armv9-a does not appear to be accepted
# by some versions of gcc that can emit sve2 
# instructions (contrary to the docs).
#
CFLAGS = -g -O3 -march=armv8-a
RUNTOOL = 
TIMETOOL = time
BINARIES = main

all-test:		${BINARIES}
			echo "Making and testing all versions..."
			${RUNTOOL} ./main tests/input/bree.jpg 1.0 1.0 1.0 tests/output/bree1a.jpg
			${RUNTOOL} ./main tests/input/bree.jpg 0.5 0.5 0.5 tests/output/bree1b.jpg
			${RUNTOOL} ./main tests/input/bree.jpg 2.0 2.0 2.0 tests/output/bree1c.jpg

all:			${BINARIES}

main:			main.c function.o
			gcc ${CFLAGS_MAIN} main.c function.o -o main

function.o:		function.c
			gcc ${CFLAGS} -c function.c -o function.o

clean:			
			rm ${BINARIES} *.o tests/output/bree??.jpg tests/output/montage.jpg || true


