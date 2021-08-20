class TreeNode:
    def __init__(self, passageId, nextPassageId, sentence, tags, addKnowledge = "", nextNodes = [], role = "", headNode = True):
        '''Initialize nodes of small dialogue trees (we can say cognitive resources as well)
        :param passageId: node identifier (aux)
        :param nextPassageId: list containing the identifiers of the nodes that follow the current node (aux)
        :param sentence: utterance associated with current node
        :param tags: list with the context and knowledge base tags of the node
        :param addKnowledge: knowledge to be added to the knowledge base given the node
        :param nextNodes: list with node objects that follow current node
        :param role: role associated with current node - can be kept empty if no role found
        :param headNode: bool that indicates if current node is head node of the tree
        '''
        self.passageId = passageId
        self.nextPassageId = nextPassageId
        self.sentence = sentence
        self.tags = tags
        self.addKnowledge = addKnowledge
        self.nextNodes = nextNodes
        self.role = role
        self.headNode = headNode
