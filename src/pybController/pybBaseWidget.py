class pybBaseWidget():
    
    ARG_APPEND = 0 # append argument list
    ARG_EXEC = 1  # execute argument immediately
    
    
    def getLayout(self):
        return self.layout

    def getWidget(self):
        return self.widget
    
    def formatArg(self,arg):
        # To implement, format arguments
        # default is no format
        return arg
    
    def formattedArgs(self,argList):
        f_arg = []
        for arg in argList:
            f_arg.append(self.formatArg(arg))
        return f_arg
        
    def getArg(self):
        # TODO
        argList = []
        if len(self.execute) > 0:
            formatted = self.formattedArgs(self.execute)
            argList.append((self.ARG_EXEC,formatted))
                
        if len(self.args) > 0:
            formatted = self.formattedArgs(self.args)
            argList.append((self.ARG_APPEND,formatted))
            
        return argList
    
    def __init__(self,element):
        # extract information
        self.args = [] # argument list
        self.widget = None
        self.layout = None
        
        self.label = None
        self.default = None
        self.execute = []

        # standard elements
        if element.find("label") is not None:
            self.label = element.find("label").text
        if element.find("default") is not None:
            self.default = element.find("default").text
            
        self.execute = [i.text for i in element.findall("exec")]
        self.args = [i.text for i in element.findall("arg")]
        