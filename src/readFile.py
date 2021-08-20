import json
import frame
import treeNode

class ReadFile:
    '''Class to read scenario JSON file'''
    def __init__(self, filename):
        '''Initialize read file class
        :param filename: name of the scenario file
        :var userRole: string with the social role of the user given in the scenario
        :var agentRole: string with the social role of the agent given in the scenario
        :var frames: list with the frame objects of the scenario
        :var treeNodes: list with the treeNode objects of the scenario
        :var timeoutCondition: maximum time to wait for user input in seconds given in the scenario
        '''
        self.filename = filename
        self.userRole = ""
        self.agentRole = ""
        self.frames = []
        self.treeNodes = []
        
        #Unexpected event variables
        #timeout
        self.timeoutCondition = 0
        
        #JSON File to data objects  
        self.readJsonFile()
        self.completeResourcesData()
        self.completeFramesData()
        
    def readJsonFile(self):
        '''Read the scenario file and loop through the passages to create the data objects'''
        #Open JSON file
        f = open(self.filename)
        #Returns JSON object as a dictionary
        data = json.load(f)
        #Loop through passages (Frames, roles and cognitive resources)
        for passage in data['passages']:
            #passage properties
            name = passage.get('name')
            pid = passage.get('pid')
            props = passage.get('props')
            tags = passage.get('tags')
            links = passage.get('links')           
            if tags is not None:
                if 'frame' in tags: #frames
                    tags.remove('frame')
                    nextPid = None
                    if links is not None:
                        for l in links:
                            nextPid = l['pid']
                    self.addFrameOrUpdateId(pid, nextPid, tags)
                    if "timeout" in tags: #timeout frame
                        self.timeoutCondition = int(props['timer'])
                elif 'roles' in tags: #roles
                    if props is not None:
                        self.userRole = props['user']
                        self.agentRole = props['agent']
                else: #cognitive resources
                    nextPid = []
                    if links is not None:
                        for l in links: #check for connections
                            nextPid.append(l['pid'])
                    #append new tree node to list of tree nodes
                    if props is not None:
                        self.treeNodes.append(treeNode.TreeNode(pid, nextPid, name, tags, props['addKnowledge'])) #resource has knowledge to add
                    else:
                        self.treeNodes.append(treeNode.TreeNode(pid, nextPid, name, tags))
        
    def addFrameOrUpdateId(self, pid, nextPid, tags):
        '''Create frame object or update its ids
        :param pid: list with the frame identifiers
        :param nextPid: list with the identifiers of the frames that follow this frame
        :param tags: knowledge and context tags of frame
        '''
        for f in self.frames:
            if f.tags == tags: #frame object already created - frames can be the same but every different ids
                f.passageId.append(pid) #append to its ids
                if nextPid is not None:
                    f.nextPassageId.append(nextPid) #append to the ids of the following frames
                return
        #frame object was not yet created
        if nextPid is not None:
            newFrame = frame.Frame([pid], [nextPid], tags)
        else:
            newFrame = frame.Frame([pid], [], tags)
        #Append new frame to list of frames    
        self.frames.append(newFrame)
    
    def completeResourcesData(self):
        '''Complete resources data (roles, next nodes, head node)'''
        for n in self.treeNodes:
            #roles
            tags = n.tags
            if self.userRole in tags: #extract user role from tags
                n.role = self.userRole
                tags.remove(self.userRole)
            elif self.agentRole in tags: #extract agent role from tags
                n.role = self.agentRole
                tags.remove(self.agentRole)
            #next nodes  
            nextNodes = n.nextPassageId
            n.nextNodes = []
            for nn in self.treeNodes:
                if nn.passageId in nextNodes:
                    n.nextNodes.append(nn) #append node objects that follow current node to the nextNodes list of the current tree node
                    nn.headNode = False #if next node is linked after current node it cannot be a head node
                    
    def completeFramesData(self):
        '''Complete frames data (next frames and frequency, start frame, cognitive resources)'''
        for f in self.frames:
            #next frames
            nextFrames = f.nextPassageId
            nextFramesAux = []
            for nf in self.frames:
                passageIdAux = nf.passageId
                tags = nf.tags
                #Error start frame exception
                if "timeout" in tags:
                    nf.startFrame = False #even though timeout frame is not linked to any frame it should not be a start frame, this bool should be only true for frames starting a practice (e.g., greeting)
                for pI in passageIdAux:
                    if pI in nextFrames:
                        nextFramesAux.append(nf) #append frame objects that follow current frame to aux list
                        nf.startFrame = False 
            f.nextFrames = self.countFrequency(nextFramesAux) #create dictionary with frequency of frames that follow current frame
        #cognitive resources
        for f in self.frames:
            f.cognitiveResources = []
            for n in self.treeNodes:
                if n.tags == f.tags and n.headNode: #obtain tree nodes that are associated with current frame and that are head nodes - the start of the dialogue trees will be useful for the deliberation mechanism
                    f.cognitiveResources.append(n)   
    
        
    def countFrequency(self, lst):
        '''Transform a list to a dictionary with objects and their frequency (number of times they appear on the list)
        :param lst: the list that will be transformed into a dictionary
        '''   
        count = {}
        for i in lst:
            count[i] = count.get(i, 0) + 1
        return count