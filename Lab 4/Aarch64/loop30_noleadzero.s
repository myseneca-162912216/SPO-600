.text
.globl _start

min = 0                          /* starting value for the loop index; note that this is a symbol (constant), not a variable */
max = 31                         /* loop exits when the index hits this number (loop condition is i<max) */

_start:

        mov     x19, min
        mov     x22, 10

loop:
        /*loop start*/

        adr     x23, msg        /*setting the string address*/

        udiv    x20, x19, x22   /*calculating first digit*/
        msub    x21, x22, x20, x19  /* calulating remainder - second digit */
        cmp     x19,x22
        b.lt    ddigit
        add     x20, x20, '0'
        strb    w20, [x23, 5]   /*writing the first digit*/
ddigit:
        add     x21, x21, '0'
        strb    w21, [x23, 6]   /*writing the second digit*/

        mov     x0, 1
        adr     x1, msg
        mov     x2, len

        mov     x8, 64
        svc     0

        /*loop end*/

        add     x19, x19, 1
        cmp     x19, max
        b.ne    loop

        mov     x0, 0           /* status -> 0 */
        mov     x8, 93          /* exit is syscall #93 */
        svc     0               /* invoke syscall */

.data
msg:    .ascii  "Loop  #\n"
len=    . - msg