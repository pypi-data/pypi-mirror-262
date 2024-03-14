import justsimplestdb.owntypes as owntypes
from justsimplestdb.owntypes import *
class Instance:
    def __init__(self, file_to_read: owntypes.FileName,
                 do_save_txt_as_db: bool = False,
                 separator: str = "\t") -> None:
        """
        JustSimplestDB instance which allows you to use DBMS methods.
        
        Variable named do_save_as_db determines creating database_file_to_read.py from provided .txt file.
        
        It means, if this value is set to True, first program start will automatically create database file based on .txt file.
        
        Default value for save_as_db is False, but you can change it to True.

        Separator variable(default value is TAB) determines how this libary divides each record for database.

        Separator variable CAN'T be equal space(s).
        """
        self.sep = separator
        if bool(self.sep) != True:
            raise WrongSeparator(f"Separator {self.sep} is wrong, separator can't be a null or space(s).") 
        self.main_file = file_to_read
        self.__shell = "shell_" + self.main_file + ".py"
        self.__is_shell_exists = is_file_exists(self.__shell)
        if owntypes.is_file_exists(self.__shell):
            self.__is_shell_exists = True
        self.do_save_txt_as_db = do_save_txt_as_db
        self.txt_db_file: str = self.main_file + ".txt"
        self.db_file = "database_" + self.main_file + ".py"
        self.__is_dummy_record_var = self.__is_dummy_record()
        self.is_new_db = self.__is_dummy_record()
        self.DATABASE = []
        self.structurised_list = owntypes.StructurisedListLikeDBObject([])
        self.struct_list_keys = []
        self.database_keys_list = []
        self.is_txt_exists = owntypes.is_file_exists(self.txt_db_file)
        self.is_db_exists = owntypes.is_file_exists(self.db_file)
        if self.is_txt_exists:
            self.structurised_list = self.read_it_like_db()
            self.struct_list_keys = self.get_txt_keys()
            
        if self.is_db_exists:
            self.__create_dbms_shell()
            self.do_save_txt_as_db = True
            self.database_keys_list = self.get_db_keys()
            self.DATABASE = self.read_db()
        if not self.__is_shell_exists:
            self.__create_dbms_shell()
            
        if self.do_save_txt_as_db:
            if not self.is_db_exists and self.is_txt_exists:
                self.save_as_db()
    
    def read_it_like_db(self) -> owntypes.StructurisedListLikeDBObject:
        #start
        """
        WORKS ONLY FOR .txt FILES!
        
        Method converting files to structurised data (like databases(KEY: VALUE)) and returning list with sub-dicts.
        
        Each key and value in row needs to be seperated by TAB.
        
        First line of the file is read as list of keys for the rest of data.
        
        first line: (keys   keys    keys) each row is seperated by TAB
        
        second line: (values values  values)
        
        third line: (values values  values)
        
        Provided file should have empty last line.
        
        DO NOT edit or have opened provided file while this method is working.
        
        DO NOT edit provided file with IDE, because TABs(defualt value) in them are interpreted as several spaces instead as TAB.
        """
        #end
        
        temp_structurised_list = owntypes.StructurisedListLikeDBObject([])
        keys = []
        keys_lenght: int
        temp_dict: dict
        is_first_line = True
        id_counter = 0
        try:
            with open(self.txt_db_file, encoding="UTF-8") as file:
                read_lines = file.readlines()
                if not self.sep in read_lines[0]:
                    raise WrongSeparator("Separators in .txt files are different than provided separators.\nAdd a \"separator=<separator string value>\" into Instance attributes.")
                
                # dodawanie pustej linii jeśli jej nie ma, zapewnia poprawność odczytu wszystkich danych
                with open(self.txt_db_file, mode="a", encoding="UTF-8") as subfile:
                    if not "\n" in read_lines[-1]:
                        subfile.write("\n")
                        raise Exception(f"INFO for file {self.txt_db_file}: Please, restart the program (this info may appear x times for other files).")
                
                for line in read_lines:
                    if is_first_line:
                        temp_line = line
                        line = "id" + self.sep
                        line += temp_line
                    
                    line = line.split(self.sep)
                    
                    line[-1] = self.__delete_chars(line[-1], 1)
                    
                    # pierwsza linia zawsze zawiera informacje na temat kluczy
                    if is_first_line:
                        keys = line
                        is_first_line = False
                        continue
                    
                    # tymczasowy słownik przechowujący informacje o bierzącym przetwarzanym rekordzie
                    temp_dict = {}
                    keys_lenght = len(keys)
                    temp_dict[keys[0]] = id_counter
                    id_counter += 1
                    for keys_index in range(1, keys_lenght):
                        temp_dict[keys[keys_index]] = line[keys_index-1]
                        try:
                            temp_dict[keys[keys_index]] = float(temp_dict[keys[keys_index]])
                        except ValueError:
                            pass
                    temp_structurised_list.append(temp_dict)
                    temp_dict = {}
                file.close()
            return temp_structurised_list
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {self.txt_db_file}, because it doesn't exist.")
    
    def read_db(self) -> owntypes.DatabaseObject:
        #start
        """
        WORKS FOR .py ONLY!
        
        Reads data from database_FILE_NAME.py if exists.
        """
        #end
        temp_db = ""
        namespace = {} 
        try:
            with open(self.db_file, encoding="UTF-8") as file:
                temp_db = file.read()
            exec(temp_db, namespace)
            if "DATABASE" in namespace:
                return namespace["DATABASE"]
        except FileNotFoundError:
            raise owntypes.DatabaseObjectExistence("Database file is not created, change do_save_txt_as_db value to True and restart the program, or create it using 'save_as_db' method.")
    
    def get_db_keys(self) -> list[dict]:
        #start
        """
        WORKS ONLY FOR DATABASE FILE AND IF IT EXISTS!
        Method scrapping keys from database.
        """
        #end
        self.DATABASE = self.read_db()
        temp_keys = []
        for key in self.DATABASE[0].keys():
            temp_keys.append(key)
        return temp_keys
    
    def get_txt_keys(self) -> list[dict]:
        #start
        """
        WORKS ONLY FOR .txt FILE AND IF IT EXISTS!
        
        Method scrapping keys from .txt file.
        """
        #end
        if bool(self.structurised_list) != False:
            temp_keys = []
            for key in self.structurised_list[0].keys():
                temp_keys.append(key)
            return temp_keys
                
        else:
            raise owntypes.KeysError("None keys found.")
    
    def save_as_db(self):
        #start
        """WORKS ONLY IF .txt FILE EXISTS!"""
        #end
        if type(self.structurised_list) != owntypes.StructurisedListLikeDBObject:
            raise owntypes.StructurisedLikeDBerror(f'"{self.structurised_list}" have type {type(self.structurised_list)}, not "StructurisedLikeDB"')
        
        with open(self.db_file, "w", encoding="UTF-8") as file:
            file.write("DATABASE = [\n")
            for element in self.structurised_list:
                file.write("\t"+str(element)+",\n")          
            file.write("]"+"\n")
            file.close()
    
    def get_db_last_record_id(self) -> int:
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Gets id of last record.
        
        Last record ALWAYS have the greatest id.
        """
        #end
        return self.read_db()[-1]["id"]
    
    def get_txt_last_record_id(self) -> int:
        #start
        """
        WORKS ONLY FOR .txt FILE AND IF .txt FILE EXISTS!
        
        Gets id of last record.
        
        Last record ALWAYS have the greatest id.
        """
        #end
        return self.read_it_like_db()[-1]["id"]
    
    def get_db_record_by_id(self, id: int) -> owntypes.DatabaseObject:
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Method returning record containing provided id.
        """
        #end
        if self.__is_dummy_record():
            raise owntypes.DatabaseObjectExistence("Database object don't have any added data yet.")
        if type(id) != int:
            raise owntypes.IdError(f"Provided id {id} is not even an integer.")
        if self.get_db_last_record_id() < id:
            raise owntypes.IdError(f"Provided id {id} is greater than the greatest id in database.")
        if id not in self.get_db_all_values_by_key("id"):
            raise owntypes.IdError(f"Record with provided id {id} doesn't exist, it was probably deleted.")

        for record in self.DATABASE:
            if record["id"] == id:
                return record
            
    def get_txt_record_by_id(self, id: int) -> owntypes.StructurisedListLikeDBObject:
        #start
        """
        WORKS ONLY FOR .txt FILE AND IF .txt FILE EXISTS!
        
        Method returning record containing provided id.
        """
        #end
        if type(id) != int:
            raise owntypes.IdError(f"Provided id {id} is not even an integer.")
        if self.get_txt_last_record_id() < id:
            raise owntypes.IdError(f"Provided id {id} is greater than the greatest id in .txt file.")

        for record in self.structurised_list:
            if record["id"] == id:
                return record
    
    def add_record(self, *values: str):
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Method adding a new database record.
        """
        #end
        values = list(values)
        self.database_keys_list = self.get_db_keys()
        try:
            with open(self.db_file, encoding="UTF-8") as file:
                if len(self.database_keys_list) == 0 :
                    raise owntypes.KeysError(f"Can't add record, none keys found in provided {self.db_file} file.")
                elif len(self.database_keys_list)-1 != len(values):
                    raise owntypes.KeysError("Given list of values is shorter or longer than number of all keys.")
                if bool(file.readlines()) == False:
                    raise Exception("File can't be empty, use 'save_as_db' method to create data.")
        except FileNotFoundError:
            raise FileNotFoundError("Provided file doesn't exist.")
        else:
            self.DATABASE = self.read_db()
            if self.DATABASE[0]["id"] == "test":
                self.is_new_db = True
                self.database_keys_list = self.get_db_keys()

            temp_dict = {} 
            if not self.is_new_db:
                last_record_id = self.get_db_last_record_id()
                temp_dict["id"] = last_record_id+1
            else:
                temp_dict["id"] = 0
                self.is_new_db = False
            for index in range(1, len(self.database_keys_list)):
                temp_dict[self.database_keys_list[index]] = values[index-1]
            
            temp_temp_dict = {}
            for record in self.DATABASE:
                temp_temp_dict = self.__scrap_id_from_record(temp_dict)
                temp_record = self.__scrap_id_from_record(record)
                # print(temp_temp_dict, temp_record)
                if temp_temp_dict == temp_record:
                    raise owntypes.DatabaseObjectExistence("You can't store duplicated records, database have existing one like provided record.")
            self.DATABASE.append(temp_dict)
            temp_dict = {}
            self.__delete_record("test")
            self.__save_db_state() 
    
    def update_record(self, id: int, key: str, new_value: float | str):
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Changing value by record id and existing key in record.
        """
        #end
        access = False
        if key == "id":
            raise owntypes.JustSimplestDBAccessDenied("Can't modify record id.")
        else:
            access = True
        if access:
            self.__update_record(id, key, new_value)
    
    def get_db_all_values_by_key(self, key: str) -> owntypes.DatabaseObject:
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Method returing all values existing in database by provided key.
        """
        #end
        if key not in self.database_keys_list:
            raise owntypes.KeysError(f"Key {key} doesn't exist in this database.")
        if not self.is_db_exists:
            raise owntypes.DatabaseObjectExistence("Database object doesn't exist.")
        temp_keys = []
        for record in self.DATABASE:
            temp_keys.append(record[key])
            
        return temp_keys
    
    def get_txt_all_values_by_key(self, key: str) -> owntypes.StructurisedListLikeDBObject:
        #start
        """
        WORKS ONLY FOR .txt AND IF .txt FILE EXISTS!
        
        Method returing all values existing in .txt by provided key.
        """
        #end
        if key not in self.struct_list_keys:
            raise owntypes.KeysError(f"Key {key} doesn't exist in this database.")
        if not self.is_txt_exists:
            raise owntypes.DatabaseObjectExistence("Txt object doesn't exist.")
        temp_keys = []
        for record in self.structurised_list:
            temp_keys.append(record[key])
            
        return temp_keys
   
    def delete_record(self, id: int):
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Method removing record by provided id, this operation CANNOT be undone.
        """
        #end
        if self.get_db_last_record_id() < id:
                raise owntypes.IdError(f"None record with id {id} found.")
        if id not in self.get_db_all_values_by_key("id"):
            raise owntypes.IdError(f"Record with given id {id} doesn't exist.")
        self.__delete_record(id)
    
    def reindex_database(self):
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Method giving new id for each record in database.
        """
        #end
        for index in range(len(self.DATABASE)):
            self.DATABASE[index]["id"] = index
        self.__save_db_state()
    
    def create_standalone_db(self, *keys: str):
        #start
        """
        Method creating standalone database undependly of .txt file.
        """
        #end
        keys = list(keys)
        if self.is_db_exists:
            raise owntypes.JustSimplestDBAccessDenied("Can't create database, cause of existing one.")
        self.DATABASE.append({"id": "test"})
        for key in keys:
            if key == "id":
                raise owntypes.JustSimplestDBAccessDenied("Can't create id key, it's default key.")
            self.DATABASE[0][key] = "test"
        self.is_db_exists = True
        key_check = ""
        for next_selected_index in range(len(keys)):
            key_check = keys[next_selected_index]
            for index in range(len(keys)):
                if index == next_selected_index:
                    continue
                if key_check == keys[index]:
                    raise owntypes.KeysError(f"Can't create {key_check}, it's duplicated.")
        self.__create_dbms_shell()
        self.__save_db_state()
        self.DATABASE = self.read_db()
    
    def db_what_ids(self, key: str, value) -> int:
        #start
        """
        WORKS ONLY FOR DATABASE AND IF DATABASE FILE EXISTS!
        
        Method returning each record id by provided value on provided key.
        """
        #end
        temp_found_ids = []
        if key == "id":
            raise KeyError("Can't find id by itself.")
        for record in self.DATABASE:
            if record[key] == value:
                temp_found_ids.append(record["id"])
        return temp_found_ids
    
    def txt_what_ids(self, key: str, value) -> int:
        #start
        """
        WORKS ONLY FOR .txt file AND IF.txt FILE EXISTS!
        
        Method returning each record id by provided value on provided key.
        """
        #end
        temp_found_ids = []
        if key == "id":
            raise KeyError("Can't find id by itself.")
        for record in self.structurised_list:
            if record[key] == value:
                temp_found_ids.append(record["id"])
        return temp_found_ids
    
    def code(self):
        #start
        """
        Returns JustSimplestDB code.
        """
        #end
        with open(__file__, encoding="UTF-8") as file:
            return file.readlines()
        
    def __update_record(self, id: int, key: str, new_value: float | str):
        '''DEV METHOD'''
        record_id = self.get_db_record_by_id(id)["id"]
        for index, record in enumerate(self.DATABASE):
            if record_id == record["id"]:
                self.DATABASE[index][key] = new_value
                self.__save_db_state()
                break
    
    def __save_db_state(self):
        """DEV METHOD"""
        with open(self.db_file, "w", encoding="UTF-8") as file:
            file.write("DATABASE = [\n")
            for record in self.DATABASE:
                    file.write("\t"+str(record)+",\n")
            file.write("]\n")
            file.close()
        self.DATABASE = self.read_db()
    
    def __delete_record(self, id: int):
        for record_index, record in enumerate(self.DATABASE):
            if record["id"] == id:
                del self.DATABASE[record_index]  # Delete by record identity
                break
        self.__save_db_state()
        if len(self.DATABASE) == 0:
            self.__create_dummy_record()
  
    def __create_dummy_record(self):
        self.DATABASE.append({"id": "test"})
        for key in self.database_keys_list:
            self.DATABASE[0][key] = "test"
        try:
            self.__save_db_state()
        except owntypes.DatabaseObjectExistence:
            pass
        self.__is_dummy_record_var = True
        
    def __is_dummy_record(self):
        try:
            self.DATABASE = self.read_db()
            for record in self.DATABASE:
                if record["id"] == "test":
                    return True
        except owntypes.DatabaseObjectExistence:
            pass
        
        return False
    
    def __scrap_id_from_record(self, record: dict) -> owntypes.DatabaseObject:
        keys = list(record.keys()); keys.pop(0)
        values = list(record.values()); values.pop(0)
        temp_dict = {}
        for index, key in enumerate(keys):
            temp_dict[key] = values[index]
        return temp_dict
    
    def __create_dbms_shell(self):
        if not self.__is_shell_exists:
            with open(self.__shell, "w", encoding="UTF-8") as file:
                file.write(f"file_name = \"{self.main_file}\"\n" + """
import justsimplestdb
_db = justsimplestdb.Instance(file_name)
user_query = ""
performed_query = ""
available_methods_dict = {}

def scrap_methods_and_their_comment():
        methods_list = []
        comments_list = []
        read_file = _db.code()
        for index in range(len(read_file)):
            line = read_file[index]
            line = line[4:]
            if line.startswith("def ") and not "def __" in line:
                line = line[4:]
                line = line.split()
                line[0] = line[0].split("(")
                line[0] = line[0][0]
                methods_list.append(line[0])
            try:
                if '#start' in read_file[index]:
                    comment = ""
                    subindex = 2
                    while not '#end' in read_file[index+subindex]:
                        
                        comment += read_file[index+subindex]
                        subindex += 1
                    comments_list.append(comment[:-5])
            except IndexError:
                pass
        return {"methods_list": methods_list, "comments_list": comments_list}

for i in range(len(scrap_methods_and_their_comment()["methods_list"])):
    available_methods_dict[scrap_methods_and_their_comment()["methods_list"][i]] = scrap_methods_and_their_comment()["comments_list"][i]

def print_available_methods(method_name: str = "all"):
    global available_methods_dict
    available_methods = list(available_methods_dict.keys())
    methods_decription = list(available_methods_dict.values())
    if method_name == 'all':
        print('-'*100)
        for index, method_description in enumerate(methods_decription):
            print()
            print(f'Method name: {available_methods[index]}')
            print('Method description: ')
            print(f'{method_description}')
            print()
        print('-'*100)
    else:
        for index, method_description in enumerate(methods_decription):
            if method_name not in available_methods:
                print(f'No such \"{method_name}\" exists in DBMS methods.')
                break
            if available_methods[index] == method_name:
                print('-'*100)
                print()
                print(f'Method name: {available_methods[index]}')
                print('Method description: ')
                print(f'{method_description}')
                print('-'*100)
                break

while user_query != "exit":
    print()
    user_query = input("Your query: ")
    if user_query == "?" or user_query == "help":
        print_available_methods()
    elif user_query.startswith("?") or user_query.startswith("help"):
        user_query = user_query.split()
        print_available_methods(user_query[1])
    else:
        try:
            exec(
                f'''
import justsimplestdb
db = justsimplestdb.Instance("{file_name}")
executed_query = db.{user_query}
if executed_query != None:
    print(executed_query)
'''
            )
        except Exception as exception:
            print(exception)
            print("If you don\'t know DBMS methods, "+ 'type \"?\" or \"help\" for help.')
            print('You can also get help for specific methods, by typing \"? <method name>\" or \"help <method name>\"(WITHOUT BRACES)')
""")
            self.__is_shell_exists = True
    
    def __delete_chars(self, string: str, num_of_chars: int) -> str:
        '''DEV METHOD
        
        Deletes num_of_chars from the end.'''
        string = string[:-num_of_chars]
        return string
# Author data: 
# 01001010 01100001 01101011 01110101 01100010 00100000 01000001 01101100 01100101 01101011 01110011 01100001 01101110 01100100 01100101 01110010 00100000 01001101 01101001 01100011 01101000 01100001 01101100 01110011 01101011 01101001 00100000 00100010 01001101 00110001 01100011 01101000 00110100 01101100 00110101 01101011 00110001 00100010