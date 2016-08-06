#include <stdio.h>
int delayTime = 20;
int strelka=0;
// Пины шаговиков и лазера настроить 
const byte stepPin = 2;
const byte directionPin = 5;
const byte enablePin = 8;
const byte stepPin2 = 3;
const byte directionPin2 = 6;
const byte enablePin2 = 8;
const byte laser = 9;



class Command
{
public:
char type;
unsigned int parameter;
Command *next_command;
Command(char _type,unsigned int _parameter):type(_type),parameter(_parameter),next_command(NULL){}
};

 

void setup() {
// put your setup code here, to run once:
Serial.begin(9600);
pinMode(laser, OUTPUT);

pinMode(stepPin, OUTPUT);
pinMode(directionPin, OUTPUT);
pinMode(enablePin, OUTPUT);
pinMode(stepPin2, OUTPUT);
pinMode(directionPin2, OUTPUT);
pinMode(enablePin2, OUTPUT);

}
char mass[10];
int index = 0 ;
Command* first_command = NULL;
Command* last_command = NULL;
void process_input(){
char type;
unsigned int parameter;
type = mass[0]; 
*strstr(mass,"\n") = '\0';
parameter = atoi(strstr(mass,":")+1);

//ADD COMMAND TO LIST

if(first_command == NULL){
first_command = new Command(type,parameter);
last_command = first_command;
}else{
last_command -> next_command = new Command(type,parameter);
last_command = last_command -> next_command;
}


}

void stepper1(){
digitalWrite(enablePin, HIGH);
if(strelka>0)
digitalWrite(directionPin, HIGH);
else{
digitalWrite(directionPin, LOW);
strelka*=-1;
}
for (int i = 0; i < strelka; ++i){
digitalWrite(stepPin, HIGH);
delay(delayTime);
digitalWrite(stepPin, LOW);
delay(delayTime);
Serial.println("Move");

}
digitalWrite(enablePin, LOW);
}

void stepper2(){
digitalWrite(enablePin2, HIGH);
if(strelka>0)
digitalWrite(directionPin2, HIGH);
else{
digitalWrite(directionPin2, LOW);
strelka*=-1;
}
for (int i = 0; i < strelka; ++i){
digitalWrite(stepPin2, HIGH);
delay(delayTime);
digitalWrite(stepPin2, LOW);
delay(delayTime);
Serial.println("Move");

}
digitalWrite(enablePin, LOW);
}

void laser1(){
digitalWrite(laser, HIGH);
Serial.println("Light");
delay(strelka);
digitalWrite(laser,LOW);
}



void performe(Command *comm){
Serial.println("Performing");
Serial.println(comm->type);
Serial.println(comm->parameter);
if(comm->type == 'H'){
strelka=comm->parameter;
stepper1();
}
if(comm->type == 'V'){
strelka=comm->parameter;
stepper2();
}
if(comm->type == 'L'){
strelka=comm->parameter;
laser1();
}
//Добавить шаговиков
}
void loop() {
//read new command
if(Serial.available()) {
mass[index] = Serial.read();
if(mass[index] == '\n'){
process_input();
index = 0;
}else{
++index; 
}
}
//performe next command
if(first_command!=NULL){
performe(first_command);
Command* next_comm = first_command -> next_command;
delete first_command;
first_command = next_comm;
}

}

