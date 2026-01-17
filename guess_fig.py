import numpy as np
from PIL import Image
from tensorflow import keras

# ------------------------------------------------------------------
# 1. Путь к модели и к картинке
# ------------------------------------------------------------------
MODEL_PATH = "models/shapes_real_cnn.keras"
IMAGE_PATH = "my_figure.png"
CLASS_NAMES = ['circle', 'decagon', 'heptagon', 'hexagon', 'kite', 'nonagon', 'octagon', 'oval', 'parallelogram',
               'pentagon', 'rectangle', 'rhombus', 'semicircle', 'square', 'star', 'trapezoid',
               'triangle']
IMG_SIZE = 28

# ------------------------------------------------------------------
# 2. Загрузка модели
# ------------------------------------------------------------------
model = keras.models.load_model(MODEL_PATH)


# ------------------------------------------------------------------
# 3. Подготовка изображения
# ------------------------------------------------------------------
def preprocess_image(path: str, img_size: int):
    img = Image.open(path).convert("L")  # grayscale
    img = img.resize((img_size, img_size))  # 28×28
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return arr.reshape(1, img_size, img_size, 1)  # batch=1


# ------------------------------------------------------------------
# 4. Предсказание
# ------------------------------------------------------------------
def get_prediction():
    X = preprocess_image(IMAGE_PATH, IMG_SIZE)
    probs = model.predict(X, verbose=0)[0]  # вероятности
    pred = int(probs.argmax())

    print("Предсказанный класс:", CLASS_NAMES[pred])
    print("Вероятности:")
    for name, p in zip(CLASS_NAMES, probs):
        print(f"{name:>8}: {p:.3f}")
    return CLASS_NAMES[pred]
