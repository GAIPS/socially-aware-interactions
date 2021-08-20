class Frame:
    def __init__(self, passageId, nextPassageId, tags, nextFrames = {}, cognitiveResources = [], startFrame = True):
        '''Initialize frame
        :param passageId: frame identifier (aux)
        :param nextPassageId: list containing the identifiers of the frames that follow the current frame (aux)
        :param tags: list with the context and knowledge base tags of the frame
        :param nextFrames: dictionary with the frame objects that follow the current frame and their respective frequency
        :param cognitive resources: list with the cognitive resources objects that are head nodes of a dialogue tree and that belong to the frame
        :param startFrame: bool that indicates if the frame is the initial frame of a practice - used only for starting the conversation if context is empty
        '''
        self.tags = tags
        self.nextFrames = nextFrames
        self.cognitiveResources = cognitiveResources
        self.passageId = passageId
        self.nextPassageId = nextPassageId
        self.startFrame = startFrame