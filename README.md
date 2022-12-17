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

![image](https://user-images.githubusercontent.com/82180479/208268789-cb28a23f-8513-479f-93fa-433f096fff28.png)


#
