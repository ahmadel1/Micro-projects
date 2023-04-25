#include <stdint.h>
#include "initsHeaders.h"
#include "tm4c123gh6pm.h"

void PortF_Init(void){
	volatile uint32_t delay;
  SYSCTL_RCGCGPIO_R |= 0x00000020;  // 1) activate clock for Port F
  delay = SYSCTL_RCGCGPIO_R;        // allow time for clock to start
  GPIO_PORTF_LOCK_R = 0x4C4F434B;   // 2) unlock GPIO Port F
  GPIO_PORTF_CR_R = 0x1F;           // allow changes to PF4-0
  // only PF0 needs to be unlocked, other bits can't be locked
  GPIO_PORTF_AMSEL_R = 0x00;        // 3) disable analog on PF
  GPIO_PORTF_PCTL_R = 0x00000000;   // 4) PCTL GPIO on PF4-0
  GPIO_PORTF_DIR_R = 0x0E;          // 5) PF4,PF0 in, PF3-1 out
  GPIO_PORTF_AFSEL_R = 0x00;        // 6) disable alt funct on PF7-0
  GPIO_PORTF_PUR_R = 0x11;          // enable pull-up on PF0 and PF4
  GPIO_PORTF_DEN_R = 0x1F;          // 7) enable digital I/O on PF4-0
}

void SysTick_Init(void){
	NVIC_ST_CTRL_R = 0;  //disable systick during setup
	NVIC_ST_RELOAD_R = 0XFFFFFF;  //maximum reload value
	NVIC_ST_CURRENT_R = 0;   //any write to current clears it 
	NVIC_ST_CTRL_R = 0X05;  //enable systick with core clock
}

void systick_wait_1ms(){
	NVIC_ST_RELOAD_R = 16000-1;
	NVIC_ST_CURRENT_R = 0;
	while((NVIC_ST_CTRL_R & 0x00010000)==0){};
}

void delay(uint32_t timeInSeconds){
	uint32_t counter = timeInSeconds*1000, i=0;
	for(i = 0; counter>i; i++){
			systick_wait_1ms();
	}
}