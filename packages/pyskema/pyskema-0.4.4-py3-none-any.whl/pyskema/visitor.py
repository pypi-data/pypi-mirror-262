"""Schema base visitor.

:mod:`pyskema` uses the `visitor patter <https://en.wikipedia.org/wiki/Visitor_pattern>`_
to implement various operations on schema.
This module implement the base class that should be extended to implement such operation.
"""
from copy import deepcopy as copy
from .schema import Node, Atom, Union, Record, Collection, Map, Tuple
from typing import TypeVar, Generic


T = TypeVar('T')


class Visitor(Generic[T]):
    "The base visitor."

    def visit(self, node: Node, *args, **kwargs) -> T:
        "Visit a :class:`scheme.Node`."
        return node.structure.accept(self, *args, **kwargs)

    def visit_atom(self, atom: Atom, *args, **kwargs):
        "Visit an :class:`pyskema.schema.Atom` instance."
        pass

    def visit_union(self, union: Union, *args, **kwargs):
        "Visit an :class:`pyskema.schema.Union` instance."
        for node in union.options:
            self.visit(node, *args, **kwargs)

    def visit_record(self, rec: Record, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Record` instance."
        for _, node in rec.fields.items():
            self.visit(node, *args, **kwargs)

    def visit_collection(self, collection: Collection, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Collection` instance."
        self.visit(collection.element)

    def visit_map(self, map_: Map, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Map` instance."
        self.visit(map_.element)

    def visit_tuple(self, tup: Tuple, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Tuple` instance."
        for node in tup.fields:
            self.visit(node, *args, **kwargs)


class CopyingVisitor(Visitor):
    """A base for non mutating visitors.

    Similar to Visitor, but it should create an entirely new tree.
    """

    def visit(self, node: Node, *args, **kwargs) -> Node:
        "Visit a :class:`scheme.Node` and create a new one from the result."
        struct = node.structure.accept(self, *args, **kwargs)

        return Node(
            struct,
            node.description,
            node.optional,
            copy(node.default),
        )

    def visit_atom(self, atom, *args, **kwargs) -> Atom:
        return Atom(atom.type_, copy(atom.options))

    def visit_union(self, union, *args, **kwargs) -> Union:
        return Union([self.visit(node, *args, **kwargs) for node in union.options])

    def visit_record(self, rec, *args, **kwargs) -> Record:
        return Record({name: self.visit(node, *args, **kwargs) for name, node in rec.fields.items()})

    def visit_collection(self, collection, *args, **kwargs) -> Collection:
        return Collection(self.visit(collection.element, *args, **kwargs))

    def visit_map(self, map_, *args, **kwargs) -> Map:
        return Map(self.visit(map_.element, *args, **kwargs))

    def visit_tuple(self, tup, *args, **kwargs) -> Tuple:
        return Tuple([self.visit(node, *args, **kwargs) for node in tup.fields])
