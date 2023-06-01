

def split_last(txt:str,char:str):
    if char not in txt : return txt
    index = txt.rfind(char)
    return [txt[:index] , txt[index+1:]]

def split_first(txt:str,char:str):
    if char not in txt : return txt
    index = txt.find(char)
    return [txt[:index] , txt[index+1:]]


class C_arg:
    name : str
    type : str = '???'
    type_allias : str = None
    default_value : str = None
    new_line_before : bool = True
    
    def __init__(self,arg_str:str) -> None:
        self.arg_str = arg_str
        self.sanitize()
        self.split_arg_str()
        self.use_type_allias()

    def sanitize(self):
        self.arg_str = self.arg_str.replace('\t','')
        self.arg_str = self.arg_str.replace(' ','')

    def split_arg_str(self):
        arg_str = self.arg_str.replace(' ','')
        self.new_line_before = arg_str[0] == '\n' 
        arg_str = arg_str.replace('\n','')

        match split_first(arg_str,'='):
            case arg_,default_value : self.default_value = default_value
            case arg_ : pass

        match split_first(arg_,':'):
            case name,type_ : self.type = type_ ; self.name = name
            case name : self.name = name

    def use_type_allias(self):
        match self.type :
            case "np.ndarray" : self.type_allias = "Array"
            case "pd.DataFrame" : self.type_allias = "DataFrame"
    
    @property
    def type_or_allias(self):
        if self.type_allias is not None : return self.type_allias
        else : return self.type

    def __repr__(self) -> str:
        return (f"name = {self.name}\n"+
                f"type = {self.type}\n"+
                f"type_allias = {self.type_allias}\n"+
                f"default_value = {self.default_value}\n"+
                f"new_line_before = {self.new_line_before}")

class func_doc :
    func_str : str
    l_args : list[C_arg]
    name : str

    def __init__(self,func_str) -> None:
        self.func_str = func_str
        self.find_args()
        self.sanitize_args()
        self.find_name()


    def sanitize_args(self):
        new_l_args = []
        for arg in self.l_args : 
            if arg.name != 'self': new_l_args.append(arg)
        self.l_args = new_l_args

    def find_args(self):
        i_args_start = self.func_str.find('(')
        i_args_end = self.func_str.rfind(')')
        args_str = self.func_str[i_args_start+1:i_args_end]

        self.l_args = []
        arg_str = None
        for arg_str_ in args_str.split(','):
            if arg_str is None : arg_str = arg_str_
            else : arg_str += f',{arg_str_}'
            check_1 = (arg_str.count('(') - arg_str.count(')'))==0
            check_2 = (arg_str.count('[') - arg_str.count(']'))==0
            check_3 = (arg_str.count('{') - arg_str.count('}'))==0
            check_4 = (arg_str.count('\"') - arg_str.count('\"'))==0
            check_5 = (arg_str.count('\'') - arg_str.count('\''))==0
            if check_1 and check_2 and check_3 and check_4 and check_5: 
                self.l_args.append(C_arg(arg_str))
                arg_str = None

    def find_name(self): 
        func_str = self.func_str
        index_start = func_str.find('def')+4
        index_end = func_str.find('(')
        self.name = func_str[index_start:index_end]

    def write_doc(self):
        doc = "\n\"\"\"\n"
        doc += "Args\n"
        doc += "----\n"
        for arg in self.l_args :
            doc += f"- `{arg.name}` : {arg.type_or_allias}" 
            if arg.default_value is not None :
                doc += f" (default = {arg.default_value})"
            doc += '\n'
        doc += "\nReturns\n"
        doc += "-------\n"
        doc += "- `________` : ???\n"
        doc += "\"\"\""
        return doc.replace('\n','\n    ')




def sanitize(func_str:str):
    new_func_str = func_str.replace('def ','**special_def**')
    new_func_str = new_func_str.replace('\n','')
    new_func_str = new_func_str.replace('\t','')
    new_func_str = new_func_str.replace(' ','')
    new_func_str = new_func_str.replace('**special_def**','def ')
    return new_func_str