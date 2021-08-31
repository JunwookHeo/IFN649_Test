#define LEDPIN 11
#define REDPIN 1
#define GREENPIN 2
#define YELLOWPIN 3
#define BUZZERPIN 4
#define SOILPIN 12
#define PHOTOPIN 20

// Analog sensor class for soil moisture and photoresistor
class ASensor {
  private:
    char mName[10];
    int mPin = -1;
    char mBuf[20];
  public:
  ASensor(String name, int pin){
    name.toCharArray(mName, 10);
    mPin = pin;
  }
  String readString(){
    int val = analogRead(mPin);
    snprintf (mBuf, 20, "%s : %d", mName, val);
    return mBuf;
  }
};

// Class for digital outputs for LEDs and Buzzer
class DOut {
  protected:    
    int mPin = -1;    
  public:
  virtual boolean On(){return false;}
  virtual boolean Off(){return false;}
};
class DLed : public DOut{
  public:
  DLed(int pin){ mPin = pin; pinMode(pin, OUTPUT);}
  boolean On(){ digitalWrite(mPin, HIGH); return true; }
  boolean Off(){ digitalWrite(mPin, LOW); return true; }
};
class Buzzer : public DOut{ 
  public:
  Buzzer(int pin){ mPin = pin; pinMode(pin, OUTPUT);}
  boolean On(){ tone(mPin, 1000); return true; }
  boolean Off(){ noTone(mPin); return true; }
};

// Command class for interface to deal with commands
class Command { 
  protected:
  String mCmd;
  DOut *mDout;
  public: 
  virtual boolean execute(String cmd){return false;} 
};
// Command classes for each command
class RedLedONCmd : public Command {
  public:
  RedLedONCmd(DOut *dout){ mDout = dout; mCmd = "RedLed_ON";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->On(): false;}
};
class RedLedOFFCmd : public Command {
  public:
  RedLedOFFCmd(DOut *dout){ mDout = dout; mCmd = "RedLed_OFF";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->Off(): false;}
};
class GreenLedONCmd : public Command {
  public:
  GreenLedONCmd(DOut *dout){ mDout = dout; mCmd = "GreenLed_ON";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->On(): false;}
};
class GreenLedOFFCmd : public Command {
  public:
  GreenLedOFFCmd(DOut *dout){ mDout = dout; mCmd = "GreenLed_OFF";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->Off(): false;}
};
class YellowLedONCmd : public Command {
  public:
  YellowLedONCmd(DOut *dout){ mDout = dout; mCmd = "YellowLed_ON";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->On(): false;}
};
class YellowLedOFFCmd : public Command {
  public:
  YellowLedOFFCmd(DOut *dout){ mDout = dout; mCmd = "YellowLed_OFF";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->Off(): false;}
};
class BuzzerONCmd : public Command {
  public:
  BuzzerONCmd(DOut *dout){ mDout = dout; mCmd = "Buzzer_ON";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->On(): false;}
};
class BuzzerOFFCmd : public Command {
  public:
  BuzzerOFFCmd(DOut *dout){ mDout = dout; mCmd = "Buzzer_OFF";}
  boolean execute(String cmd) {return cmd == mCmd ? mDout->Off(): false;}
};

// Create objects for LEDs and Buzzer
DLed redLed = DLed(REDPIN);
DLed greenLed = DLed(GREENPIN);
DLed yellowLed = DLed(YELLOWPIN);
Buzzer buzzer = Buzzer(BUZZERPIN);
// Pointer list to manage commands
Command *cmdList[8];
// Create object for analog sensors
ASensor soil("Soil", SOILPIN);
ASensor photo("Photo", PHOTOPIN);

// Deal with commands from bluetooth.
void procRxCmd(){
  if(Serial1.available() > 0){
    String str = Serial1.readString().substring(1);  
    for(unsigned int i = 0; i < sizeof(cmdList)/sizeof(cmdList[0]); i++){
      if(cmdList[i]->execute(str) == true) break;
    }
  }
}

void setup() { 
  // Setup serial for monitor and Setup Serial1 for BlueTooth
  Serial.begin(9600);  
  Serial1.begin(9600); 

  // Initialize commands and LEDs, Buzzer for outputs
  cmdList[0] = new RedLedONCmd(&redLed);
  cmdList[1] = new RedLedOFFCmd(&redLed);
  cmdList[2] = new GreenLedONCmd(&greenLed);
  cmdList[3] = new GreenLedOFFCmd(&greenLed);
  cmdList[4] = new YellowLedONCmd(&yellowLed);
  cmdList[5] = new YellowLedOFFCmd(&yellowLed);
  cmdList[6] = new BuzzerONCmd(&buzzer);
  cmdList[7] = new BuzzerOFFCmd(&buzzer);
}

void loop() {
  // Check the current time for an interval to read sensors
  static boolean state = 0;
  static unsigned long preTime = 0;
  unsigned long curTime = millis();

  // Process commands from bluetooth first.
  procRxCmd();  

  // Measure values from sensors.
  if(curTime - preTime > 1000){
    String mois = soil.readString();
    Serial.println(mois);
    Serial1.println(mois);
    String light = photo.readString();
    Serial.println(light);
    Serial1.println(light);

    digitalWrite(LEDPIN, state);
    
    state = !state;    
    preTime = curTime;
  }
}
