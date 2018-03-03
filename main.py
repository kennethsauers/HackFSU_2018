import numpy as np
import config
import database
import model
import tester_1
import tester_2

lr = np.arange(.03,.15,.01)



if __name__ == '__main__':
    name = model.agent('kenneth')
    name.train_for(1)
    name.save()
    print(name.predict(database.test_x[87].reshape([-1,28,28,1])))
