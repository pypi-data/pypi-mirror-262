from phootlogger import logger

msg = logger.messages(__name__)

def testing():
    msg.error( "error message here." )
    msg.warning( "warning message here." )
    msg.system( "normal message here." )
    msg.quit_script()
    return



def main():
    testing()
    return

if __name__ == "__main__":
    main()
