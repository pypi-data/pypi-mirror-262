from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class ConfigParameters:
    """Docstring"""

    config_file: Path

    def __post_init__(self):
        # self.__config = self.__read_config_file()
        self.__validate_config()
        
    @property
    def ptypes(self) -> list[str]:
        return [ptype for ptype in self.__hierarchy["Id"]]
        
    @property
    def id_var(self) -> str:
        return self.__config_parameters.get('id_var')

    @property
    def complete_var(self) -> str:
        return self.__config_parameters.get('repliesVar')
    
    @property
    def min_replies(self) -> int:
        return self.__config_parameters.get('minReplies')

    @property
    def min_diff(self) -> int:
        return self.__config_parameters.get('minDiffrule')
    
    @property
    def __config_parameters(self) -> dict[str, str]:
        return dict(zip(self.__basicconfig['Parameter'],self.__basicconfig['Value']))
        
        
    def __validate_config(self) -> None:
        """Only a basic check for now. Could easily be expanded but important for now."""
        try:
            pd.read_excel(self.config_file, sheet_name=None)
        except FileNotFoundError:
            raise FileNotFoundError(r'Filen med config findes ikke')

        try:
            self.__basicconfig = pd.read_excel(self.config_file, sheet_name='Konfiguration')
            self.__hierarchy = pd.read_excel(self.config_file, sheet_name='Hierarki')
            self.__diffrule = pd.read_excel(self.config_file, sheet_name='Differenceregel')
            self.__aggresults_vars = pd.read_excel(self.config_file, sheet_name='Resultsoversigt_variable')
        except ValueError:
            raise ValueError('Config filen skal som minimum indeholde: Hierarki, Differenceregel, Resultatoversigt & Resultatoversigt_variable')

    def __read_config_file(self) -> pd.DataFrame:
        try:
            return pd.read_excel(self.config_file, sheet_name=None)
        except FileNotFoundError:
            raise FileNotFoundError(r'Filen med config findes ikke')
            

if __name__ == '__main__':
    
    test_path = Path(r'C:\Users\ctf\pq_data\resultatoversigt_data\Setup_file_example.xlsx')
    
    test = ConfigParameters(test_path)
    print(test.id_var)
    print(test.ptypes)
    print(test.min_replies)
    print(test.min_diff)
