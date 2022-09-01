import os
import glob
import tensorflow as tf
import tfjs_graph_converter.api as tfjs

graphDir = 'models/'
savedDir = 'saved/'
tfliteDir = 'tflite/'

def saved2tflite(savedModelDir, tfliteModelName):
  if (os.path.isfile(os.path.join(savedModelDir, 'saved_model.pb'))):
    converter = tf.lite.TFLiteConverter.from_saved_model(savedModelDir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT] # type: ignore
    converter.target_spec.supported_ops = [ tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS ]
    # converter.target_spec.experimental_supported_backends = ["CPU", "GPU"]
    converter.target_spec.supported_types = [tf.float16]
    converter.allow_custom_ops = True
    converter.exclude_conversion_metadata = True
    try:
      tfliteModel = converter.convert()
      # tf.lite.experimental.Analyzer.analyze(model_content = tfliteModel)
    except:
      print('  tflite convert failed')
    else:
      with open(tfliteModelName, 'wb') as f:
        f.write(tfliteModel)
      print('  tflite model', tfliteModelName)
  else:
    print('  tf saved model missing:', savedModelDir)


def tfjs2saved(graphJsonFile, savedModelDir):
  if (not os.path.exists(savedModelDir)):
    try:
      tfjs.graph_model_to_saved_model(graphJsonFile, savedModelDir) # type: ignore
    except:
      print('  tf saved convert failed:', graphJsonFile)
    else:
      print('  tf saved model:', savedModelDir)
  else:
    print('  tf saved model exists:', savedModelDir)


def main():
  tf.compat.v1.enable_control_flow_v2()
  for graphJsonFile in glob.glob(os.path.join(graphDir, '*.json')):
    modelName = os.path.basename(graphJsonFile).split('.')[0]
    print('model:', modelName)
    print('  tfjs graph model:', graphJsonFile)
    savedModelDir = os.path.join(savedDir, modelName)
    tfliteModelFile = os.path.join(tfliteDir, modelName) + '.tflite'
    tfjs2saved(graphJsonFile, savedModelDir)
    saved2tflite(savedModelDir, tfliteModelFile)


if __name__ == '__main__':
  main()
