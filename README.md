### Suspended
I've got into trouble with mathematics with understanding physics i want to put in the engine that are not in the book.  
I'm stopping development until I get enough base knowledge in mathematics.


# space
my python version of sample codes in Game Physics Engine Development  
also implemented omitted portions of source codes with help of [author's repository](https://github.com/idmillington/cyclone-physics)
all the codes are organized in each branches that corresponds to each chapter or example in the book  
check the branches

# Issues
### 1. Speed
If your code looks too fast or not working properly, you might not have initialized TimingData() or didn't call timing.update() in your overridden update() function.
timing.update() is called in main in the samples of book, but I couldn't find a way to share the variable between two modules like `extern TimingData timing;` in CPP, so each demo should have its own TimingData instance

### 2. Changes in some of the function prototypes
I tried to implement the functions same as possible to the original cpp code, but you might notice some of the functions are not exactly the same.
1. AFAIK, python doesn't support function overloading, but still make similar behaviour using `isinstance()`. you might wanna check if the function you are using has already taken care of different argument types or you can implement one of your own
2. For example, [this function](https://github.com/cd80/space/blob/master/demo/fireworks.py#L189) has its original prototypes in the [author's code](https://github.com/idmillington/cyclone-physics/blob/master/src/demos/fireworks/fireworks.cpp#L356) where there can be number as an argument or not. But it could look better to use if we just make it like `def create(self, type, parent, number=0)`.
