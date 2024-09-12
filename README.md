# ChasmSystem

This package is a framework created to systematize and abstract the notions and
methods surrounding characters, monsters and other entities within the contexts
of RPGs and similar experiences.


## 💻 Requirements

So far, every package utilized in this project is native to the latest Python 3 version


## :file_folder: Documentation

The ChasmSystem is based off of 6 data classes:

- the [Die](#the-die)
- the [Entity](#the-entity)
- the [Weapon](#the-weapon)
- the [Aspect](#the-aspect)
- the [Ability](#the-ability)
- the [Game Master](#the-game-master)

> Every one of those follows the Builder design pattern, meaning that objects are configured through the layering of setter methods.
>
> Example:
> ```def entity():
    return Entity() \
        .set_attribute('Vit', 100) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330) \
        .add_aspects(base_aspect)```

### The Die

The Die class creates an object able to return random numbers based on it's predetermined configuration.

Its properties are:
- num_sides: the number of sides that the dice has.
- modifier:  a value to be added on top of the roll.
- scalar:    a value to multiply (scale) the rolled value

Its methods include:
- die.*set_num_sides*(_x_)
    Set the _num_sides_ property to x

### The Entity

### The Weapon

### The Aspect

### The Ability

### The Game Master