import os
import inspect
from importlib import import_module

from fastapi import FastAPI
from turbo_boot.config_loader import ConfigLoader
from turbo_boot.logging import Logger

def convert_filename_to_classname(filename):
    if '_' in filename:
        words = filename.split('_')
        capitalized_words = [word.capitalize() for word in words]
        class_name = ''.join(capitalized_words)
        return class_name
    return filename

def build_application(application_path: str):
    if application_path is None:
        raise ValueError("application_path can not be None")
    
    app = FastAPI()
    
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

class TurboBoot:
    
    @staticmethod
    def get_app(application_path: str = None):
        if application_path is None:
            application_path = os.getcwd()
        
        app = build_application(application_path)
        
        return app

    @staticmethod
    def get_config_loader(config_file_path: str = None) -> ConfigLoader:
        if config_file_path is None:
            config_file_path = os.path.join(os.getcwd(), 'resources', 'application.yaml')
        
        config_loader = ConfigLoader(config_file_path=config_file_path)
        
        return config_loader

    @staticmethod
    def get_logger(config_loader: ConfigLoader) -> Logger:
        if config_loader is None:
            raise ValueError()
        
        logger = Logger(config_loader = config_loader)
        
        return logger