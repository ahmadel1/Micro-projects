#include <stdint.h>
#include "inits\initsHeaders.h"
void SystemInit(){}
	

int main(void){
	uint32_t current = 2;
  PortF_Init();
	SysTick_Init(); 
	while(1){
		delay(1);
		GPIO_PORTF_DATA_R = current;
		if(current == 14)current = 2;
		else current = current + 2;
	}

}
