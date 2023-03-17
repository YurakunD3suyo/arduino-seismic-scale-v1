# arduino-seismic-scale-v1
P2P地震情報で公開されている「ラズパイ震度計」を、Arduinoとのシリアル通信で実現したものです。

## 作り方
作り方は「ラズパイ地震計」と同じで、Arduinoに置き換わっただけです。
fritzingの画像は後程張りますのでしばしお待ちを...

## Arduinoにコードを書き込もう！
1. https://www.arduino.cc/en/software 
   に行き、Arduino IDEの最新版をダウンロード

2. Arduino IDEでArduino-SendInt.inoを読み込む(同じ名前のフォルダ内で開く)

3. Arduinoの「ボード」と「シリアルポート」を選択し、Arduinoに書き込む

## Pythonコードを実行しよう！
1. https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=ja-jp&gl=jp&rtc=1
   に行きPython 3.10をダウンロード

2. コマンドプロンプトを開き、`python -m pip install pyserial` を実行する

3. Python-Calcu.pyを右クリックし、プログラムから実行する>Python 3.10 を選択
![image](https://user-images.githubusercontent.com/128114749/225811494-beef7860-9448-4250-b1e7-103018d74e75.png)

4.計算結果が出るはずです！

![image](https://user-images.githubusercontent.com/128114749/225812862-ec31e629-ee03-4b53-beee-9a8432de31e1.png)

