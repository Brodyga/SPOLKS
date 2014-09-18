#include <msp430.h>				

int main(void) {
	WDTCTL = WDTPW | WDTHOLD;
	P8DIR |= BIT1;
	P8OUT &= !BIT1;

	P1DIR |= BIT7;
	P1OUT |= BIT7;
	P1REN |= BIT7;
	P1DIR &= !BIT7;

	P2DIR |= BIT2;
	P2OUT |= BIT2;
	P2REN |= BIT2;
	P2DIR &= !BIT2;

	int enable = 0;

	for(;;) {
		volatile unsigned int i;

		if (!(P1IN & BIT7) || !(P2IN & BIT2))
		{
			enable ^= 1;
			P8OUT &= !BIT1;
		}

		if (enable == 1)
		{
			P8OUT ^= BIT1;
		}

		i = 10000;
		do i--;
		while(i != 0);
	}
	
	return 0;
}
