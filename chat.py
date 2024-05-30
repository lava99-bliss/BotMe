import random #beacuse later we need to check for rand ansrs
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

#pass saved data to this file
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval() #evaluate

bot_name = "BotMe"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words) #BOW is a numpy array
    X = X.reshape(1, X.shape[0]) #1 row at a time.(input->1 sentence) and no of features
    X = torch.from_numpy(X).to(device) #convert BOW to torch tensor

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()] #tags=>sorted tags list
    # .item() returns a number

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() >= 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "Sorry I dont get you..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        response  = get_response(sentence)
        print(response )
