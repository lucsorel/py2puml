
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


## Tuple assignment

```python
self.u, self.v = (1, y)
```
node.targets[0] (ast.Tuple).elts

## Annotated assignment

```python
self.coordinates: Coordinates = Coordinates(x, y)
```
annotation (Name).id = 'Coordinates'

```python
self.unit: withenum.TimeUnit = withenum.TimeUnit.DAYS
```

annotation (Attribute).attr = 'TimeUnit'
annotation (Attribute).value (Name) = 'withenum'

```python
self.hour_unit: modules.withenum.TimeUnit = modules.withenum.TimeUnit.HOURS
```

annotation (Attribute).attr = 'TimeUnit'
annotation (Attribute).value (Attribute).attr = 'withenum'
annotation (Attribute).value (Attribute).value (Name) = 'modules'

print(class_module.modules.withenum.TimeUnit.__module__)
print(class_module.withenum.TimeUnit.__module__)

```python
self.z: str = z
```

annotation (Name).id = 'str'
target (Attribute).attr = 'z'
target.value (Name).id = 'self'
value (Name).id = 'z'

```python
self.l: List[int] = [1, 2]
```

annotation (Subscript) -> get_source_segment
annotation.value (Name).id = 'List'
annotation.slice (Index).value (Name).id = 'int'
target (Attribute).attr = 'l'
target.value (Name).id = 'self'


## Tuple assignment

```python
self.u, self.v = 1, y
```

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