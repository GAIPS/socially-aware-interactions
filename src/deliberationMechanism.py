import random
class DeliberationMechanism:
    '''Class with system's deliberation mechanism (for agent responses and user inputs)'''
    def __init__(self, app):
        '''Initialize deliberation mechanism class
        :param app: system application in order to obtain data from the scenario file and call error events functions
        :var currSocialCtx and prevSocialCtx: list of current and previous social context tags
        :var currNode and prevNode: current and previous tree node objects
        :var knowledgeBase: list with knowledge base tags acquired during conversation
        :var user role, agent role, frames: relevant variables from the scenario file
        :var rand: initialize random - used to randomize choices between frames and resources
        '''
        self.app = app
                
        self.currSocialCtx = []
        self.currNode = None
        self.prevSocialCtx = None
        self.prevNode = None
        self.knowledgeBase= []
        
        self.inputFile = app.inputFile
        self.timeout = app.timeout      
        self.userRole = self.inputFile.userRole
        self.agentRole = self.inputFile.agentRole
        self.frames = self.inputFile.frames

        self.rand = random.SystemRandom()
        
    def respondAgentOutput(self, userInputNode):
        '''Agent's deliberation according to user input
        :param userInputNode: tree node of user input
        '''
        #Error Management
        #Timeout - check if user replied after timeout error activation to repeat sentence
        if self.timeout.timeoutRecoveryRepetition(userInputNode):
            return self.repetitionSentence()        
        #Timeout - check if user is not replying to activate error frame
        if self.timeout.timeoutRecoveryAcknowledge(userInputNode):
            self.activateErrorContext("timeout")
        else:
            #update context with tags
            self.currSocialCtx = userInputNode.tags
            #update knowledge base with add knowledge
            if userInputNode.addKnowledge != "":
                self.knowledgeBase.append(userInputNode.addKnowledge)
            #update current tree node
            self.currNode = userInputNode
        
        #check if we are still within dialogue tree - if tree is not finished dont change the context suddenly
        possibleNodes = self.getPossibleNodes()

        if len(possibleNodes) == 0:
            #find the frame that matches the current ctx+kb
            currFrame = self.getCurrentFrame(self.currSocialCtx)
            #find salient frames 
            salientFrames = self.salienceFrames(currFrame)
            #check if start nodes from those frames can be said by agent role
            possibleFrames = self.checkRoleFrames(salientFrames, self.agentRole)
            #no frames found - use current frame
            if len(possibleFrames) == 0:
                possibleFrames.append(currFrame)
            #random choice between salient frames
            salientFrame = self.rand.choice(possibleFrames)
            #update ctx with salient frame
            self.currSocialCtx = salientFrame.tags
            #check if start nodes from those frames' resources can be said by agent role
            possibleNodes = self.checkRoleResource(salientFrame, self.agentRole)

        #update current node
        self.currNode = self.rand.choice(possibleNodes)
        #update knowledge base if its the case
        if self.currNode.addKnowledge != "":
            self.knowledgeBase.append(self.currNode.addKnowledge)
        #return the agent response
        return self.currNode.sentence    
 
    def listUserOptions(self):
        '''Obtain user options according to the current context'''
        #check if we are still within dialogue tree - if tree is not finished dont change the context suddenly
        possibleNodes = self.getPossibleNodes()
        if len(possibleNodes) == 0:
            #find current frames, given ctx+kb
            currFrame = self.getCurrentFrame(self.currSocialCtx)
            #next frames are options
            nextFrames = self.checkStartApp(currFrame)
            #check if start nodes from those frames can be said by user role
            possibleFrames = self.checkRoleFrames(nextFrames, self.userRole)
            #no frames found - use current frame             
            if len(possibleFrames) == 0:
                possibleFrames.append(currFrame)
            #get possible nodes given possible frames and checking if those nodes can be used by user role
            possibleNodes = []
            for pf in possibleFrames:
                possibleNodes += self.checkRoleResource(pf, self.userRole)
        return possibleNodes
    
    ''' Error Recovery Funtions'''
    def repetitionSentence(self):
        '''Repeat previous sentence returning to previous social context'''
        self.currSocialCtx = self.prevSocialCtx
        self.currNode = self.prevNode
        return self.currNode.sentence   
    def activateErrorContext(self, error):
        '''Activate specific error frame'''
        self.prevSocialCtx = self.currSocialCtx
        self.prevNode = self.currNode
        self.currSocialCtx = [error]
        self.currNode = None
    
    ''' AUX Functions'''
    def salienceFrames(self, currFrame):
        ''' Compute most salient frames
        :param currFrame: current frame object to find nextFrames
        '''
        salientFrames = []
        maxSalience = 0
        for nf in currFrame.nextFrames:
            freq = currFrame.nextFrames[nf]
            kbMatch = len(list(set(nf.tags).intersection(self.knowledgeBase)))              
            res = freq + kbMatch #frequency plus knowledge base match equals the salience
            if  res > maxSalience:
                maxSalience = res
                salientFrames = [nf]
            elif res == maxSalience:
                salientFrames.append(nf)
        return salientFrames
    
    def checkStartApp(self, currFrame):
        '''Use start frames to show user options if we are starting the dialogue'''
        if currFrame is not None: #not starting app
            return currFrame.nextFrames.keys()
        else: #starting app
            auxNextFrames = []
            for f in self.frames:
                if f.startFrame:
                    auxNextFrames.append(f)
            return auxNextFrames
    
    def getPossibleNodes(self):
        '''Verify if current node is linked to other nodes to check if we are in the middle of a dialogue tree'''
        if self.currNode is not None and len(self.currNode.nextNodes) != 0:
            return self.currNode.nextNodes
        else:
            return []
    
    def getCurrentFrame(self, currCtx):
        '''Obtain current frame object given its tags'''
        currentFrame = None
        if len(currCtx) > 0:
            for f in self.frames:
                ctxMatch = True
                for c in currCtx: 
                    if c not in f.tags:
                        ctxMatch = False
                if ctxMatch:
                    currentFrame = f
        return currentFrame
    
    def checkRoleFrames(self, frames, role):
        '''Return the frames that have head nodes that can be said by a specific role'''
        possibleFrames = []
        for sf in frames:
            matchRole = False
            for cr in sf.cognitiveResources:
                if cr.role == role or cr.role == "":
                    matchRole = True
            if matchRole:
                possibleFrames.append(sf)
        return possibleFrames
    
    def checkRoleResource(self, frame, role):
        '''Return the head resources of a specific frame that can be said by a specific role'''
        possibleNodes = []
        for cr in frame.cognitiveResources:
            if cr.role == role or cr.role == "":
                possibleNodes.append(cr)
        return possibleNodes             