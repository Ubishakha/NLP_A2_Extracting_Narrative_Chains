import chains
from pprint import pprint
import simplejson as json
import itertools

def parse_test_instance(story):
    """Returns TWO ParsedStory instances representing option 1 and 2"""
    # this is very compressed
    id = story.InputStoryid
    story = list(story)
    sentences = [chains.nlp(sentence) for sentence in story[2:6]]
    alternatives = [story[6], story[7]]
    return [chains.ParsedStory(id, id, chains.nlp(" ".join(story[2:6]+[a])), *(sentences+[chains.nlp(a)])) for a in alternatives]

def story_answer(story):
    """Tells you the correct answer. Return (storyid, index). 1 for the first ending, 2 for the second ending"""
    #obviously you can't use this information until you've chosen your answer!
    return story.InputStoryid, story.AnswerRightEnding

# Load training data and build the model
# data, table = chains.process_corpus("train.csv", 10000)

# load the pre-built model
with open("all.json", ) as fp:
    table = chains.ProbabilityTable(json.load(fp))
    
def get_pmi(deps):
    num = 0
    total_pmi= 0
    for i in range(0, len(deps)):
        for j in range(i, len(deps)):
            new_pmi = table.pmi(deps[i][0],deps[i][1],deps[j][0],deps[j][1])
            total_pmi += new_pmi
            num += 1
    #smoothing 
    num += 0.001
    return total_pmi/num

# # load testing data
test = chains.load_data("val.csv")
t = chains.load_data("val.csv")
num_correct = 0
total_num = len(list(t))
for t in test:
    one, two = parse_test_instance(t)
    
    one_deps = chains.extract_dependency_pairs(one)
    one_deps_list = one_deps[1][0]
    pmi1 = get_pmi(one_deps_list)
    
    two_deps = chains.extract_dependency_pairs(two)
    two_deps_list = two_deps[1][0]
    pmi2 = get_pmi(two_deps_list)
    
    chosen_ans = 1
    if pmi2>pmi1:
        chosen_ans = 2
    
    if chosen_ans == story_answer(t)[1]:
        num_correct += 1
    
print("Total correct ans:" + str(num_correct))
print("Total items in the set:" + str(total_num))
print("Accuraccy of the model: " + str((num_correct / total_num) * 100) + "%")

