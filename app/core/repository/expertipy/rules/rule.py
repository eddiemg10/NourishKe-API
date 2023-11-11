from enum import Enum

def validateNumber(var):
    if not isinstance(var, (int, float)):
        raise TypeError("Variable must be a number (int or float)")
    
class Operation(Enum):
    equals = "equals"
    lesser = "lesser"
    greater = "greater"
    between = "between"

class Antecedent():
    """
    A class used to represent the entecedent of a rule
    """
    # Eg if bloog sugar is less than 70
    # Eg if age is between 10 and 90
    # Eg if PAL is active

    def __init__(
            self, 
            value: int | float | str, 
            operation: Operation, 
            reference: int | float | str | list | tuple,
            ):
        """
        Parameters
        ----------
        value: any
            Value (from fact) to be compared to
        operation: Enum(greater, leser, equal) 
            How to compare the values
        reference: any
            Could be 1 value (float | str | int) or 2 (iterable) in the case of ranges 
        """

        self.fact_value = value # The value of specific fact
        self.operation = operation # Operation to perform (equals, greater, between)
        self.reference_value = reference # The value to compare it to

    def evaluate(self):
        """
        Evaluates the antecedent to determine its truth value.
        """
        if self.operation == Operation.between:
            # If checking for an in between value, cofirm the reference is an iterable object
            try:
                iter(self.reference_value)
                arg_length = len(self.reference_value)
                if arg_length != 2:
                    raise ValueError(f"Expected an iterable with 2 items, got {arg_length}")
                else:
                    if self.fact_value >= min(self.reference_value) and self.fact_value <= max(self.reference_value):
                        return True
                    else:
                        return False
            except (TypeError, ValueError) as err:
                print(err)
                return err
            
        elif self.operation == Operation.greater:
            validateNumber(self.fact_value)
            validateNumber(self.reference_value)
            return self.fact_value > self.reference_value
             
        elif self.operation == Operation.lesser:
            validateNumber(self.fact_value)
            validateNumber(self.reference_value)
            return self.fact_value < self.reference_value
        
        elif self.operation == Operation.equals:
            validateNumber(self.fact_value)
            validateNumber(self.reference_value)
            return self.fact_value == self.reference_value

class Consequent():
    
    def __init__(self, action):
        self.action = action

    def execute(self):
        print(self.action)
    
class ProductionRule():
    def __init__(self, antecedents: list[Antecedent], consequents: list[Consequent]):
        """
        Parameters
        ----------
        `antecedents`: list
            A list of antecedent objects
        `consequents`: list
            A list of consequents to be executed if all antecedents evaluate to True
        """
     
        self.antecedents = antecedents
        self.consequents = consequents

    def evaluate(self):
        for condition in self.antecedents:
            if not condition.evaluate():
                return False
        return True

    def execute(self):
        if self.evaluate():
            for action in self.consequents:
                action.execute()
