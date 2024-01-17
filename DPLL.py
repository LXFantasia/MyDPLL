from functools import reduce

class Truth:
    r'''
    真值, 分为True, False, Unknown三类
    
    Args:
        value: True, False or Unknown
    '''
    def __init__(self,  value) -> None:
        self.value = value
    
    def neg(self):
        r'''
        返回真值的非
        '''
        if self.value == "True":
            return Truth("False")
        elif self.value == "False":
            return Truth("True")
        else:
            return Truth("Unknown")
    
    def __str__(self):
        return self.value
    
    def __repr__(self) -> str:
        return self.value
    
    def disjunction(self, other):
        r'''
        真值的析取
        '''
        if self.value == "True" or other.value == "True":
            return true
        elif self.value == "False" and other.value == "False":
            return false
        else:
            return unknown
    
    def conjunction(self, other):
        r'''
        真值的合取
        '''
        if self.value == "False" or other.value == "False":
            return false
        elif self.value == "Unknown" or other.value == "Unknown":
            return unknown
        else:
            return true

true = Truth("True")
false = Truth("False")
unknown = Truth("Unknown")

class Literal:
    r'''
    命题逻辑变元

    Args:
        name: The name of literal
        vlaue: The truth value of literal
    '''
    def __init__(self, name, value = unknown) -> None:
        self.name = name
        self.value = [value]
        self.negvalue = [value.neg()]
    
    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def __neg__(self):
        r'''
        Return the negation of the literal
        '''
        lit_neg = Literal("-" + self.name)
        lit_neg.value = self.negvalue
        lit_neg.negvalue = self.value
        return lit_neg
    
    def set_value(self, val):
        r'''
        Reset the value of a literal

        Args:
            val: the truth value assigned
        
        Returns:
            None
        '''
        self.value[0] = val
        self.negvalue[0] = val.neg()

    def check_value(self):
        r'''
        Check the value of a literal
        '''
        return self.value[0]
    
    def is_assigned(self) -> bool:
        r'''
        Check whether the truth value is assigned

        Return a bool value
        '''
        if self.value[0] == unknown:
            return False
        return True

class Clause:
    r'''
    子句，以析取范式的形式表示

    Args:
        args: A sequence of literals
    '''
    def __init__(self, *args) -> None:
        self.value = list(args)

    def get_truth(self):
        r'''
        Get the truth value of clause
        '''
        truth = []
        for x in self.value:
            truth.append(x.value[0])
        return reduce(Truth.disjunction, truth)
    
    def __str__(self):
        name = []
        for x in self.value:
            name.append(x.name)
        return " \/ ".join(name)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def remove(self, lit):
        for x in self.value:
            if x.name == lit.name:
                self.value.remove(x)
                break

class CNF:
    r'''
    合取范式
    '''
    def __init__(self, *args) -> None:
        self.value = list(args)
    
    def get_truth(self):
        r'''
        Get the truth value of CNF
        '''
        truth = []
        for x in self.value:
            truth.append(x.get_truth())
        return reduce(Truth.conjunction, truth)
    
    def __str__(self):
        name = []
        for x in self.value:
            name.append(x.__str__())
        return "(" + ") /\ (".join(name) + ")"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def remove(self, lit):
        r'''
        Remove the clause containing certain literal
        '''
        for idx, x in enumerate(self.value):
            for y in x.value:
                if y.name == lit.name:
                    self.value[idx] = 0
                    break
        self.value = [i for i in self.value if i != 0]
    
    def get_member(self) -> list[Literal]:
        r'''
        Return the membership of CNF
        '''
        ans = []
        for clause in self.value:
            for literal in clause.value:
                if literal not in ans:
                    ans.append(literal)
        return ans
    
    def check_unit(self):
        r'''
        Check is there any unit clause
        '''
        for x in self.value:
            if len(x.value) == 1:
                return x.value[0]
        return None
    
    def DPLL(self) -> bool:
        r'''
        Run the DPLL to check SAT
        '''
        while (unit := self.check_unit()) != None:
            self.remove(unit)
            for x in self.value:
                x.remove(-unit)
        for x in self.value:
            if len(x.value) == 0:
                return False
        if len(self.value) == 0:
            return True
        lit = self.get_member()[0]
        cnf1 = CNF(*self.value, Clause(lit))
        cnf2 = CNF(*self.value, Clause(-lit))
        return cnf1.DPLL() or cnf2.DPLL()

if __name__ == "__main__":
    x1 = Literal("x1")
    x2 = Literal("x2")
    x3 = Literal("x3")
    x4 = Literal("x4")
    x5 = Literal("x5")
    x6 = Literal("x6")
    x7 = Literal("x7")
    c1 = Clause(-x2, -x3, -x4, x5)
    c2 = Clause(-x1, -x5, x6)
    c3 = Clause(-x5, x7)
    c4 = Clause(-x1, -x6, -x7)
    c5 = Clause(-x1, -x2, x5)
    c6 = Clause(-x1, -x3, x5)
    c7 = Clause(-x1, -x4, x5)
    c8 = Clause(-x1, x2, x3, x4, x5, -x6)
    cnf1 = CNF(c1, c2, c3, c4, c5, c6, c7, c8)
    print(cnf1)
    print(cnf1.DPLL())