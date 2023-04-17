// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

	@sum  //sum=0
	M=0

	@R1  //n=R1
	D=M
	@n
	M=D

	@i  // i=0
	M=0
  (LOOP)
    // if i >= n, goto SET
    @i
    D=M
    @n
    D=D-M
    @SET
    D;JGE

    // else sum += R0
    @R0
    D=M
    @sum
    M=D+M

    // i += 1
    @i
    M=M+1

    @LOOP
    0;JMP

  (SET)
    @sum
    D=M
    @R2
    M=D

    @END
    0;JMP

  (END)
    @END
    0;JMP

