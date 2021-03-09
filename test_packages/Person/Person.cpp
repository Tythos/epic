/**
 * @author "Brian Kirkpatrick" <code@tythos.net>
 */

#include "Person.h"

Person::Person() {
    name = "[unknown]";
    age = 0;
}

void Person::saySomething(std::string msg) {
    std::cout << name << ", age " << age << ", says '" << msg << "'" << std::endl;
}
