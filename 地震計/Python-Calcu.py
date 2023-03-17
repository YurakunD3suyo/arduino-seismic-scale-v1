# [初めに]
# このコードは、たくや様(https://twitter.com/p2pquake_takuya)の「ラズパイ震度計」で利用されているコードを、
# Arduinoとのシリアル通信で取得した値を使用して計算するように改変したものです。

# ソース元 [https://github.com/p2pquake/rpi-seismometer]
# ソース元ライセンス [MIT License(githubに入っています)]

# ゆらくん https://github.com/YurakunD3suyo

import time
import datetime
import math
import serial

# FPS制御 -----
# ターゲットFPS
target_fps = 200
start_time = time.time()
frame = 0

# シリアル通信制御 -----
ser = serial.Serial('COM3', 500000)

def ReadChannel(channel):
    # Arduinoにチャンネル番号を送信
    ser.write(bytes([channel]))
    # Arduinoからデータを読み取り、10進数に変換
    data = int(ser.readline().strip().decode('utf-8'))
    return data

# 加速度データ制御 -----
# A/Dコンバータ値 -> ガル値 係数
ad2gal = 1.13426
# 0.3秒空間数
a_frame  = int(target_fps * 0.3)

# 地震データ -----
adc_values = [[1] * target_fps, [1] * target_fps, [1] * target_fps]
rc_values   = [0, 0, 0]
a_values = [0] * target_fps * 5

adc_ring_index = 0
a_ring_index = 0

# リアルタイム震度計算 -----
while True:
    # リングバッファ位置計算
    adc_ring_index = (adc_ring_index + 1) % target_fps
    a_ring_index = (a_ring_index + 1) % (target_fps * 5)

    # 3軸サンプリング
    for i in range(3):
        val = ReadChannel(i)
        adc_values[i][adc_ring_index] = val
   
    # フィルタ適用及び加速度変換
    axis_gals = [0, 0, 0]
    for i in range(3):
        offset = sum(adc_values[i])/len(adc_values[i])
        rc_values[i] = rc_values[i]*0.94+adc_values[i][adc_ring_index]*0.06
        axis_gals[i] = (rc_values[i] - offset) * ad2gal

    # 3軸合成加速度算出
    composite_gal = math.sqrt(axis_gals[0]**2 + axis_gals[1]**2 + axis_gals[2]**2)

    # 加速度リングバッファに格納
    a_values[a_ring_index] = composite_gal

    # 0.3秒以上継続した合成加速度から震度を算出
    seismic_scale = 0
    min_a = sorted(a_values)[-a_frame]
    if min_a > 0:
      seismic_scale = 2 * math.log10(min_a) + 0.94

    #出力(小数点の桁数固定、ゼロ埋め)
    if frame % (target_fps / 20) == 0:
        print(datetime.datetime.now(), '{:.02f}'.format(composite_gal), "gal" , " scale:" , '{:.02f}'.format(seismic_scale), " frame:", frame)

    # 次フレームの開始時間を計算
    frame += 1
    next_frame_time = frame / target_fps

    # 残時間を計算し、スリープ
    current_time = time.time()
    remain_time = next_frame_time - (current_time - start_time)

    if remain_time > 0:
        time.sleep(remain_time)

    # フレーム数は32bit long値の上限あたりでリセットしておく
    if frame >= 2147483647:
        start_time = current_time
        frame = 1
