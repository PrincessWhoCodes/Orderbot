import os
import openai

openai.api_key  = "Add your API key"

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    
    return response.choices[0].message["content"]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))

    return pn.Column(*panels)

import panel as pn
pn.extension()
panels=[]

context=[
{'role':'system','content':"""
You are OrderBot, an automated service to collect orders for a classic cuisine cafe . \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
Pepperoni pizza  12.95, 10.00, 7.00 \
Cheese pizza   10.95, 9.25, 6.50 \
Veg extra cheese pizza   11.95, 9.75, 6.75 \
Red sauce pasta   5.78 , 13.5 , 10.0\
Italian cuisine    10.00 \
Chinese cuisine    10 \
Fries 4.50, 3.50 \
Greek salad 7.25 \
Toppings: \
Extra cheese 2.00, \
Mushrooms 1.50 \
Sausage 3.00 \
Black olives 3.50 \
AI sauce 1.50 \
Peppers 1.00 \
Drinks: \
Coke 3.00, 2.00, 1.00 \
Sprite 3.00, 2.00, 1.00 \
Bottled water 5.00 \
Caffe location: \
Seattle Washington,USA
"""}]
inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)
dashboard.show()
