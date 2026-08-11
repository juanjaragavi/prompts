# PYTHON DATA ARCHITECTURE & TERMINOLOGY

## 1. CORE DATA TYPES

- Immutable (Fixed memory object): int, float, str, tuple, bool, frozenset
- Mutable (In-place modification): list, dict, set

## 2. ACCESS MECHANISMS

- Index-Based (list, tuple): Access via zero-based integer offset. Time complexity: O(1)
- Hash-Based (set, frozenset): Lookup via object hash value. Time complexity: Average O(1)
- Key-Value Pair (dict): Lookup value by hashing unique key. Time complexity: Average O(1)

## 3. DATA STRUCTURE MATRIX

- List: Ordered | Mutable | Duplicates | Index-based -> [1, 2]
- Tuple: Ordered | Immutable | Duplicates | Index-based -> (1, 2)
- Set: Unordered | Mutable | Unique Hashables | Hash-based -> {1, 2}
- Dict: Key-mapped | Mutable | Unique Keys | Key-Value -> {'a': 1}

## 4. ESSENTIAL TERMINOLOGY

- Parameter: Variable defined in function signature. Example: def func(param):
- Argument: Concrete value passed during function execution. Example: func(arg)
- type(obj): Evaluates exact class of an object.
- isinstance(obj, class): Validates if object is an instance/subclass (Preferred).
- String Immutability: Reassignment creates a new string object rather than modifying the existing memory block.
