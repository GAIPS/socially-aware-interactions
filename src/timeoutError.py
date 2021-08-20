from PyQt5.QtCore import QTimer

class TimeoutErrorApp:
    ''' Class of timeout error - error detection and recovery'''
    def __init__(self, app):
        '''Initialize timeout error
        :param app: dialogue system's application to get readFile object to obtain variable from scenario file and call app function
        :var timeoutCondition: maximum time in seconds to wait for user input (obtained from scenario file)
        :var timeoutActive: bool that indicates if the timeout error was activated or not
        '''
        
        self.app = app
        self.inputFile = app.inputFile
        
        self.timeoutCondition = self.inputFile.timeoutCondition
        self.timeoutActive = False
    
    def identifyTimeoutError(self):
        '''Detect timeout error'''
        if self.timeoutCondition > 0 and not self.timeoutActive:              
            self.timer = QTimer()
            self.timer.timeout.connect(self.activateTimeoutFunction)
            self.timer.start(self.timeoutCondition*1000)
        
    def activateTimeoutFunction(self):
        '''Activate timeout error for the agent to acknowledge the timeout error'''
        if not self.timeoutActive:
            self.timeoutActive = True
            #for agent to enter timeout frame
            self.app.printAgentResponse(None)
        
    def timeoutRecoveryRepetition(self, inputNode):
        '''After entering timeout frame'''
        if inputNode is not None and self.timeoutActive:
            self.timeoutActive = False
            return True
        return False
        
    def timeoutRecoveryAcknowledge(self, inputNode):
        '''Before entering timeout frame'''
        if inputNode is None and self.timeoutActive:
            return True
        return False
