import socket
import os
import sys
# import cli
# import pythonserv


class Step:

    def __init__(self, 
                execute_instructions,
                validate_instructions, 
                passed_instructions, 
                error1_instructions, 
                error2_instructions, 
                allOtherError_instructions):
        self.execute_instructions = execute_instructions
        self.validate_instructions = validate_instructions
        self.passed_instructions = passed_instructions
        self.error1_instructions = error1_instructions
        self.error2_instructions = error2_instructions
        self.allOtherError_instructions = allOtherError_instructions

    def execute(self):
        print("Running Execute on a step")
        self.execute_instructions()

    def validate(self):
        print("Running validate on a step")
        match self.validate_instructions():
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
        print("running passed on a step")
        self.passed_instructions()

    def error1(self):
        print("running error 1 on a step")
        self.error1_instructions()

    def error2(self):
        print("running error 2 on a step")
        self.error2_instructions()

    def allOtherErrors(self):
        print("running all other error on a step")
        self.allOtherError_instructions()


class Procedure:

    def __init__(self):
        self.steps = []
        self.currentStep = 0
        self.isEnabled = False

    def buildStep(self, validate, execute, passed, error1, error2, allOtherErrors):
        self.steps.append(Step(execute, validate, passed, error1, error2, allOtherErrors))

    def run(self):
        print("running run on a procedure")
        if not self.isEnabled:
            print("tried to run an unActived procedure")
            return 0

        if self.currentStep < len(self.steps):
            print("Running step: ", self.currentStep)
            self.steps[self.currentStep].execute()
            return 1
        else:
            print("ran out of steps")
            # self.isEnabled = False
            return 2
    
    def validate(self):
        print("running validate on a procedure")
        if self.currentStep > len(self.steps):
            print("error: attempted to validate a step out side of step range")
            return
        
        if self.steps[self.currentStep].validate():
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

    def validate(self, procedureName):
        self.procedures[procedureName].validate()

    def validateActiveProcedure(self):
        print("Validating the active procedure")
        for name in self.procedures:
            if self.procedures[name].isEnabled:
                self.procedures[name].validate()
                return True
            
        return False
