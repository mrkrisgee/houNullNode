import hou

def createNull():
    node = hou.pwd()  
    
    ### Iterate over nodes
    for i in hou.selectedNodes():
        if hou.nodeTypeCategories().keys(): # allow this function to be called in any context
            print(hou.nodeTypeCategories().keys())
            
            ### Get output connections
            outputCons = i.outputConnections() #########################
            
            ### Set new node parms
            dir = i.parent().path() + "/"
            selNodeName = i.name()
            
            ### Create small window for user input
            inputName = hou.ui.readInput(f"Create Null Node for {selNodeName}", buttons=( "OK", "Cancel"))
            ### Break if "Cancel" is pressed
            if inputName[0] == 1:
                break;
            ### Get input and replace spaces
            inputName = inputName[1].replace(" ", "_");
            ### Concat "OUT_" into name
            inputName = f"OUT_{inputName}"
            
            ### Create new null
            nullNode = i.createOutputNode("null", inputName)
            ### Set colour
            nullNode.setColor(hou.Color( [0.302, 0.525, 0.114] ))
            ### Set flags
            i.setSelected(0)
            ### Try/Except code block for alternative contexts other than SOP's
            try:
                if i.setRenderFlag(0): # Sanity check for render flag
                    nullNode.setSelected(1)
                    nullNode.setDisplayFlag(1)
                    nullNode.setRenderFlag(1)
            except:
                pass
                
            ### Allow null to be created correctly within a chain of nodes
            for con in outputCons:
                idx = con.inputIndex()
                if ( con.inputItem().name() == i.name()):
                    con.outputItem().setInput( idx, nullNode, 0 )
            
            return nullNode          

            
def renameNull():

    ### Iterate over nodes
    for node in hou.selectedNodes():
        if hou.nodeTypeCategories().keys(): # allow this function to be called in any context
            ### Get node name
            nodeName = node.name()
            ### Get first 4 elems of string list
            namePrefix = nodeName[:4]        
            ### Add "OUT_" to name if it doesn't have one
            if ( namePrefix != "OUT_" ):
                newString = f"OUT_{nodeName}"
                ### Set name
                node.setName(newString)
                ### Set colour
                node.setColor(hou.Color( [0.302, 0.525, 0.114] ))
            else:
                ### Set colour
                node.setColor(hou.Color( [0.302, 0.525, 0.114] )) 
            
            return node
            
def createOM(node):
    
    ### Remove "OUT_" prefix from the name if it has one
    currName = node.name()
    if ( currName[:4] == "OUT_" ):
        currName = currName[4:]  

    ### Init new name
    newName = "IN_" + currName
    ### Store node position
    selNodePos = node.position()
    ### Get parent directory
    parentDir = node.parent().path() + "/"
    ### Set node directory
    nodeDir = f"../{node}"
    ### Create new node
    newNode = hou.node(f"/{parentDir}").createNode("object_merge", newName)
    
    ### Node positioning
    newNode.setPosition(hou.Vector2(selNodePos[0]+1.5,selNodePos[1]-1))  
    ### Set parms
    newNode.parm("objpath1").set(f"../{node}")
    newNode.parm("xformtype").set(1)
    ### Set shape
    newNode.setUserData("nodeshape", "chevron_down")
    ### Set colour
    newNode.setColor(hou.Color( [0.094, 0.369, 0.69] ))
    
    ### Set display flags
    node.setSelected(0)
    newNode.setSelected(1)
            
    
### Iterate over nodes
for node in hou.selectedNodes():

    ### Get node type name
    nodeType = node.type().name()
    
    ### Handle nulls
    if ( nodeType != "null" ):
        node = createNull()
    else:
        node = renameNull()
    
    ### Create object merge
    ### Try/Except code block for alternative contexts other than SOP's that do not support object merges
    try: 
        createOM(node)
    except:
        pass
        
