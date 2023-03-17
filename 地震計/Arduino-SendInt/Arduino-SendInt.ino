//[このコードについて]
//たくや様(https://twitter.com/p2pquake_takuya)の「ラズパイ震度計」をもとに
//改変したプログラムへデータを送るためのコードです。

//ゆらくん https://github.com/YurakunD3suyo

#include <SPI.h>

// MCP3204からの入力チャンネル番号
int channel = 0;

// MCP3204のピン設定
const int CS_PIN = 10;

void setup() {
  // MCP3204用のSPI通信初期化
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  SPI.begin();
  SPI.beginTransaction(SPISettings(16000000, MSBFIRST, SPI_MODE0));
  Serial.begin(500000);
}

int readChannel(int channel) {
  // MCP3204にチャンネル指定を送信
  byte cmd = B00000110 | (channel >> 1);
  byte data[3];
  digitalWrite(CS_PIN, LOW);
  SPI.transfer(cmd);
  data[0] = SPI.transfer(0);
  data[1] = SPI.transfer(0);
  data[2] = SPI.transfer(0);
  digitalWrite(CS_PIN, HIGH);
  
  // MCP3204の出力値を10進数に変換して返す
  int value = ((data[0] & 0x0F) << 8) | data[1];
  return value;
}

void loop() {
  // チャンネルの値を読み取り、シリアル通信で送信
  int value = readChannel(channel);
  Serial.println(value);
  delay(2);
}
