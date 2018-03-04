import database
import model
import numpy as np

def main():
    quarter = model.brain(name = 'quarter', input_size = [None, 30, 30, 1], input_size_1 = [-1,30,30,1], output_size = 2)
    quarter.training()

    #print(database.big_test_label)
if __name__ == '__main__':
    main()
