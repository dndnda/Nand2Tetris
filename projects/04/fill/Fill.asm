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


  (LOOP)
     @KBD  
     D=M
     @BLACK
     D;JNE

     @WHITE
     0;JMP

     @LOOP
     0;JMP

  (BLACK)
     @SCREEN  //addr = SCREEN
     D=A
     @addr
     M=D

     @i
     M=0
     @8192
     D=A
     @n
     M=D

   (LOO)
     @i    // if i >= n, end the loop
     D=M
     @n
     D=D-M
     @LOOP
     D;JGE

     @addr  
     A=M
     M=-1

     @addr  //addr += 1
     M=M+1

     @i     // i += 1
     M=M+1
     
     @LOO
     0;JMP

  (WHITE)
     @SCREEN  //addr = SCREEN
     D=A
     @addr
     M=D

     @i
     M=0
     @8192
     D=A
     @n
     M=D

   (LOOO)
     @i    // if i >= n, end the loop
     D=M
     @n
     D=D-M
     @LOOP
     D;JGE

     @addr  
     A=M
     M=0

     @addr  //addr += 1
     M=M+1

     @i     // i += 1
     M=M+1
     
     @LOOO
     0;JMP



