int address  = 0;    // I2C address
int data = 0;   // I2C data
int inByte = 0;         // incoming serial byte
int flag = 0;
String inString = "";    // string to hold input
String cmdarg1 = "";
String cmdarg2 = "";
String arg1 = "";
String arg2 = "";
int arglen1 =0;
int arglen2 =0;
char argbyte1[10];
char argbyte2[10];
int inChar;
char *endptr;
#include <Wire.h>
byte x = 0;

void setup()
{
  pinMode(11, OUTPUT);
  pinMode(13, OUTPUT);
  //   /* Setup the 8mhz PWM clock
  // * This will be on pin 11*/
  // Fast PWM, No Prescaling, Compare Match...Freq=F_CPU/(N*(1+TOP))/2 <-toggle
  ASSR &= ~(_BV(EXCLK) | _BV(AS2));// No Async, No External Clock
  TCCR2A = (1 << COM2A0) | (1 << WGM21) | (1 << WGM20);// FastPWM, Compare Match(toggle)
  TCCR2B = (1 << WGM22) | (1 << CS20);// TOP=OCR2A, No Prescaling(N=1)
  OCR2A = 0;// TOP=0CR2A=0
  delay(3000);

  // start serial port at 9600 bps:
  Serial.begin(9600);
  // join i2c bus (address optional for master)
  Wire.begin();
  pinMode(SDA, INPUT); //disable internal pull-up
  pinMode(SCL, INPUT); //disable internal pull-up

  PrintMenu();
}

void loop()
{

  //Command input
  inChar == 0 ;
  Serial.print(">");
  while (inChar != '\n' ) {
    if (Serial.available() > 0) {
      inChar = Serial.read();
      Serial.print((char)inChar);
      inString += (char)inChar;
    }
  }

  Serial.println("");
  inString.trim();
  if(inString[0] == 'w' | inString[0] == 'W')
  {
    inString[0] = ' ';
    cmdarg1 = inString;
    cmdarg1.trim();
    arglen1 = cmdarg1.indexOf(' ');
    arg1 = cmdarg1.substring(0,arglen1);
    for (int i=0; i < arglen1; i++){
      cmdarg1[i] = ' ';
    }
    cmdarg2 = cmdarg1;
    cmdarg2.trim();
    arglen2 = cmdarg2.indexOf(' ');
    if (arglen2 == -1 )
    {
      arglen2 = cmdarg2.length();
      arg2 = cmdarg2;
    }
    else
    {
      arg2 = cmdarg2.substring(0,arglen2);
    }
    arg1.toCharArray(argbyte1,arglen1+1);
    arg2.toCharArray(argbyte2,arglen2+1);

    // address =  hexsz2int(argbyte1);
    // data    =  hexsz2int(argbyte2);
    address = strtol(argbyte1, NULL, 16);
    data = strtol(argbyte2, NULL, 16);

    Serial.print("Ad=");
    Serial.println(address,HEX);
    Serial.print("Dt=");
    Serial.println(data,HEX);

    Wire.beginTransmission(0x21); // write 0x42 read 0x43
    Wire.write(address);        // sends address
    Wire.write(data);              // sends data
    flag = Wire.endTransmission();    // stop transmitting
    Serial.print("flag=");
    Serial.println(flag,DEC);

    delay(10);

  }
  else if (inString[0] == 'r' | inString[0] == 'R')
  {
    inString[0] = ' ';
    cmdarg1 = inString;
    cmdarg1.trim();
    arglen1 = cmdarg1.indexOf(' ');
    if (arglen1 == -1 ) {
      arglen1 = 2;
    }
    arg1 = cmdarg1.substring(0,arglen1);

    Serial.print("arglen1 =");
    Serial.println(arglen1 ,HEX);

    arg1.toCharArray(argbyte1,arglen1+1);
    address =  hexsz2int(argbyte1);

    Serial.println(arg1);

    Serial.print("Address=");
    Serial.println(address,HEX);
    Serial.println("---");

    Wire.beginTransmission(0x21); // write 0x42 read 0x43
    Wire.write(address);        // sends address
    flag = Wire.endTransmission();    // stop transmitting
    Serial.print("flag=");
    Serial.println(flag,DEC);

    Wire.requestFrom(0x21, 1);
    data = Wire.read();

    Serial.print("Data(HEX)=");
    Serial.println(data,HEX);
    Serial.print("Data(DEC)=");
    Serial.println(data,DEC);

    delay(50);

  }
  else if (inString[0] == 'h' | inString[0] == 'H')
  {
    Serial.println("WRITE :w [address] [data]");
    Serial.println("READ  :r [address] [number of data] ");
    Serial.println("HELP  :h ");
  }
  else
  {
    Serial.println("Syntax Error");
  }

  inString = "";
  inChar = 0;
  cmdarg1 = "" ;
  cmdarg2 = "" ;
  arg1 = "" ;
  arg2 = "" ;
  arglen1 =0;
  arglen2 =0;
  data = 0;
  Serial.println("");
}


void PrintMenu(void)
{
  Serial.println("------------------------------");
  Serial.println(" OV7640 Camera Debugger");
  Serial.println(" Copyright 2011 Hirokazu Enya");
  Serial.println("------------------------------");
  Serial.println( " ");
}

//"hexsz2int" is part of fuction "maybekanji"
//original source from below URL
//<http://www.koders.com/cpp/fid2BB5F1A942B42648647CBD66ED9A2A03B1C00B5F.aspx>

/*
 * The following function "maybekanji" is derived from
 * RJIS-1.0 by Mr. Hironobu Takahashi.
 * Maybekanji() is included here under the courtesy of the author.
 * The original comment of rjis.c is also included here.
 */

/*
 * RJIS ( Recover JIS code from broken file )
 * Copyright (C) 1992 1994
 * Hironobu Takahashi (takahasi@tiny.or.jp)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either versions 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SKK, see the file COPYING.  If not, write to the Free
 * Software Foundation Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

int hexsz2int(char *str)
{
  int val;
  int sign;

  while (*str == ' ' || *str == '\t') str++;
  sign = 1;
  if (*str == '+') str++;
  else if (*str == '-') {
    sign = -1;
    str++;
  }
  val = 0;
  while (*str >= '0' && *str <= '9' ||
    *str >= 'A' && *str <= 'F' ||
    *str >= 'a' && *str <= 'f') {
    val <<= 4;
    if      (*str >= '0' && *str <= '9') val += *str - '0';
    else if (*str >= 'A' && *str <= 'F') val += *str - 'A' + 10;
    else                                 val += *str - 'a' + 10;
    str++;
  }

  return sign == 1 ? val : -val;
}
