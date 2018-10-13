// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// R0: Counter from SCREEN to SCREEN + 8192 (16384 to 24576)
// R1: Contains the color being drawn
// i: Loop counter (32 iterations)

//Initialization:
@16384
D=A
@R0
M=D		//R0=16384
@32
D=A
@i
M=D		//i=32
@0
D=A
@R1
M=D		//The screen is initially white (pixel=0)
(LOOP)
@R1
D=M
@R0
A=M
M=D		//Fill the chunk with the color indicated by R1
@R0
M=M+1		//Increment the chunk being considered.
@i
M=M-1		//Increment the loop counter
D=M
@CHECK	
D,JEQ		//Checks for new input after 32 loops
@LOOP
0,JMP		//Loops
(CHECK)
@32
D=A
@i
M=D		//Reset loop
@R0
D=M
@24576
D=D-A
@READ
D,JNE		//Do nothing if R0 != 24576
@16384
D=A
@R0
M=D		//Return to top line after bottom line
(READ) 
@KBD
D=M
@ZERO
D,JEQ		//Jump to ZERO (D=0) if KBD==0
@R1
M=-1
@LOOP
0,JMP		//Jump to loop
(ZERO)		
@R1
M=D		//R1=0 (black pixels) if KBD==0
@LOOP
0,JMP		//Jump to loop