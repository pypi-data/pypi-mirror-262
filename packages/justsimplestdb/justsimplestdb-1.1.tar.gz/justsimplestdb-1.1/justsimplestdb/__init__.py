"""
Simplified DataBase Management System(SDBMS) using raw python, can also read ".txt" files into database-like format.

Author: Jakub Aleksander Michalski

Short documentation:

    -   REMEMBER TO RUN YOUR CODE IN IT'S DIRECTORY! 
    
        Otherwise libary's gonna create DBMS Shell in other place on disk;

    -   You can use separator attribute(example: justsimplestdb.Instance("example", separator=";")).

        Separator variable determines ".txt" divider for each line in it(default value is TAB);

    -   When you create justsimplestdb.Instance(file name) and run code, DBMS Shell is gonna be created;

    -   In braces, you provide file name without extention, libary automatically assign extentions;

    -   read_it_like_db() method (you don't provide ANY arguments in braces) reads

        filename.txt if it exists, and returns it as database-like formatted list.

        Libary automatically reads data from .txt file if it exists, 
        
        which allows you to use other READ-ONLY methods instantly, 
        
        but use it when you want to see read data, or assign the return of this method to a variable;

    -   Most of created methods have own variants, "txt" methods and "db" methods.

        "txt" methods are dedicated for operating on "txt" file if exists(which means it won't work for database), 

        "txt" methods offers READ-ONLY operations.

        "db" methods are dedicated for operating on database file if exists,

        which allows you to save data and perform CRUD(Create Read Update Delete) operations.

        To save data read from ".txt" file, add attribute "do_save_as_db=True" in braces.

        Example: example = justsimplestdb.Instance("example", do_save_as_db=True);


    FULL DOCUMENTATION: https://github.com/M1ch5lsk1/JustSimplestDB

"""
from justsimplestdb.owntypes import *
from justsimplestdb.JustSimplestDB import *