/*
*/

#include "Person.h"

int main(int nArgs, char** vArgs) {
	Person p;
	p.sayHello();
	p.age = 32;
	p.name = "Brian";
	p.sayHello();
	return 0;
}

