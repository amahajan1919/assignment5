"""
Student information for this assignment:

Replace <FULL NAME> with your name.
On my/our honor, Aakanksha Mahajan and Surabhi Arun, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

=======
UT EID 1: am96292
UT EID 2: sa59594
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = max(0, salary)

    @property
    def name(self):
        """

        name getter
        """
        return self.__name

    @property
    def manager(self):
        """

        manager getter
        """
        return self.__manager

    @property
    def performance(self):
        """

        performance getter
        """
        return self._performance

    @performance.setter
    def performance(self, value):
        self._performance = max(PERCENTAGE_MIN, min(PERCENTAGE_MAX, value))

    @property
    def happiness(self):
        """

        happiness getter
        """
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        self._happiness = max(PERCENTAGE_MIN, min(PERCENTAGE_MAX, value))

    @property
    def salary(self):
        """

        salary getter
        """
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError(SALARY_ERROR_MESSAGE)
        self._salary = value

    @abstractmethod
    def work(self):
        """

        abstract method for work
        """

    def interact(self, other):
        """

        Simulates an interaction between this employee and another employee
        """
        if other.name not in self.relationships:
            self.relationships[other.name] = 0
        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            self.happiness += 1
        elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[other.name] += 1
        else:
            self.relationships[other.name] -= 1
            self.happiness -= 1

    def daily_expense(self):
        """

        Simulates the employee’s daily expenses by reducing their happiness and savings
        """
        self.happiness -= 1
        self.savings -= DAILY_EXPENSE

    def __str__(self):
        return f"""{self.name}
\tSalary: ${self.salary}
\tSavings: ${self.savings}
\tHappiness: {self.happiness}%
\tPerformance: {self.performance}%"""

class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """
    def work(self):
        adjust = random.randint(-5, 5)
        self.performance += adjust
        if adjust <= 0:
            self.happiness -= 1
            for person in self.relationships:
                self.relationships[person] -= 1
        else:
            self.happiness += 1

class TemporaryEmployee(Employee):
    "temporary employee in the worst company"
    def work(self):
        "simulates one hour of work"
        change = random.randint(-15, 15)
        self.performance += change
        self.happiness += 1 if change > 0 else -2

    def interact(self, other):
        "handles interaction between employees"
        super().interact(other)

        if self.manager and other.name == self.manager.name:
            if other.happiness > HAPPINESS_THRESHOLD and \
                self.performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary //= 2
                self.happiness = max(0, self.happiness - 5)
                if self.salary <= 0:
                    self.is_employed = False




class PermanentEmployee(Employee):
    "permanent employee in the worst company"
    def work(self):
        "one hour of work"
        change = random.randint(-10, 10)
        self.performance += change
        self.happiness += 1 if change >= 0 else 0

    def interact(self, other):
        'interaction btwn employees'
        super().interact(other)

        if self.manager and other == self.manager:
            if other.happiness > HAPPINESS_THRESHOLD and self.performance > 25:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness = max(0, self.happiness - 1)
