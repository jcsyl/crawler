import numpy as np
import tensorflow as tf
import pandas as pd
a = np.array([1,2,3,4,5,6,7,8,9,11,12,13]).reshape((2,2,3))
print(a)
print(tf.Session() .run(tf.stack(list(a),axis=2)))

df = pd.DataFrame({'key1':['a', 'a',  'b', 'b', 'a'],

	'key2':['one', 'two',  'one', 'two', 'one'],

	'data1':np.random.randn(5),

	'data2':np.random.randn(5)})

print(df.head().values)