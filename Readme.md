# Proto Parser

This module provides functionality to parse and manipulate a robot structure from a proto file.

## Classes

### proto_robot

Represents the robot structure parsed from a proto file.

- **Attributes:**
  - `header` (str): The header of the proto file.
  - `children` (list): The list of child nodes.
  - `cursor` (proto_robot): The current node in the structure.
  - `parent` (proto_robot): The parent node of the current node.

- **Methods:**
  - `__init__`: Initializes the proto_robot object.
  - `add_child(child)`: Adds a child to the current node.
  - `set_current(child)`: Sets the current node.
  - `read_proto_file(proto_filename)`: Reads a proto file and builds the robot structure.
  - `search(name)`: Searches the robot structure with the given name.
  - `save_robot()`: Saves the robot structure to a file.
  - `__str__`: Returns the string representation of the robot structure.
  - `__repr__`: Returns the string representation of the robot structure.
  - `__dict__`: Returns the dictionary representation of the robot structure.

### structure

Base class for different parts of the robot structure.

- **Attributes:**
  - `name` (str): The name of the structure.
  - `stage` (int): The stage of the structure.
  - `parent` (structure): The parent structure.
  - `children` (list): The list of child structures.
  - `DEF` (str): The DEF attribute of the structure.

- **Methods:**
  - `__init__(name, parent, stage=0, DEF=None)`: Initializes the structure object.
  - `add_child(child)`: Adds a child to the structure.
  - `search(name)`: Searches the structure with the given name.
  - `__str__`: Returns the string representation of the structure.
  - `__repr__`: Returns the string representation of the structure.

### Node

Represents a node in the robot structure.

- **Attributes:**
  - `name` (str): The name of the node.
  - `parent` (structure): The parent structure.
  - `DEF` (str): The DEF attribute of the node.
  - `stage` (int): The stage of the node.

- **Methods:**
  - `__init__(name, parent, DEF=None, stage=0)`: Initializes the Node object.
  - `get_self_only()`: Returns the string representation of the node itself.
  - `__str__`: Returns the string representation of the node.
  - `__dict__`: Returns the dictionary representation of the node.

### property

Represents a property in the robot structure.

- **Attributes:**
  - `name` (str): The name of the property.
  - `parent` (structure): The parent structure.
  - `stage` (int): The stage of the property.
  - `content` (str): The content of the property.

- **Methods:**
  - `__init__(name, parent, stage=0, content="")`: Initializes the property object.
  - `get_self_only()`: Returns the string representation of the property itself.
  - `__str__`: Returns the string representation of the property.
  - `__dict__`: Returns the dictionary representation of the property.

### container

Represents a container in the robot structure.

- **Attributes:**
  - `name` (str): The name of the container.
  - `parent` (structure): The parent structure.
  - `DEF` (str): The DEF attribute of the container.
  - `stage` (int): The stage of the container.

- **Methods:**
  - `__init__(name, parent, DEF=None, stage=0)`: Initializes the container object.
  - `get_self_only()`: Returns the string representation of the container itself.
  - `__str__`: Returns the string representation of the container.
  - `__dict__`: Returns the dictionary representation of the container.

## Usage

The script can be run as a standalone program to open a proto file, parse it, and save the modified robot structure.