import functools
from dataclasses import dataclass
from typing import List, Any
from typing import Set, Optional


@dataclass(frozen=True)
class PInt:
    pass


@dataclass(frozen=True)
class PBool:
    pass


@dataclass(frozen=True)
class PBit:
    size: int


@dataclass(frozen=True)
class SPrimitive:
    primitive: PInt | PBit | PBool


@dataclass(frozen=True)
class SVariant:
    variants: frozenset["Schema"]


@dataclass(frozen=True)
class SList:
    of: Optional["Schema"]


Schema = SList | SPrimitive | SVariant


def infer_schema_from_list(data: List[Any]) -> Schema:
    if not data:
        return SList(of=None)
    return functools.reduce(merge_schemas, map(infer_schema_from_one, data))


def infer_schema_from_one(data: Any) -> Schema:
    match data:
        case bool():
            return SPrimitive(PBool())
        case int():
            return SPrimitive(PInt())
        case bytes():
            return SPrimitive(PBit(len(data) * 8))
        case [first, *rest]:  # Matches a list of any size (at least one element)
            types: Set[Schema] = {infer_schema_from_one(first)}
            for item in rest:
                types.add(infer_schema_from_one(item))

            if len(types) > 1:
                return SList(SVariant(variants=frozenset(types)))
            else:
                return SList(next(iter(types)))
        case []:
            return SList(of=None)
        case _:
            raise ValueError(f"Cannot infer schema for {type(data)}")

def optimize_schema(schema: Schema) -> Schema:
    match schema:
        case SList(of):
            return SList(of=optimize_schema(of))

        case SVariant(variants=variants):
            new_variants = set()
            for variant in variants:
                if isinstance(variant, SVariant):
                    new_variants.update(optimize_schema(variant).variants)
                else:
                    new_variants.add(optimize_schema(variant))
            return SVariant(variants=frozenset(new_variants))
        case _:
            return schema

def flatten_variant(variants: frozenset) -> frozenset:
    result = set()
    for v in variants:
        if isinstance(v, SVariant):
            result.update(flatten_variant(v.variants))
        else:
            result.add(v)
    return frozenset(result)

def make_variant(variants: frozenset) -> Schema:
    if len(variants) == 1:
        return next(iter(variants))
    return SVariant(variants=variants)

def merge_schemas(a: Schema, b: Schema) -> Schema:
    if a == b:
        return a

    match (a, b):
        case (SPrimitive(_), SPrimitive(_)):
            return make_variant(frozenset({a, b}))
        case (SList(of=schema_a), SList(of=schema_b)):
            if schema_a is None:
                return SList(of=schema_b)
            if schema_b is None:
                return SList(of=schema_a)
            return SList(of=merge_schemas(schema_a, schema_b))
        case (SVariant(variants=variants_a), SVariant(variants=variants_b)):
            # Flatten nested variants
            flattened_a = flatten_variant(variants_a)
            flattened_b = flatten_variant(variants_b)
            return make_variant(flattened_a.union(flattened_b))
        case (SVariant(variants=variants), other) | (other, SVariant(variants=variants)):
            # Flatten variant and add the other schema
            flattened = flatten_variant(variants)
            return make_variant(flattened.union(frozenset({other})))
        case _:
            return make_variant(flatten_variant(frozenset({a, b})))

