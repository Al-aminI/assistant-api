import pandas as pd

from io import StringIO
import sys
from typing import Dict, Optional
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

def preprocess_value(value):
    """
    This function takes a value and returns a preprocessed version of it.

    Parameters
    ----------
    value : Any
        The value to preprocess.

    Returns
    -------
    Any
        The preprocessed value.

    """
    if isinstance(value, str):
        return value.strip().lower()
    return value

class PythonREPL:
    """Simulates a standalone Python REPL."""

    def __init__(self):
        """
        Initialize a new PythonREPL instance.

        Returns
        -------
        None
            This function does not return any values.
        """
        pass        

    def run(self, command: str, df) -> str:
        """
        Runs the given command in the Python REPL and returns any printed output.

        Parameters
        ----------
        command : str
            The command to run.
        df : pandas.DataFrame
            The input DataFrame.

        Returns
        -------
        str
            Any printed output from the command.

        """
        
        df_cleaned = df.applymap(preprocess_value)
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        local_vars = {"df": df_cleaned}
        try:
            exec(command, globals(), local_vars)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = "ERROR "+str(e)
            
        # sys.stderr.write("PYTHON OUTPUT: \"" + output + "\"\n")
        return output




def execute_step(code):
    """
    Runs the given code in the Python REPL and returns any printed output.

    Parameters:
        code
    Returns:
        output of the exwcution
    """
    repl = PythonREPL()
    
    # Call the run method with a command as an argument
    output = repl.run(code)
    return output