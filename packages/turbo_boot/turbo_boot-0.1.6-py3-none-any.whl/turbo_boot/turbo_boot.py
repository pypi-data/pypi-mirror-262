import os
import inspect
from importlib import import_module

from fastapi import FastAPI
from turbo_boot.config_loader import ConfigLoader
from turbo_boot.logging import Logger
from typing import Optional, Dict

Any = object()

def convert_filename_to_classname(filename):
    if '_' in filename:
        words = filename.split('_')
        capitalized_words = [word.capitalize() for word in words]
        class_name = ''.join(capitalized_words)
        return class_name
    return filename

def build_application(application_path: str, fast_api_app_configs: Optional[Dict[str, Any]] = None):
    if application_path is None:
        raise ValueError("application_path can not be None")
    
    arguments_to_remove = ['self']
    argument_list = list(inspect.signature(FastAPI.__init__).parameters.keys())
    filtered_arguments = [arg for arg in argument_list if arg not in arguments_to_remove]
    parameters = {}
    for argument in filtered_arguments:
        if argument in fast_api_app_configs:
            parameters[argument] = fast_api_app_configs[argument]
    app = FastAPI(**parameters)
    
    for root, dirs, files in os.walk(application_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__') and file != "main.py":
                module_name = os.path.relpath(os.path.join(root, file), application_path)
                module_name = module_name.replace(os.path.sep, '.')[:-3]
                
                try:
                    module = import_module(module_name)
                    class_info = {key: value for key, value in inspect.getmembers(module, inspect.isclass)}
                    class_name = convert_filename_to_classname(module_name.split(".")[-1])
                    
                    if class_name in class_info.keys():
                        if "__api_router__" in class_info[class_name].__dict__.keys():
                            app.include_router(class_info[class_name].__dict__["__api_router__"])
                except ImportError as e:
                    print(f"Error loading module '{module_name}': {e}")

    return app

def get_config_loader(config_file_path: str = None) -> ConfigLoader:
    if config_file_path is None:
        config_file_path = os.path.join(os.getcwd(), 'resources', 'application.yaml')
    
    config_loader = ConfigLoader(config_file_path=config_file_path)
    
    return config_loader

def get_logger(config_loader: ConfigLoader) -> Logger:
    if config_loader is None:
        raise ValueError()
    
    logger = Logger(config_loader = config_loader)
    
    return logger

class TurboBoot:
    config_loader = None
    logger = None
    app = None
    
    @staticmethod
    def setup(application_path: str = None, config_file_path: str = None, fast_api_app_configs: Optional[Dict[str, Any]] = None):
        if application_path is None or len(application_path.strip()) < 1:
            raise ValueError("application_path can be None or empty")
        
        TurboBoot.config_loader = get_config_loader(config_file_path=config_file_path)
        
        TurboBoot.logger = get_logger(config_loader=TurboBoot.config_loader)
        
        TurboBoot.app = build_application(application_path, fast_api_app_configs)
    
    @staticmethod
    def get_logger():
        return TurboBoot.logger._Logger__logger

    @staticmethod
    def get_app():
        return TurboBoot.app

    @staticmethod
    def get_config_loader():
        return TurboBoot.config_loader