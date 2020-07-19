const int analogPinUD = A0;
const int analogPinLR = A1;
int UD = 0;
int LR = 0;

void setup() {
  Serial.begin(9600);
  }

void loop() {
  UD = analogRead(analogPinUD);
  LR = analogRead(analogPinLR);

  moveCursor(UD, LR);

  delay(50);
}

void moveCursor(int ud, int lr) {
    int xMove = mapRange(ud);
    int yMove = mapRange(lr);

    //Serial.print(xMove); Serial.print("\t"); Serial.println(yMove);

    Serial.write((byte) 0xFD);
    Serial.write((byte) 0x05);
    Serial.write((byte) 0x02);

    Serial.write((byte) 0x00);
    Serial.write((byte) xMove);
    Serial.write((byte) yMove);
    Serial.write((byte) 0x00);

    delay(50);
}

int mapRange(int num) {
  num = num - 511;  // -512 ~ 512 にマッピング
  num /= 4;  // -128 ~ 128にマッピング
  num += 127; // 0 ~ 255にマッピング

  if (120 <= num && num <= 134) {
    num = 127;
  }

  if (num <= 127) {
      num = 127 - num;
    }
  else if (127 < num) {
      num -= 128; // 0 ~ 127へマッピング
      num = 255 - num;
    }
  return num;
}
