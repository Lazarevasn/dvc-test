from keras import models
from keras.preprocessing.image import ImageDataGenerator
from dvclive import Live
from dvclive.keras import DVCLiveCallback

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    './data/test',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

model = models.load_model('./bird-rec-model/')


with Live(dir='live/eval', save_dvc_exp=False) as live:
    eval_results=model.evaluate(test_generator, callbacks=[DVCLiveCallback(live=live)])

    live.log_metric("test_loss", eval_results[0])
    live.log_metric("test_accuracy", eval_results[1])
    live.log_metric("test_precision", eval_results[2])
    live.log_metric("test_recall", eval_results[3])

    y_pred = model.predict(test_generator)
    y_true = test_generator.classes
    live.log_sklearn_plot("confusion_matrix", y_true, y_pred.argmax(axis=1))
