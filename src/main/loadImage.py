from util import util
from glob import glob
import keras
from keras.utils import np_utils
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.preprocessing.image import array_to_img, img_to_array, load_img
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from PIL import Image

#プロパティ読み出し
util = util.Util()

#X:本命及び義理チョコの画像(メタデータ)情報
#Y:本命及び義理チョコの属性情報
X = []
Y = []

##事前処理##
#義理チョコと本命チョコ間で重複している画像は、どちらかを削除

#本命チョコイメージのリスト
hmImg = glob(util.getWorkDir() + "\honmei\*.png")
#義理チョコイメージのリスト
grImg = glob(util.getWorkDir() + "\giri\*.png")

#pandasでデータフレーム化
hmImgFrame = pd.DataFrame({
  "filename":[os.path.basename(f) for f in hmImg],
  "fullpath":[f for f in hmImg]
})

grImgFrame = pd.DataFrame({
  "filename":[os.path.basename(f) for f in grImg],
  "fullpath":[f for f in grImg]
})

#本命 + 義理チョコ一覧
ifiles = pd.concat([hmImgFrame,grImgFrame], axis=0).reset_index(drop=True)

# 画像のサイズとチャンネル数を取得してDataFrameに追加
ret = []
for fname in ifiles["fullpath"]:
    rimf = Image.open(fname)
    ret.append(np.asarray(rimf).shape)

ifiles["shape"] = ret

# ファイル名と画像サイズ、チャンネル数を元に、重複していないファイルを抽出
dupfiles = ifiles[ifiles.duplicated(subset=['filename', 'shape'], keep=False)]

# 義理と本命で重複していると思われる画像を削除
_ = [ os.remove(fpath) for fpath in dupfiles["fullpath"] ]
print(f"delete {len(dupfiles)} duplicated files")

##事前処理 end##
#本命チョコ
for targetImage in hmImg:
    #画像の呼び出し
    temp_img = load_img(targetImage, target_size=(64,64))

    #画像データの行列化
    temp_img_array  = img_to_array(temp_img)
    
    #画像の保管
    X.append(temp_img_array)
    #属性情報の保管
    Y.append(0)


#義理チョコ
for targetImage in grImg:
    #画像の呼び出し
    print(targetImage)
    temp_img = load_img(targetImage, target_size=(64,64))

    #画像データの行列化
    temp_img_array  = img_to_array(temp_img)
    
    #画像の保管
    X.append(temp_img_array)
    #属性情報の保管
    Y.append(1)

#numpyの機能で、arrayに変換
X = np.asarray(X)
Y = np.asarray(Y)

# 画素値を0から1の範囲に変換
X = X.astype('float32')
X = X / 255.0

# クラスの形式を変換
Y = np_utils.to_categorical(Y, 2)

# 学習用データとテストデータ
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=111)

##ここからデータモデルの作成（サンプルを使用）##
model = Sequential()

model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=X_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(2))       # クラスは2個
model.add(Activation('softmax'))

# コンパイル
model.compile(loss='categorical_crossentropy',
              optimizer='SGD',
              metrics=['accuracy'])

# 実行。出力はなしで設定(verbose=0)。
history = model.fit(X_train, y_train, batch_size=5, epochs=200,
                   validation_data = (X_test, y_test), verbose = 0)

#historyより確認
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(['acc', 'val_acc'], loc='lower right')
plt.show()

##データモデルの作成（サンプルを使用）END##