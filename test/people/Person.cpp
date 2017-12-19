/*
*/

#include "Person.h"
#include <iostream>

Person::Person() {
	age = 0;
	name = "[unnamed]";
}

void Person::sayHello() {
	std::cout << this->name << ", age " << this->age << ", says 'Hello!'" << std::endl;
}



