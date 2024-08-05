def isTag(tuple, tag_prefix):
    if tuple[1][0]== tag_prefix:
        return True
    else:
        return False

def stripPunc(sent):
    return(sent.translate(str.maketrans('', '', string.punctuation)))
    
def question(sent="", debug=False):
    q_body = ""
    verb = ""
    MD_tag = ""
    Exist_tag = ""
    isProper = None
    isPrepositional = False
    isWh = False
    isMD = False
    isExist = False
    nounFound = False
    token = ""
    

    tagged_sent = pos_tag(word_tokenize(stripPunc(sent)))
    
    if debug:
        print(sent, end = "\n\n")
        print(tagged_sent, end = "\n\n")
    
    for idx,tuple in enumerate(tagged_sent):
        token = tuple[0]
        if tuple[1] == "." or tuple[1] == "," or tuple[1] == "CD":
            continue
        if tuple[1] == "IN":
            isPrepositional = True
            continue
        if isPrepositional and len(verb) == 0 and not isTag(tuple, "V"):
            continue
        if nounFound and idx > 1 and len(verb) > 0 and not isTag(tuple, "V"):
            break
        if idx == 0 and isTag(tuple, "W"):
            isWH = True
            break
        if tuple[1] == "MD":
            isMD = True
            MD_tag = token[0].upper() + token[1:]
            continue
        if tuple[1] == "EX":
            isExist = True
            Exist_tag = token[0].upper() + token[1:]
            continue
        if isTag(tuple, "V"):
            # Verb will always start with a lower case
            token = token[0].lower() + token[1:]
            if len(verb) == 0:
                verb = token
            else:
                verb += " " + token
        else:
            # Reached here if not a verb
            if tuple[1] == 'NNP' or tuple[1] == 'NNPS':
                nounFound = True
                if isProper is None:
                    isProper = True
            elif isTag(tuple, "N"):
                nounFound = True
                token = token[0].lower() + token[1:]
                if isProper is None:
                    isProper = False
                if idx == 0:
                    # if start of sentence and not proper, then make lower
                    token = token[0].lower() + token[1:]
            elif isTag(tuple, "P"):
                nounFound = True
                if not (tuple[1] == "PRP" and token == "I"):
                    # if start of sentence and not proper, then make lower
                    token = token[0].lower() + token[1:]
            else:
                # Reached here is not verb, or noun
                if not token.isupper():
                    token = token[0].lower() + token[1:]
            
            q_body += " " + token
            
    if isWh:
        if debug:
            print(sent,end="\n\n")
        return sent
    else:
        if isMD:
            q_body = MD_tag + q_body + " " + verb + "?"
        elif isExist:
            q_body = Exist_tag + q_body + " " + verb + "?"
        elif isProper:
            q_body = "Who " + verb + q_body + "?"
        else:
            q_body = "What " + verb + q_body + "?"
        if debug:
            print(q_body, end="\n\n")
        return q_body
