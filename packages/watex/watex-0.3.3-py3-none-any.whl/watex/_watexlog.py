# -*- coding: utf-8 -*-
#   License: BSD-3-Clause
#   Author: LKouadio <etanoyau@gmail.com>
#   Created on Tue May 18 12:53:48 2021

"""
`WATex`_ Logger 
================

Module to track bugs and issues, and also deal with all exceptions in 
:mod:`~.exceptions`.
 
"""

import os 
import yaml
import logging 
import logging.config
import inspect 

class watexlog:
    """
    Field to logs  module Files  in order to tracks all exceptions.
    
    """
    
    @staticmethod
    def load_configure (
            path2configure =None, 
            OwnloggerBaseConf=False, 
            verbose=False, 
            ) :
        """
        configure/setup the logging according to the input configfile

        :param configfile: .yml, .ini, .conf, .json, .yaml.
        Its default is the logging.yml located in the same dir as this module.
        It can be modified to use env variables to search for a log config file.
        """
        
        configfile=path2configure
        
        if configfile is None or configfile == "":
            if OwnloggerBaseConf ==False :
                logging.basicConfig()
            else :
                watexlog().set_logger_output()
            
        elif configfile.endswith(".yaml") or configfile.endswith(".yml") :
            this_module_file=os.path.abspath(__file__)

            if verbose:
                print('yaml config file', this_module_file) 
            
            if verbose :
                print('os.path.dirname(this_module_path)=',
                  os.path.dirname(this_module_file)) 

            yaml_path=os.path.join(os.path.dirname(this_module_file),
                                   configfile)
    
            if verbose: 
                print(f"Effective yaml configuration file {yaml_path!r}") 
            if os.path.exists(yaml_path) :
                # try : 
                with open (yaml_path,"rt") as f :
                    config=yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                # except : 
                #     with open (os.path.dirname (yaml_path),"rt") as f :
                #         config=yaml.safe_load(f.read())
                #     logging.config.dictConfig(config)
            else :
                logging.exception(
                    "the config yaml file %s does not exist?", yaml_path)
                
        elif configfile.endswith(".conf") or configfile.endswith(".ini") :
            logging.config.fileConfig(configfile,
                                     disable_existing_loggers=False)
            
        elif configfile.endswith(".json") :
            pass 
        else :
            logging.exception(
                "logging configuration file %s is not supported" %configfile)
            
    
    @staticmethod        
    def get_watex_logger(
            loggername=''
            ):
        """
        create a named logger (try different)
        :param loggername: the name (key) of the logger object in this 
        Python interpreter.
        :return: logger 
        """
        return logging.getLogger(loggername) # logger 
 

    @staticmethod
    def load_configure_set_logfile (
            path2configfile=None, 
            configfile ='wlog.yml', 
            app = 'watex'
            ): 
        """
        configure/setup the logging according to the input configure .yaml file.

        :param configfile: .yml, or add ownUsersConfigYamlfile (*.yml) 
            Its default is the logging.yml located in logfiles folder 
            It can be modified to use env variables to search for a log 
            config file.
        :param path2configfile: path to logger config file 
        :param app: application name. Use to set the variable environnment. 
        
        """
        
        ownUserLogger=configfile
        
        if path2configfile is None :
            env_var=os.environ[app]
            path2configfile =os.path.join( env_var, app, ownUserLogger)
            
        elif path2configfile is not None :
            if os.path.isdir(os.path.dirname(path2configfile)):
                if path2configfile.endswith(
                        '.yml') or path2configfile.endswith('.yaml'):
                    
                    logging.info(
                        'Effective yaml configuration file'
                        ' :%s' %path2configfile)
                else :
                    logging.exception(
                        'File provided {%s}, is not a .yaml config file '
                        '!'%os.path.basename(path2configfile))
            else :
                
                logging.exception ('Wrong path to .yaml config file.')
        
        yaml_path=path2configfile
        os.chdir(os.path.dirname(yaml_path))
        if os.path.exists(yaml_path) :
            with open (yaml_path,"rt") as f :
                config=yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else :
            logging.exception(
                "the config yaml file %s does not exist?", yaml_path) 
            
    @staticmethod
    def set_logger_output(
            logfilename="watex.log", 
            date_format='%m %d %Y %I:%M%S %p',
            filemode="w",
            format_="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.DEBUG 
            ):
        """
        
        Parameters
        ----------
        * logfilename : str, optional
            logfilename output. The default is "LogFileTest.log".
        * date_format :str, 
            format of date . consult module time. The default is 
            '%m %d %Y %I:%M%S %p'.
        * filemode : str, 
            mode to write the out[ut file. Must be ["a","w", "wt',"wt"].
            the default is "a".
        * format_ : str,
            format of date and time. Must consult the module of datetime.
            The default is '%s(asctime)s %(message)s'.
        * level : object, optional
                    logging object.  Must be C.E.W.I.D :
                        >>> logging.CRITICAL
                        >>> Logging.ERROR
                        >>> logging.WARNING
                        >>> logging.INFO
                        >>> logging.DEBUG
                    The default is logging.DEBUG.

        Returns : NoneType object
        -------
        Procedure staticFunctions

        """
        # #create logger 
        # logger=logging.getLogger(__name__)
        logger=watexlog.get_watex_logger(__name__) 
        logger.setLevel(level)
        
        # #create console handler  and set the level to DEBUG 
        ch=logging.StreamHandler()
        ch.setLevel(level) # level=logging.DEBUG
        
        #create formatter :
        formatter =logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        #add Formatter to ch 
        ch.setFormatter(formatter)
        
        #add ch to logger 
        logger.addHandler(ch)
        
        # logging.basicConfig(filename="test.log", level=logging.DEBUG)
        logging.basicConfig(filename=logfilename, format=format_,
                            datefmt=date_format,
                            filemode=filemode, level=level)
        logging.debug("debug message")
        logging.info("info message ")
        logging.warning("warn message")
        logging.error("error message")
        logging.critical("critical message")

        
def test_yaml_configfile(yamlfile="wlog.yml"):
    
    this_func_name = inspect.getframeinfo(inspect.currentframe())[2]

    UsersOwnConfigFile = yamlfile
    watexlog.load_configure(UsersOwnConfigFile)
    logger = watexlog.get_watex_logger(__name__)
    
    print((logger,
           id(logger),
           logger.name,
           logger.level,
           logger.handlers
           ))
    
    # 4 use the named-logger
    logger.debug(this_func_name + ' __debug message')
    logger.info(this_func_name + ' __info message')
    logger.warn(this_func_name + ' __warn message')
    logger.error(this_func_name + ' __error message')
    logger.critical(this_func_name + ' __critical message')

    print(("End of: ", this_func_name))
    
if __name__=='__main__':
    # ownerlogfile = '/watex/wlog.yml'
    # watexlog().load_configure(path2configure='wlog.yml')
    
    # watexlog().get_watex_logger().error('First pseudo test error')
    # watexlog().get_watex_logger().info('Just a logging test')
    
    print(os.path.abspath(watexlog.__name__))
    

    
    
    
    
    