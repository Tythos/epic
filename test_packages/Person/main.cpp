/**
 * @author "Brian Kirkpatrick" <code@tythos.net>
 */

#include "Person.h"

int main(int nArgs, char** vArgs) {
    Person *p = new Person();
    p->name = "Kirk";
    p->age = 35;
    p->saySomething("WHAZZUUP");
    return 0;
}
