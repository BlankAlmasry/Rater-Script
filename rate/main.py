from __future__ import print_function, unicode_literals

import os
import sys
from os.path import isfile

from rate.calculator import Calculator
from rate.gui import GUI
from rate.readers import ReaderFactory
from rate.utils import ResultHandler
from rate.writers import WriterFactory
from rate.config import supported_algorithms, supported_writers, supported_readers


def generate(file, player_a_index, player_b_index, result_a_index,
             algorithm_name, output_format,
             result_win, result_loss, result_draw):
    file_name, file_extension = os.path.splitext(file)

    # create reader
    columns_indexes = [player_a_index, player_b_index, result_a_index]
    reader = ReaderFactory.create_reader(file_extension, file, columns_indexes)

    # create writer
    output_file_name = file_name + "_" + algorithm_name + "." + output_format
    writer = WriterFactory.create_writer(output_file_name, headers=["file_name", "rating"])

    # create result handler to handle results according to the user specifications
    result_handler = ResultHandler(result_win, result_loss, result_draw)

    # start calculation
    calculator = Calculator(reader,
                            writer,
                            algorithm_name if algorithm_name != 'all' else supported_algorithms,
                            result_handler)
    calculator.calculate()
    del calculator


def main():
    # example answers
    # answers = {
    #     'file': 'fights.json',
    #     'player_a_index': '0',
    #     'player_b_index': '1',
    #     'result_a_index': '2',
    #     'algorithm_name': 'all',
    #     'output_format': 'csv',
    #     'result_win': 'Win',
    #     'result_loss': 'loss',
    #     'result_draw': 'Draw',
    # }

    try:
        file = sys.argv[1:][0]
    except IndexError:
        print("Please provide a file name")
        exit(1)
    if not isfile(file):
        print("File does not exist")
        exit(1)
    if file.split(".")[-1] not in supported_readers:
        print(f"File format is not supported, please use one of the following: {supported_readers}")
        exit(1)

    answers = GUI.display(supported_writers, supported_algorithms)
    if answers['algorithm_name'] == 'all':
        for algorithm in supported_algorithms:
            print(f"Computing {answers['algorithm_name']} ratings...")
            answers["algorithm_name"] = algorithm
            generate(**answers)
    else:
        print(f"Computing {answers['algorithm_name']} ratings...")
        generate(**answers)
    print("Done")


if __name__ == '__main__':
    main()