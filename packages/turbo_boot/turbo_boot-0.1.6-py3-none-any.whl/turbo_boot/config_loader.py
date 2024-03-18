import yaml
import os
from turbo_boot.singleton_meta import SingletonMeta

class ConfigLoader(metaclass=SingletonMeta):
    def __init__(self, config_file_path: str) -> None:
        self.__yaml_data = None
        self.config_file = config_file_path
        self.__load_config()
    
    def __load_config(self):
        with open(self.config_file, 'r') as yaml_file:
            self.__yaml_data = yaml.safe_load(yaml_file)
    
    def get_config(self, key: str):
        return self.__get_yaml_value_with_env_substitution(self.__yaml_data, key)

    def __get_yaml_value_with_env_substitution(self, yaml_data, path):
        keys = path.split('.')
        value = yaml_data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, None)
                if value is None:
                    return None
            else:
                return None
        return self.__substitute_env_variables(value)

    def __substitute_env_variables(self,value):
        if isinstance(value, str):
            parts = value.split(':$')
            if len(parts) == 2 and parts[1].startswith('{') and parts[1].endswith('}'):
                env_var = parts[1][2:-1]
                return os.environ.get(env_var, parts[0])
        return value