import readFile
import deliberationMechanism
import timeoutError
import sys
import math
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QGridLayout, QApplication, QScrollArea, QVBoxLayout, QLabel,  QLineEdit
from PyQt5.QtCore import Qt


class App():
    def __init__(self):
        '''Initialize dialogue system application'''
        #Run the application
        self.runApp()
    
    def sendUserInput(self, userInputNode):
        '''Print user input and send it to agent to obtain response
        :param userInputNode: tree node of user input 
        '''         
        self.printUserInput(userInputNode.sentence)      
        self.printAgentResponse(userInputNode)
        #Check for timeout error
        self.timeout.identifyTimeoutError()
             
    def printUserInput(self, sentence):
        '''Print user input
        :param sentence: sentence associated with user input node
        '''
        label = QLabel(sentence + " <<<")
        label.setAlignment(Qt.AlignRight)
        self.scrollLayout.addWidget(label)
        label.setStyleSheet("border: none")
    
    def printAgentResponse(self, userNode):
        '''Print agent response
        :param userNode: tree node of user input
        '''
        #Call agent's deliberation mechanism
        response = self.deliberation.respondAgentOutput(userNode)
        label = QLabel(">>> " + response)
        label.setStyleSheet("border: none")
        self.scrollLayout.addWidget(label)
        
        #Update user options according to user response
        self.updateUserOptions()
        
                      
    def updateUserOptions(self):
        '''Update user options according to the current context of the conversation'''
        #Clear grid of user options
        for i in reversed(range(self.grid.count())): 
            self.grid.itemAt(i).widget().setParent(None)
        #Call deliberation mechanism to obtain appropriate user options
        inputs = self.deliberation.listUserOptions()
        
        #Position and show user options buttons
        positions = [(i, j) for i in range(math.ceil(len(inputs)/4)) for j in range(4)]   
        for position, userIn in zip(positions, inputs):
            #Create button with sentence
            button = QPushButton(userIn.sentence)
            #style
            button.setStyleSheet("background-color:#ffffff; border-radius:15px; border:1px solid #dcdcdc;color:#666666; height: 30px; font-size: 13px; padding: 4px")
            #position
            self.grid.addWidget(button, *position)
            #function - When clicked the user input is printed and sent to the agent
            button.clicked.connect(lambda checked, i = userIn: self.sendUserInput(i))
        
    def openScenarioFile(self):
        '''Select scenario JSON file which will be read by the system'''
        fileName = QFileDialog.getOpenFileName(self.widget, 'Scenario JSON File', "", "JSON (*.json)")
        self.textScenarioFile.setText(fileName[0])
    
    def startSystem(self):
        '''Start or restart system after selecting scenario file'''
        file = self.textScenarioFile.text()
        if len(file) > 0:
            #Clear conversation history
            self.clearLayout(self.scrollLayout)
            #Read the input file       
            self.inputFile = readFile.ReadFile(file)
            #Initialize the timeout error event
            self.timeout = timeoutError.TimeoutErrorApp(self)
            #Initialize the deliberation mechanism
            self.deliberation = deliberationMechanism.DeliberationMechanism(self)

            
            self.updateUserOptions()           
    
    def clearLayout(self, layout):
        '''Clear layout widget'''
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addStretch(1)

                
    def runApp(self):
        '''
            Construct dialogue interface
        '''
        #Main widget for all interface elements    
        app = QApplication([])
        self.widget = QWidget()
        vBox = QVBoxLayout()
        self.widget.setLayout(vBox)
        self.widget.setWindowTitle('Chat')
        
        #1. Widget for file input and start buttons
        buttons = QGridLayout()
        widgetButtons = QWidget()
        widgetButtons.setLayout(buttons)
        
        #1.1: File input
        self.labelScenario = QLabel("Scenario:")
        self.textScenarioFile = QLineEdit()
        self.uploadScenario = QPushButton('...')
        #styles and configurations
        self.labelScenario.setStyleSheet("height: 30px; font-size: 13px; color:#666666;")
        self.textScenarioFile.setStyleSheet("background-color:#ffffff; border-radius:0px; border:1px solid #dcdcdc;color:#666666; height: 30px; font-size: 13px;")
        self.uploadScenario.setStyleSheet("background-color:#dddddd; border-radius:15px; border:1px solid #dcdcdc;color:#666666; height: 30px; font-size: 13px;")
        self.labelScenario.setFixedWidth(60)
        #positions
        buttons.addWidget(self.labelScenario, 0, 0, 1, 1)                             
        buttons.addWidget(self.uploadScenario, 0, 5, 1, 1)
        buttons.addWidget(self.textScenarioFile, 0, 1, 1, 4)
        #functions
        self.uploadScenario.clicked.connect(self.openScenarioFile)

        #1.2: Start
        self.startApp = QPushButton('Start')
        #style
        self.startApp.setStyleSheet("background-color:#608041; color: #ffffff; border-radius:15px; border:1px solid #dcdcdc; height: 30px; font-size: 13px;")
        #position
        buttons.addWidget(self.startApp, 1, 5, 1, 1)
        #function
        self.startApp.clicked.connect(self.startSystem)
        
        #2. Widgets for Scrollable Conversation history
        widgetScroll = QWidget()
        vBoxScroll = QVBoxLayout()
        widgetScroll.setLayout(vBoxScroll)        
        scroll = QScrollArea(widgetScroll)
        vBoxScroll.addWidget(scroll)
        #style and configurations
        scroll.setStyleSheet("border: 1px solid #dcdcdc; border-radius: 15px; font-size: 13px")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(300)
        scroll.setMinimumWidth(800)
        #change scroll of bar automatically - always at the bottom showing the most recent utterances
        bar = scroll.verticalScrollBar()
        bar.rangeChanged.connect(lambda x,y: bar.setValue(y))
        #content
        scrollContent = QWidget(scroll)       
        self.scrollLayout = QVBoxLayout(scrollContent)
        self.scrollLayout.addStretch(1)
        scrollContent.setLayout(self.scrollLayout)      
        scroll.setWidget(scrollContent)
        
        #3. Widget for user input
        self.grid = QGridLayout()
        widgetGrid = QWidget()
        widgetGrid.setLayout(self.grid)
                    
        #Add and show all widgets
        vBox.addWidget(widgetButtons)
        vBox.addWidget(widgetScroll)
        vBox.addWidget(widgetGrid)
        self.widget.show()
    
        sys.exit(app.exec_())
   
if __name__ == '__main__':
    App()
    