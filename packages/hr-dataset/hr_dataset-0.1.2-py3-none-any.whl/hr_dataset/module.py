from dataclasses import dataclass

import pandas as pd
from functions.file_handler import InputFile
from config.config_parser import ConfigParameters
from differenceregel.differenceregel import beregn_differenceregel, calculate_diffrule


@dataclass
class HRDataset:
    """Docstring - to be continued"""
    input_dir: str
    output_dir: str
    config_file: str
    data_file: str
    
    def __post_init__(self):
        self.__validate_inputs()
        self.__config = self.__parse_config_file()
        self.dataset = self.__load_dataset()
        
    def __parse_config_file(self) -> ConfigParameters:
        return ConfigParameters(self.cf_file.full)
    
    def __load_dataset(self) -> pd.DataFrame:
        if self.data.file_type == '.csv':
            # df = pd.read_csv(self.data.full, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
            try:
                df = pd.read_csv(self.data.full, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(self.data.full, encoding='ansi', sep=';', decimal=',', low_memory=False)
        return df
        
    def __validate_inputs(self) -> None:
        self.cf_file = InputFile(self.input_dir, self.config_file)
        self.data = InputFile(self.input_dir, self.data_file)

        if not self.cf_file.valid and not self.data.valid:
            raise ValueError('Invalid inputfiles - check directory and filenames')

        if self.cf_file.file_type != '.xlsx':
            raise ValueError('Config file has to be a xlsx file')        
        
    def run_diff_rule(self) -> pd.DataFrame:
        diff_df = calculate_diffrule(
            df=self.dataset,
            ptypes=self.__config.ptypes,
            id_var=self.__config.id_var,
            replies_var=self.__config.complete_var,
            diff_limit=self.__config.min_diff,
            report_limit=self.__config.min_replies            
        )
        return diff_df
        
if __name__ == '__main__':
    hr_projekt = HRDataset(
        input_dir=r'C:\Users\ctf\pq_data\resultatoversigt_data',
        output_dir=r'C:\Users\ctf\pq_data\resultatoversigt_data',
        config_file=r'Setup_file_example.xlsx',
        data_file=r'Hedensted_2023_dataset.csv'
    )
    diff_dataset = hr_projekt.run_diff_rule()