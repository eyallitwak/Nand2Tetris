// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//prepares R2 and an iterator variable
   @R2
   M=0
   @i
   M=0
 
//if either factor is 0, end immediately 
   @R0
   D=M
   @END
   D;JLE
   @R1
   D=M
   @END
   D;JLE

//adds R1 to R2, R0 times   
(LOOP)
   @R1
   D=M
   @R2
   M=D+M
   
   @i
   M=M+1

   D=M
   @R0
   D=D-M
   @LOOP
   D;JLT

(END)
   @END
   0;JMP