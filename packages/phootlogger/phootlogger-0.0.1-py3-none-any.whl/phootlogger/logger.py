# Modules
import sys
import re
import inspect
from pathlib import Path
# using datetime module
import datetime;

class messages:

    def __init__( self, file_name ):
        self._max_character_length = 10
        self._message_type = ""
        self._user_message = ""
        self._file_name = ""
        self.setFileName( file_name )
        return

    def error( self, msg ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        funcname = module.__name__

        if not self.printUserMessage( filename, funcname, "ERROR", msg ):
            self.quit_script()

        return


    def warning( self, msg ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        funcname = module.__name__

        if not self.printUserMessage( filename, funcname,"WARNING", msg ):
            self.quit_script()

        return


    def system( self, msg ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        funcname = module.__name__
    
        if not self.printUserMessage( filename, funcname, "SYSTEM", msg ):
            self.quit_script()

        return


    def quit_script( self ):

        print( "Exiting script.")
        exit(1)


    def printUserMessage( self, file_name, func_name, msg_type, msg_to_user ):

        # Formats the message type then sets it
        if not self.setMessageType( msg_type ):
            return False

        # replaces all newlines with new lines and a tab
        msg_to_user = re.sub( "\n", "\n\t\t", msg_to_user )

        self.setUserMessage( file_name, func_name, msg_to_user )

        print( self.getUserMessage() )

        return True


    def getFileNameAndFunction( self ):
        caller_path = Path(inspect.stack()[1][1])
        print(f'{caller_path.name}: ')
        return


    def getMessageType( self ):
        return self._message_type


    def setMessageType( self, message_type ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        # Checks the message length
        length = len( message_type )
        if( length > self._max_character_length ):
            print( __name__ + ": ["+ str( length ) + "] is too many character. Max is [" + max_character_length + "]." )
            return False

        # Sets everything to spaces, with one extra space for a ':' at the end
        formatted_message_type = ""
        for curr in range( self._max_character_length + 1 ):
            formatted_message_type += " "

        # Formats the message type
        for curr in range( len( message_type ) ):
            formatted_message_type = formatted_message_type[ :curr ] +  message_type[ curr ] + formatted_message_type[ curr+1: ]

        formatted_message_type = formatted_message_type[ :( len( message_type )) ] + ":" + formatted_message_type[ ( len( message_type ) + 1): ]

        self._message_type = formatted_message_type

        return True


    def setUserMessage( self, file_name, func_name, message ):
        """
        Description:    
        Arguments:      
        Returns:        
        """

        self._user_message = self.getTimeStamp() + ": '" + file_name + "' : '" + func_name + "' : " + self.getMessageType() + message

        return True

    def getUserMessage( self ):
        return self._user_message

    def setFileName( self, name ):
        self._file_name = name
        return

    def getFileName( self ):
        return self._file_name

    def getTimeStamp( self ):
        ct = str( datetime.datetime.now() )
        #print( "timestamp: " + ct + "\n" )

        return ct
