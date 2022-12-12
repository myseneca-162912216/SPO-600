.text
.globl _start

min = 0                          /* starting value for the loop index; note that this is a symbol (constant), not a variable */
max = 10                         /* loop exits when the index hits this number (loop condition is i<max) */

_start:

        mov     x19, min

loop:

        /*Start of loop*/

        mov     x20, x19
        add     x20, x20, '0'
        adr     x21, msg + 5
        strb    w20, [x21]

        mov     x0, 1
        adr     x1, msg
        mov     x2, len

        mov     x8, 64
        svc     0

        /*End of loop*/

        add     x19, x19, 1
        cmp     x19, max
        b.ne    loop

        mov     x0, 0           /* status -> 0 */
        mov     x8, 93          /* exit is syscall #93 */
        svc     0               /* invoke syscall */

.data
msg:    .ascii  "Loop #\n"
len=    . - msg