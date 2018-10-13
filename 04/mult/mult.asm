// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// RAM words:
// R0: Multiplicand. Will be left-shifted one bit at the end of each loop.
// R1: Multiplicand. Will be &ed with a one-bit mask each loop.
// R2: Accumulates the sums R2 + R0; will contain product of R0,R1 at end.
// R3: One-bit mask, equal to 2^i at the end of the ith loop.
// R4: R1 & R4. If 0, skips to the increment step.
// j:  Counter variable. The program loops 15 times.

// Initialize:
@R2
M=0		//Initialize product to 0
@R0
D=M		//D=R0
@R5
M=D		//R5=R0
@15
D=A		//D=15
@j
M=D		//j=15
@1
D=A		//D=1
@R3
M=D		//R3=1 
(LOOP)
@R1
D=M		//D=R1
@R3
D=D&M		//Bitwise mask
@INC		
D;JEQ		//Skip to increment step if 0
@R5
D=M		//D=R5
@R2		
M=M+D		//R2=R2+R5 
(INC)
@j		
M=M-1		//j--
D=M
@END
D;JEQ		//Terminate if j=0
@R5
D=M		//D=R5
M=D+M		//R5=R5+R5
@R3
D=M		//D=R3
M=D+M		//R3=R3+R3
@LOOP
0;JMP		//Return to start of loop
(END)
@END
0;JMP		//Infinite loop to terminate