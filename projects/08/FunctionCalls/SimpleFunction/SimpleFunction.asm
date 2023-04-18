// function SimpleFunction.test 2
// Init R13 to n, R14 to i=0
(SimpleFunction.test)
@2
D=A
@R13
M=D
@R14
M=0
// condition judge
(SimpleFunction.test$condition)
@R13
D=M
@R14
D=M-D
@end$SimpleFunction.test$loop
D;JGE
// Init local vars
@SP
A=M
M=0
@SP
M=M+1
@R14
M=M+1
@SimpleFunction.test$condition
0;JMP
(end$SimpleFunction.test$loop)

// push local 0
@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 1
@LCL
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// not
@SP
AM=M-1
M=!M
@SP
M=M+1
// push argument 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// push argument 1
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// return
@LCL
D=M
@R15
M=D
@R14
M=D
@5
D=A
@R14
A=M-D
D=M
@R13
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R15
D=M
D=D-1
A=D
D=M
@THAT
M=D
@R15
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R15
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R15
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R13
A=M
0;JMP

