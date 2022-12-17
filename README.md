### Rat22F-Compiler
A compiler for the made up language Rat22F in my Compilers lecture.
This program will read in code files that follows grammar listed below(Also example file given "test1.rat") and generate assembly code to an output file.

#Execute: 
python3 ratf.py [INPUTFILE] -o [OUTPUTFILE]

#Atttributes:
1. First will slice code into tokens using the lexical analysis
2. Then will send tokens to the syntax analayzer to get production rules
3. Lastly will generate assembly code from production rules and outputs to file.
#

### Grammar For Rat22F

R1. <Rat21F>  ::=   <Opt Function Definitions>   #  <Opt Declaration List>  <Statement List>  #
R2. <Opt Function Definitions> ::= <Function Definitions>     |  <Empty>
R3. <Function Definitions>  ::= <Function> | <Function> <Function Definitions>   
R4. <Function> ::= function  <Identifier>   ( <Opt Parameter List> )  <Opt Declaration List>  <Body>
R5. <Opt Parameter List> ::=  <Parameter List>    |     <Empty>
R6. <Parameter List>  ::=  <Parameter>    |     <Parameter> , <Parameter List>
R7. <Parameter> ::=  <IDs >  <Qualifier> 
R8. <Qualifier> ::= integer    |    boolean    |  real 
R9. <Body>  ::=  {  < Statement List>  }
R10. <Opt Declaration List> ::= <Declaration List>   |    <Empty>
R11. <Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>
R12. <Declaration> ::=   <Qualifier > <IDs>                   
R13. <IDs> ::=     <Identifier>    | <Identifier>, <IDs>
R14. <Statement List> ::=   <Statement>   | <Statement> <Statement List>
R15. <Statement> ::=   <Compound>  |  <Assign>  |   <If>  |  <Return>   | <Print>   |   <Scan>   |  <While> 
R16. <Compound> ::=   {  <Statement List>  } 
R17. <Assign> ::=     <Identifier> = <Expression> ;
R18. <If> ::=     if  ( <Condition>  ) <Statement>   endif   |   
                          if  ( <Condition>  ) <Statement>   else  <Statement>  endif 
R19. <Return> ::=  return ; |  return <Expression> ;
R21. <Print> ::=    put ( <Expression>);
R21. <Scan> ::=    get ( <IDs> );
R22. <While> ::=  while ( <Condition>  )  <Statement>  
R23. <Condition> ::=     <Expression>  <Relop>   <Expression>
R24. <Relop> ::=        ==   |   !=    |   >     |   <    |  <=   |    =>        
R25. <Expression>  ::=    <Expression> + <Term>    | <Expression>  - <Term>    |    <Term>
R26. <Term>    ::=      <Term>  *  <Factor>     |   <Term>  /  <Factor>     |     <Factor>
R27. <Factor> ::=      -  <Primary>    |    <Primary>
R28. <Primary> ::=     <Identifier>  |  <Integer>  |   <Identifier>  ( <IDs> )   |   ( <Expression> )   |  
                                     <Real>  |   true   |  false                        
R29. <Empty>   ::= EMPTY

#
