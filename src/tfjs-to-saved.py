import os
import sys
import glob
import tensorflow as tf
import tfjs_graph_converter.api as tfjs

graphDir = 'models/'
savedDir = 'saved/'
tfliteDir = 'tflite/'

def main() -> None:
  for f in glob.glob(os.path.join(graphDir, '*.json')):
    modelName = os.path.basename(f).split('.')[0]
    print('graph model: ' + modelName + ' path: ' + f)
    savedModel = os.path.join(savedDir, modelName)
    try:
      tfjs.graph_model_to_saved_model(f, savedModel)  # type: ignore
    except:
      print('saved convert failed')
    else:
      converter = tf.lite.TFLiteConverter.from_saved_model(savedModel)
      converter.optimizations = [tf.lite.Optimize.DEFAULT]
      converter.target_spec.supported_ops = [ tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS ]
      converter.target_spec.supported_types = [tf.float16]
      tfliteModel = os.path.join(tfliteDir, modelName)
      try:
        tflite_model = converter.convert()
      except:
        print('tflite convert failed')
      else:
        with open(tfliteModel, 'wb') as f:
          f.write(tflite_model)
        print('saved:' + savedModel + ' tflite: ' + tfliteModel)

if __name__ == '__main__':
  main()
