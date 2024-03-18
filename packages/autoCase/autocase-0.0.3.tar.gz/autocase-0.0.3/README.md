# AutoCase (WIP:Expect Major Changes)

Automatic AI based (optional) Camel / Snake / Pascal / Kebab / Train(Title) / Upper / Lower Case Conversion

# Latest Python Installation
```bash
git clone https://github.com/MohitBurkule/AutoCase.git
cd AutoCase
pip install -e .
```
# Pypi ( slightly older version)
```
pip install AutoCase
```
# Usage
## Basic Usage
```python
from autoCase import camel, snake, kebab, title

camel = camel("hello-world") # helloWorld
snake = snake("helloWorld") # hello_world
kebab = kebab("helloWorld") # hello-world
##title = title("helloWorld") # Hello World
```

## AI Based Conversion (Coming Soon)
```python
from autoCase import camel, snake, kebab, title

string = "helloworld"
camel = camel(string,ai=True,outputs=3) # [helloWorld, hellOworld, hellOWorld]
snake = snake(string,ai=True,outputs=3) # [hello_world, hell_oworld, hell_o_world]
pascal = pascal(string,ai=True,outputs=3) # [HelloWorld, HellOworld, HellOWorld]
kebab = kebab(string,ai=True,outputs=3) # [hello-world, hell-oworld, hell-o-world]
train = train(string,ai=True,outputs=3) # [Hello-World, Hell-Oworld, Hell-O-World]
upper = upper(string,ai=True,outputs=3) # [HELLO WORLD, HELL OWORLD, HELL O WORLD]
lower = lower(string,ai=True,outputs=3) # [hello world, hell oworld, hell o world]
```

## Dictionary Based Conversion (Coming Soon)
```python
from autoCase import camel, snake, kebab, title

word_list = ["hello","world","hell"]

string = "helloworld"
camel = camel(outputs=3) # [helloWorld, hellWorld, hellWorld]
snake = snake(outputs=3) # [hello_world, hell_world, hell_world]
pascal = pascal(outputs=3) # [HelloWorld, HellWorld, HellWorld]
kebab = kebab(outputs=3) # [hello-world, hell-world, hell-world]
train = train(outputs=3) # [Hello-World, Hell-World, Hell-World]
upper = upper(outputs=3) # [HELLO WORLD, HELL WORLD, HELL WORLD]
lower = lower(outputs=3) # [hello world, hell world, hell world]
```






