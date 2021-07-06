
# Constructor arguments with annotation

```python
from typing import List

class Point:
    def __init__(self, x: int, y: str, z: List[int]):
        a = str(x) + y
        print('building')
        self.x = x
        self.y = y
        self.z = z
        # this should be ignored
        self.z[2] = x
        # it would be great to have self.w typed as int
        u: int = 0
        self.w = u
        # self.u & self.v should at least be found
        self.u, self.v = (1, y)
```

## Parsing approach

tree.body[0].args.args == [<_ast.arg object at ...e42715ad0>, <_ast.arg object at ...e42715390>, <_ast.arg object at ...e42715550>]

tree.body[0].args.args[0] == <_ast.arg object at 0x7fee42715ad0>
tree.body[0].args.args[0].arg == 'self'
tree.body[0].args.args[0].annotation == None

tree.body[0].args.args[1] == <_ast.arg object at 0x7fee42715390>
tree.body[0].args.args[1].arg == 'x'
tree.body[0].args.args[1].annotation == <_ast.Name object at 0x7fee42715150>
tree.body[0].args.args[1].annotation.id == 'int'

## Inspection approach

```python
Point.__init__.__annotations__ == {'x': <class 'int'>, 'y': <class 'str'>}
```

# Constructor assignments

tree.body[0].body == [<_ast.Assign object ...e42715290>, <_ast.Expr object at...e426f7890>, <_ast.Assign object ...e426f7750>, <_ast.Assign object ...e426f76d0>]

## Assignment to a 3rd party variable

tree.body[0].body[0] == <_ast.Assign object at 0x7fee42715290>
tree.body[0].body[0].targets[0] == <_ast.Name object at 0x7fee42715b10>
tree.body[0].body[0].targets[0].id == 'z'
tree.body[0].body[0].value == <_ast.Add object at 0x7fee52f12f10>


## Assignment to instance

tree.body[0].body[2] == <_ast.Assign object at 0x7fee426f7750>

tree.body[0].body[2].targets = [<_ast.Attribute obje...e426f7790>]
tree.body[0].body[2].targets[0] == <_ast.Attribute object at 0x7fee426f7790>
tree.body[0].body[2].targets[0].attr == 'x'
tree.body[0].body[2].targets[0].value == <_ast.Name object at 0x7fee426f7910>
tree.body[0].body[2].targets[0].value.id == 'self'

tree.body[0].body[2].value == <_ast.Name object at 0x7fee426f7850>
tree.body[0].body[2].value.id == 'x'

## Tuple assignment
self.u, self.v = 1, y
node.targets (assigned_target): ast.Tuple
.elts: List[Attribute] = [
    Attribute.attr = 'u'
    Attribute.value (ast.Name).id = 'self'
    ,
    same for v
]

node.value: ast.Tuple
.elts: List[Constant, Name]
Constant.value = 1
Name.id = 'y'