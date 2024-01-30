from keras import layers, models, metrics
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
from keras import optimizers
import dvc.api
from dvclive import Live
from dvclive.keras import DVCLiveCallback

# Загрузка предварительно обученной модели InceptionV3 без верхних слоев
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Добавление своих слоев поверх предварительно обученной модели
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(7, activation='softmax')  # 7 классов для видов птиц
])

# Заморозка весов предварительно обученной модели
base_model.trainable = False

# Компиляция модели
model.compile(optimizer=optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy', metrics.Precision(), metrics.Recall()])

# Создание генератора данных для обучения
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.5, zoom_range=0.5, 
                                   horizontal_flip=True)
train_dataset = train_datagen.flow_from_directory(
    './data/train/',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

params = dvc.api.params_show()
epochs = params['train']['epochs']

with Live(dir='live/train', save_dvc_exp=False, dvcyaml=False) as live:
    model.fit(
        train_dataset,
        epochs=epochs,
        callbacks=[
            DVCLiveCallback(live=live)
        ]
    )

    model.save("bird-rec-model")
    live.log_artifact("bird-rec-model", type="model")
