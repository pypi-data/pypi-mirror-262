# %%

from dataclasses import dataclass
import os
from pathlib import Path
import pandas as pd
from functions.file_handler import InputFile


@dataclass
class Resultatoversigt:
    """Docstring"""

    input_dir: str
    output_dir: str
    config_file: str
    data_file: str

    def __post_init__(self):
        self.__validate_inputs()
        self.__validate_config()

    def __validate_inputs(self):
        self.cf_file = InputFile(self.input_dir, self.config_file)
        self.data = InputFile(self.input_dir, self.data_file)

        if not self.cf_file.valid and not self.data.valid:
            raise ValueError('Invalid inputfiles - check directory and filenames')

        if self.cf_file.file_type != '.xlsx':
            raise ValueError('Config file has to be a xlsx file')

    def __validate_config(self):
        # Trying to read the required sheets
        try:
            levels = pd.read_excel(self.cf_file.full, sheet_name='Hierarki')
            config = pd.read_excel(self.cf_file.full, sheet_name='Resultatoversigt')
            agg_variables = pd.read_excel(self.cf_file.full, sheet_name='Resultatoversigt_variable')
        except:
            # Ugly temporary exception
            print('hov')

        # Tjekker om alle relevante parametre er angivet i filen
        config_parameters = dict(zip(config['Parameter'], config['Value']))
        filter_parameters = dict(zip(filters['FilterVar'], filters['FilterValue']))
        ptypes = [ptype for ptype in levels['Id']]
        ptypets = [ptypet for ptypet in levels['Name']]
        config_levels = [level for level in levels["Label"]]
        renames = dict(zip(levelsSheet["Name"],levelsSheet["Label"]))
        renames.update(dict(zip(aggVariablesSheet["Name"],aggVariablesSheet["Label"])))
        renames.update(dict(zip(aggVariablesSheet["Theme"],aggVariablesSheet["ThemeLabel"])))
        




if __name__ == '__main__':
    test = Resultatoversigt(
        input_dir=r'C:\Users\ctf\pq_data\resultatoversigt_data',
        output_dir=r'C:\Users\ctf\pq_data\resultatoversigt_data',
        config_file=r'Setup_file_example.xlsx',
        data_file=r'Dataset_utf8_full.csv'
    )



