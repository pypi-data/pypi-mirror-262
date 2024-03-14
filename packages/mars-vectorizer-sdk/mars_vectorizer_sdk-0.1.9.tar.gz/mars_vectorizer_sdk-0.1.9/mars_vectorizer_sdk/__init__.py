import numpy as np

from dataclasses import dataclass, field
from typing import List, Union, Dict, Callable, Tuple, Optional
from functools import reduce
from itertools import starmap, chain
from hashlib import sha256

@dataclass
class Property:

    name: str
    value: Union[str, float]

    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the property.
        """
        return {
            "name": self.name,
            "value": self.value
        }

@dataclass
class Group:

    name: str
    values: List[Union["Group", Property]]

    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the group.
        """
        return {
            "name": self.name,
            "values": list(
                chain(
                    map(
                        lambda x: x.to_dict(),
                        filter(
                            lambda x: issubclass(x.__class__, Group),
                            self.values
                        ),
                    ),
                    map(
                        lambda x: x.to_dict(),
                        filter(
                            lambda x: issubclass(x.__class__, Property),
                            self.values
                        )
                    )
                )
            )
        }

@dataclass
class PropertyParser:

    name: str
    dtype: type
    path: List[str]

    def __call__(self, data: dict) -> Optional[Property]:
        try:
            return Property(
                name=self.name, 
                value=self.dtype(reduce(lambda x,y: x[y], self.path, data))
            )
        except:
            return None
        
    def sha256(self) -> str:
        return sha256((self.name + str(self.dtype) + "".join(self.path)).encode()).hexdigest()
        
@dataclass
class ListPropertyParser:

    name: str
    parser: Union["GroupParser", "PropertyParser"]
    path: List[str]

    def __call__(self, data: dict) -> Group:
        return Group(
            name=self.name,
            values=list(
                map(
                    self.parser, 
                    reduce(lambda x,y: x[y], self.path, data)
                )
            )
        )
    
    def sha256(self) -> str:
        return sha256((self.name + self.parser.sha256() + "".join(self.path)).encode()).hexdigest()
    
@dataclass
class GroupParser:

    name: str
    children: List[Union["GroupParser", "PropertyParser"]]

    def __call__(self, data: dict) -> Group:
        return Group(
            name=self.name,
            values=list(
                filter(
                    lambda x: x is not None, 
                    map(
                        lambda parser: parser(data), 
                        self.children
                    )
                )
            )
        )
    
    def sha256(self) -> str:
        return sha256((self.name + "".join(map(lambda x: x.sha256(), self.children))).encode()).hexdigest()
        
@dataclass
class VectorProperty:

    name: str
    vector: np.ndarray = field(repr=False)
    value: Union[str, float] = field(repr=False)

    def aggregate(self, weights: Dict[str, float] = {}) -> np.ndarray:
        return self.vector * weights.get(self.name, 1.0)
    
    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the property.
        """
        return {
            "name": self.name,
            "value": self.value,
            "vector": self.vector.tolist()
        }

@dataclass
class VectorGroup:

    name: str
    values: List[Union["VectorGroup", VectorProperty]]

    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the group.
        """
        return {
            "name": self.name,
            "values": list(
                chain(
                    map(
                        lambda x: x.to_dict(),
                        filter(
                            lambda x: issubclass(x.__class__, VectorGroup),
                            self.values
                        ),
                    ),
                    map(
                        lambda x: x.to_dict(),
                        filter(
                            lambda x: issubclass(x.__class__, VectorProperty),
                            self.values
                        )
                    )
                )
            )
        }

    def mapping(self) -> dict:
        """
            Returns a mapping from its name and value to its vector.
        """
        return dict(
            list(
                chain(
                    *map(
                        lambda x: x.mapping().items(),
                        filter(
                            lambda x: issubclass(x.__class__, VectorGroup),
                            self.values
                        ),
                    ),
                    map(
                        lambda x: ((self.name, x.name, x.value), x.vector),
                        filter(
                            lambda x: issubclass(x.__class__, VectorProperty),
                            self.values
                        )
                    )
                )
            )
        )

    def aggregate(self, weights: Dict[str, float] = {}, aggregator: Callable[[np.ndarray], np.ndarray] = lambda x: np.mean(x, axis=0)) -> np.ndarray:
        """
            Aggregates the vectors of the group. It will aggregate the vectors of the subgroups and the properties recursively.

            Args:
                agg: The aggregation function to be used.

            Returns:
                A VectorProperty with the aggregated vector.
        """
        return aggregator(
            np.array(
                list(
                    filter(
                        lambda x: not np.isnan(x).any(), 
                        chain(
                            map(
                                lambda x: x.aggregate(weights),
                                filter(
                                    lambda x: issubclass(x.__class__, VectorGroup),
                                    self.values
                                ),
                            ),
                            map(
                                lambda x: x.aggregate(weights),
                                filter(
                                    lambda x: issubclass(x.__class__, VectorProperty),
                                    self.values
                                )
                            )
                        )
                    )
                )
            )
        ) * weights.get(self.name, 1.0)

@dataclass
class Vectorizer:

    """
        Interface for vectorizers. Turns a Group into a VectorGroup.
        NOTE: Override `vectorize` function! This returns random vectors.
    """

    def __call__(self, group: Group) -> VectorGroup:
        return VectorGroup(
            name=group.name,
            values=list(
                chain(
                    map(
                        lambda sub_group: self(sub_group),
                        filter(
                            lambda x: issubclass(x.__class__, Group),
                            group.values
                        ),
                    ),
                    starmap(
                        lambda p, v: VectorProperty(
                            name=p.name,
                            vector=v,
                            value=p.value,
                        ),
                        zip(
                            filter(
                                lambda x: issubclass(x.__class__, Property),
                                group.values,
                            ),
                            self.vectorize(
                                list(
                                    filter(
                                        lambda x: issubclass(x.__class__, Property),
                                        group.values,
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    
    def vectorize(self, key_values: List[Tuple[str, Union[str, float]]]) -> np.ndarray:
        """
            Vectorizes a list of key-value pairs.

            Args:
                key_values: A list of key-value pairs.

            Returns:
                A numpy ndarray matrix
        """
        return np.random.uniform(
            -1.0, 1.0, 
            (
                len(key_values), 
                10
            )
        )
    
    def sha256(self) -> str:
        return sha256(self.__class__.__name__.encode()).hexdigest()
    