"""
Functions
"""

import pandas as pd

### 1.0 Converting a GDX file to a pandas dataframe
def symbol_to_df(db, symbol, cols='None', parameter_or_set='parameter'):
    """
    Loads a symbol from a GDX database into a pandas dataframe

    Args:
        db (GamsDatabase): The loaded gdx file
        symbol (string): The wanted symbol in the gdx file
        cols (list): The columns
        parameter_or_set (str): Choose either 'parameter' or 'set'
    """   
    if parameter_or_set == 'parameter':
        df = dict( (tuple(rec.keys), rec.value) for rec in db[symbol] )
        df = pd.DataFrame(df, index=['Value']).T.reset_index() # Convert to dataframe
    elif parameter_or_set == 'set':
        df = dict( (tuple(rec.keys) ) for rec in db[symbol] )
        df = pd.DataFrame(dict( (tuple(rec.keys)) for rec in db[symbol] ), index=['Set']).T.reset_index()
    else:
        print('Choose either parameter or set!')

    if cols != 'None':
        try:
            df.columns = cols
        except:
            pass
    return df 

class IncFile:
    """A useful class for creating .inc-files for GAMS models
    Args:
    prefix (str): The first part of the .inc file.
    body (str): The main part of the .inc file.
    suffix (str): The last part of the .inc file.
    name (str): The name of the .inc file.
    path (str): The path to save the file, defaults to 'Balmorel/base/data'.
    """
    def __init__(self, prefix='', body='', suffix='',
                 name='name', path='Balmorel/base/data/'):
        self.prefix = prefix
        self.body = body
        self.suffix = suffix
        self.name = name
        self.path = path
    
    def body_concat(self, df):
        """Concatenate a df to the df in the body
        """
        self.body = pd.concat((self.body, df)) # perhaps make a IncFile.body.concat function..
 
    def save(self):
        if self.path[-1] != '/':
            self.path += '/'
        if self.name[-4:] != '.inc':
            self.name += '.inc'  
       
        with open(self.path + self.name, 'w') as f:
            f.write(self.prefix)
            f.write(self.body)
            f.write(self.suffix)
 
def read_lines(name, file_path, make_space=True):
   
    if make_space:
        string = '\n' + ''.join(open(file_path + '/%s'%name).readlines()) + '\n'
    else:
        string = ''.join(open(file_path + '/%s'%name).readlines())
   
    return string