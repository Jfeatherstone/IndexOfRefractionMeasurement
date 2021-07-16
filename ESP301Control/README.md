## ESP301 Motion Controller Interface

This library is for controlling a rotation stage through an ESP301 Motion Controller in Python.

The manufacturer (see link 1 below) provides firmware for the piece of equipment, but it is not immediately obvious how to get it working in a modern programming language. One of the manuals on this page even has an example of using the code in Python, but it seems to be dismally out of date.

This library uses Python for .Net to load in the assembly file containing bindings for the motion controller, and then there is a lightweight wrapper to make things more user friendly.

I have included the assembly file in this folder, so you don't have to search your computer for the file, and to ensure that it is the exactly version that I am using.

For usage examples, see the `test` folder in the root of the repo.

### Requirements

- 64-bit Python (I used v3.8, but any >3 should work)
- pythonnet
- .NETCore v3.1 (or maybe .NET v5.0, honestly not totally sure)

### Further Resources

1. [ESP301 Product Page](https://www.newport.com/p/ESP301-3N)
