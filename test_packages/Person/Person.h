/**
 * @author "Brian Kirkpatrick" <code@tythos.net>
 */

#ifndef EPIC_TEST_PERSON_H
#define EPIC_TEST_PERSON_H

#include <iostream>
#include <string>

class Person {
private:
protected:
public:
    std::string name;
    int age;
    Person();
    void saySomething(std::string msg);
};

#endif
