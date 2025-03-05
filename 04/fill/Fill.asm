// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(LOOP)
    //if there's input, set color variable to black
    //otherwise, set it to white
    @KBD
    D=M
    @BLACK
    D;JNE
    @color
    M=0

(CONT)
    //prepares variable that keeps the location we need to draw on
    @SCREEN
    D=A
    @location
    M=D

(DRAW)
    //go to where "location" is pointing and draw accordingly!
    @color
    D=M
    @location
    A=M
    M=D
    //advance location by 1
    @location
    DM=M+1

    //continue drawing until everything is colored accordingly
    @24575
    D=D-A
    @DRAW
    D;JLE

    //jump to the start to listen to new input
    @LOOP
    0;JMP

(BLACK)
    @color
    M=-1
    @CONT
    0;JMP