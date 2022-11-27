#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <TFT_eSPI.h>
#include <SPI.h>

#define R(t,x,y) \ 
  f = x; \
  x -= t*y; \
  y += t*f; \
  f = (3-x*x-y*y)/2; \
  x *= f; \
  y *= f;

TFT_eSPI tft = TFT_eSPI();

const int width = 10;
const int height = 10;

const int R1 = 1;
const int R2 = 2;
const float K2 = 5;
const float K1 = (width * K2 * 3)/(8 * (R1 + R2));

float cosA = 1.0, cosB = 1.0;
float sinA = 0.0, sinB = 0.0;

float f;


char output[width][height] = {' '};
int zbuffer[width][height] = {0};

void setup() {
  // put your setup code here, to run once:
  tft.init();
  tft.setCursor(0,0,1);
  tft.setRotation(2);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE,TFT_BLACK);  tft.setTextSize(1);
  Serial.begin(115200);

}

void loop() {
  tft.setCursor(0,0,1);
  // put your main code here, to run repeatedly:
  float sintheta =0, costheta = 1;
  for (int j=0; j<90; j++){
    ESP.wdtFeed();
    float sinphi =0, cosphi = 1;
    for (int i =0;i <324; i++){
      float circlex = R1 * costheta +R2;
      float circley = R1 * sintheta;

      float x = circlex *(cosB*cosphi + sinA * sinB * sinphi) - circley*cosA*sinB;
      float y = circley *(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB;
      float ooz = 1/(K2 + cosA*circlex*sinphi + circley*sinA);

      int xp = (int)(width/2 + K1 * ooz * x);
      int yp = (int)(height/2 - K1 * ooz * y);

      float L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi);
      if (L>0){
        if (ooz > zbuffer[xp][yp]){
          zbuffer[xp][yp] = ooz;
          output[xp][yp] = ".,-~:;=!*#$@"[(int)(L*8)];
          }
        }
        R(0.02,cosphi,sinphi)
      }
      R(0.07,costheta,sintheta)
    }
    tft.fillScreen(TFT_BLACK);
      for (int line = 0; line < width; line++){
        for (int col=0; col < height; col++){
          tft.print(output[col][line]);
          tft.print(" ");
          putchar(output[col][line]);
          putchar(0x20);
          }
        putchar('\n');
        tft.println();
        tft.println();
        }
    R(0.08,cosA,sinA);
    R(0.03,cosB,sinB);
    delay(1);
    //printf("\x1b[23A");
}
