import socket
import os
import sys


class Step:

    def __init__(self, 
                execute_instructions, 
                passed_instructios, 
                error1_instructions, 
                error2_instructions, 
                allOtherError_instructions):
        self.execute_instructions = execute_instructions
        self.passed_instructions = passed_instructios
        self.error1_instructions = error1_instructions
        self.error2_instructions = error2_instructions
        self.allOtherErrors_instructions = allOtherError_instructions

    def execute(self):
        self.execute_instructions()

    def validate(self, state):
        match state():
            case 100:
                self.passed()
                return True
            case 200:
                self.error1()
                return False
            case 300:
                self.error2()
                return False
            case _:
                self.allOtherErrors()
                return False

    def passed(self):
        self.passed_instructions()

    def error1(self):
        self.error1_instructions()

    def error2(self):
        self.error2_instructions()

    def allOtherErrors(self):
        self.allOtherErrors_instructions()


class Procedure:

    def __init__(self):
        self.steps = []
        self.currentStep = 0
        self.isEnabled = False

    def buildStep(self, execute, passed, error1, error2, allOtherErrors):
        self.steps.append(Step(execute, passed, error1, error2, allOtherErrors))

    def run(self):
        if not self.isEnabled:
            print("tried to run an unActived procedure")
            return 0

        if self.currentStep < len(self.steps):
            print("Running step: ", self.currentStep)
            self.steps[self.currentStep].execute()
            return 1
        else:
            print("ran out of steps")
            return 2
    
    def validate(self, state):
        if self.currentStep >= len(self.steps):
            print("error: attempted to validate a step out side of step range")
            return
        
        if self.steps[self.currentStep].validate(state):
            print("Moving to next step")
            self.currentStep += 1
            self.run()
        else:
            print("error detected")


class ProcedureManager:

    def __init__(self):
        self.procedures = {}
        pass
        
    def addProcedure(self, name, procedure):
        if name in self.procedures:
            print ("error: key name already exists, use a different name")
        else:
            self.procedures[name] = procedure

            numOfSteps = len(self.procedures[name].steps)

            print("Added procedure: " + name + " with ", numOfSteps)

    def anyProcedureIsRunning(self):
        for name in self.procedures:
            if self.procedures[name].isEnabled:
                return True
        
        return False

    def stopAllProcedures(self):
        for name in self.procedures:
            self.procedures[name].isEnabled = False

    def startProcedure(self, name):
        if name not in self.procedures:
            print ("error: tried to run a procedure that does not exist")
            return

        if self.anyProcedureIsRunning():
            print ("error: another procedure is already running")
            return


        print ("Starting Procedure: " + name)
        self.procedures[name].isEnabled = True
        self.procedures[name].run()

    def validate(self, procedureName, state):
        self.procedures[procedureName].validate(state)

    def validateActiveProcedure(self, state):
        for name in self.procedures:
            if self.procedures[name].isEnabled:
                self.procedures[name].validate(state)
                return True
            
        return False
