import database
import model
import numpy as np

def main():
    network = model.brain(name = 'my_cool_model')
    network.train_for(training_epochs = 5)
if __name__ == '__main__':
    main()
