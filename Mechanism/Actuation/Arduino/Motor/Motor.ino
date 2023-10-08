#include <AFMotor.h>

AF_DCMotor motor(1);

void setup(){
  mstop();
  Serial.begin(9600);
}

void loop(){
  if(Serial.available()){
      char cmd = Serial.read();
      switch(cmd){
        case 'f':
          Serial.print("Forward\n");
          forward();
          break;

        case 'b':
          Serial.print("Backward\n");
          backward();
          break;

        case 'a':
          accelerate();
          break;

        case 'd':
          deaccelerate();
          break;

        case 's':
          Serial.print("Stop\n");
          mstop();
          break;

        default:
          break;
      }
    }
}

void forward(){
  motor.setSpeed(200);
  motor.run(FORWARD);
  }

void backward(){
  motor.setSpeed(200);
  motor.run(BACKWARD);
  }

void accelerate(){
  motor.run(FORWARD); 

    uint8_t i;

    for (i=0; i<255; i++){
    motor.setSpeed(i);  
    delay(10);
    }
}

void deaccelerate(){
  motor.run(FORWARD); 

  uint8_t i;
  for(i=255; i!= 0; i--){
    motor.setSpeed(i);  
    delay(10);
    }
}

void mstop(){
   motor.run(RELEASE);
  } 