/*
 * main.c
 *
 *  Created on: Oct 23, 2023
 *      Author: Daniel
 *      Example program for GPIO, Will continuously toggle GPIO24 (physical pin 18) at 500 ms rate
 */
#include<stdio.h>
#include <wiringPi.h>

int main(int argc, char **argv) {
	printf("Hello World");
	const int led = 5;
	wiringPiSetup();
	pinMode(led,OUTPUT);
	while(1){
		digitalWrite(led, HIGH);
		delay(500);
		digitalWrite(led, LOW);
		delay(500);
	}
	return 0;
}
