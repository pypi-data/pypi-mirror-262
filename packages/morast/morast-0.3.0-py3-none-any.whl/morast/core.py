# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-

"""

morast.core

Core functionality


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import ast
import collections
import logging
import pathlib
import re

from threading import Lock
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from smdg import elements as mde
from smdg import strings as mds

from morast import configuration
from morast import commons
from morast import nodes
from morast import overrides


#
# Constants
#


CLASS_METHOD = 0
STATIC_METHOD = 1
INSTANCE_METHOD = 2
MODULE_LEVEL_FUNCTION = 9

METHOD_TYPES: Tuple[str, str, str] = (
    "Class method",
    "Static method",
    "Instance method",
)

TYPES_BY_DECORATOR: Dict[str, int] = {
    "classmethod": CLASS_METHOD,
    "staticmethod": STATIC_METHOD,
}

SCOPE_CLASS = "class"
SCOPE_INSTANCE = "instance"
SCOPE_MODULE = "module"

METHOD_TARGETS: Dict[int, str] = {
    CLASS_METHOD: SCOPE_CLASS,
    STATIC_METHOD: SCOPE_CLASS,
    INSTANCE_METHOD: SCOPE_INSTANCE,
}

EXCLUDED_MODULE_VARIABLES: Tuple[str, ...] = ("__all__",)

PRX_DATACLASS = re.compile("^(?:dataclasses\\.)?dataclass(?!\\w)")


#
# Functions
#


def morast_prefix(name: str) -> str:
    """Prefix _name_ with `'MoRAST:'`"""
    return f"{commons.BRAND}:{name}"


_MORAST_VERBATIM = morast_prefix("verbatim")
_MORAST_BASES = morast_prefix("bases")
_MORAST_DOCSTRING = morast_prefix("docstring")
_MORAST_SIGNATURE = morast_prefix("signature")
_MORAST_ADVERTISEMENT = morast_prefix("generator")


def camel_to_snake_case(name: str) -> str:
    """Convert _name_ (an identifier) from CamelCase
    to lower\\_snake\\_case
    """
    output_collector: List[str] = []
    for index, character in enumerate(name):
        if character.isupper():
            character = character.lower()
            if index:
                output_collector.append(commons.UNDERSCORE)
            #
        output_collector.append(character)
    #
    return "".join(output_collector)


#
# Classes
#


class IgnoredItem(Exception):
    """Raised when an Item is ignored"""

    def __init__(self, message: str) -> None:
        """Store the message"""
        self.message = message


# =============================================================================
# @dataclasses.dataclass
# class SectionStorage:
#     """Store a section nameant its subsections"""
# =============================================================================


class EmojiProxy:
    """Object providing emoji if enabled"""

    def __init__(self, emoji: configuration.EmojiConfiguration) -> None:
        """Store _emoji_ internally"""
        self.__emoji = emoji
        self.__cache: Dict[str, str] = {}
        self.__provide_preset(
            "todo_prefix", "missing_documentation_prefix", "TODO:"
        )

    def __provide_preset(
        self, name: str, emoji_name: str, default: str
    ) -> None:
        """Provide a preset in the cache"""
        self.__cache[name] = self[emoji_name] or default

    def __getitem__(self, name: str) -> str:
        """Get the matching emoji by name if enabled,
        else an empty string
        """
        try:
            return self.__cache[name]
        except KeyError:
            pass
        #
        if not self.__emoji.enabled:
            return self.__cache.setdefault(name, "")
        #
        found_emoji = getattr(self.__emoji, name)
        if isinstance(found_emoji, str):
            return self.__cache.setdefault(name, found_emoji)
        #
        raise KeyError(name)

    def __getattr__(self, name: str) -> str:
        """Get the matching emoji by name if enabled,
        else an empty string
        """
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(f"no attribute {name!r}") from error
        #


class SuperConfig:
    """Object holding a part of the configuration,
    existing overrides and an OrderedDict of
    extracted OverridesSection objects
    """

    def __init__(
        self,
        module_overrides=overrides.DUMMY_MOD_OVERRIDES,
        options=configuration.DUMMY_OPTIONS,
    ) -> None:
        """Initialize by storing the overrides
        and building a text module proxy
        """
        self.mor = module_overrides
        self.emoji = EmojiProxy(options.emoji)
        self.advertise = options.advertise
        self._extracted_sections: collections.OrderedDict[
            Tuple[str, ...],
            Tuple[MorastDocumentableItem, overrides.OverridesSection],
        ] = collections.OrderedDict()

    def get_nested_sections(
        self,
        *name_parts: str,
    ) -> Iterator[overrides.OverridesSection]:
        """Return an iterator over extracted override sections,
        in correct order (nested, attributes before functions and classes),
        starting at the name built from _name_parts_.
        """
        attributes: List[Tuple[str, ...]] = []
        functions: List[Tuple[str, ...]] = []
        classes: List[Tuple[str, ...]] = []
        for sub_name_parts, (candidate, _) in self._extracted_sections.items():
            if len(sub_name_parts) != len(name_parts) + 1:
                continue
            #
            # logging.warning("%r -> %r ???", name_parts, sub_name_parts)
            if sub_name_parts[: len(name_parts)] != name_parts:
                # logging.warning(" -> no")
                continue
            #
            # logging.warning(" -> yes")
            if isinstance(candidate, MorastFunctionDef):
                functions.append(sub_name_parts)
            elif isinstance(candidate, MorastClassDef):
                classes.append(sub_name_parts)
            else:
                attributes.append(sub_name_parts)
            #
        #
        yield self._extracted_sections[name_parts][1]
        for sub_name_parts in attributes + functions + classes:
            yield from self.get_nested_sections(*sub_name_parts)
        #

    def extract_overrides(
        self,
        item: "MorastDocumentableItem",
        namespaced_name: str,
        section: overrides.OverridesSection,
    ):
        """Store the overrides section"""
        self._extracted_sections[tuple(namespaced_name.split(commons.DOT))] = (
            item,
            section,
        )


DUMMY_SUPERCONFIG = SuperConfig()


# pylint: disable=too-many-instance-attributes


class MorastDocumentableItem:
    """Documentable item"""

    kind = overrides.KIND_UNSPECIFIED

    def __init__(
        self,
        name: str,
        namespace: str = "",
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        """Store the attributes and initialize
        the internal collection of contained items.
        """
        self.name = name
        self.namespace = namespace
        if namespace:
            self.namespaced_name = f"{namespace}.{name}"
        else:
            self.namespaced_name = name
        #
        self.scope = scope
        self.sc = superconfig
        # self.overrides_docstring
        # = self.sc.mor[self.namespaced_name].docstring
        self.original_docstring = True
        self.docstring: str = commons.EMPTY
        self.is_ignored = False

    def check_private(self) -> None:
        """Check if this is a private member"""
        if self.name.startswith(commons.UNDERSCORE):
            raise IgnoredItem(
                f"{self.namespace}: ignored private member {self.name!r}"
            )
        #

    def check_ignored(self) -> bool:
        """Check for self.is_ignored"""
        if self.is_ignored:
            raise IgnoredItem(
                f"{self.namespace}: ignored {self.name!r} as specified"
                " through override"
            )
        #
        return False

    def set_docstring_from_override(self) -> None:
        """Set the final docstring,
        either from the override if set there,
        or from its former value.

        This method also sets the _is\\_ignored_ flag.
        """
        override_section = self.sc.mor.setdefault(
            self.namespaced_name,
            kind=self.kind,
            namespace=self.namespace,
        )
        if override_section.is_ignored:
            self.is_ignored = True
        #
        if self.docstring:
            if override_section.docstring:
                self.docstring = override_section.docstring
                self.original_docstring = False
            #
        else:
            if (
                not override_section.docstring
                and not override_section.is_ignored
            ):
                override_section.add_to_docstring(
                    f"{self.sc.emoji.todo_prefix} **{self.namespaced_name}**"
                    " documentation _to be added_"
                )
            #
            self.docstring = override_section.docstring
            self.original_docstring = False
        # Always add the extracted override section
        self.sc.extract_overrides(self, self.namespaced_name, override_section)
        # return output_docstring

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        yield mde.Paragraph(self.namespaced_name)
        yield nodes.DocString(self.docstring).as_markdown()

    def as_markdown(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        if not self.is_ignored:
            yield from self.markdown_elements()
        #


# pylint: enable=too-many-instance-attributes


class MorastAttribute(MorastDocumentableItem):
    """A (module, class, or instance) attribute"""

    supported_scopes = (SCOPE_CLASS, SCOPE_INSTANCE, SCOPE_MODULE)

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        element: Union[ast.Assign, ast.AnnAssign, ast.AugAssign],
        namespace: str = "",
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
        check_self: bool = False,
    ) -> None:
        """Store the attributes and initialize
        the internal collection of contained items.
        """
        if scope not in self.supported_scopes:
            raise ValueError(f"scope must be one of {self.supported_scopes!r}")
        #
        prefix_by_scope: Dict[str, str] = {
            SCOPE_CLASS: f"{superconfig.emoji.class_attributes_prefix}"
            f" {namespace}",
            SCOPE_INSTANCE: f"{superconfig.emoji.instance_attributes_prefix} ",
            SCOPE_MODULE: f"{superconfig.emoji.constants_prefix} {namespace}",
        }
        logging.debug(ast.dump(element))
        assignment = nodes.Assignment(
            element, prefix=f"{prefix_by_scope[scope]}."
        )
        logging.debug(str(assignment))
        name = str(assignment.target)
        kind = overrides.KIND_CONSTANT
        if scope == SCOPE_INSTANCE:
            kind = overrides.KIND_INSTANCE_ATTRIBUTE
            if check_self:
                if name.startswith("self."):
                    assignment.strip_first()
                    name = str(assignment.target)
                else:
                    raise IgnoredItem(f"{name}: no instance attribute")
                #
            #
        elif scope == SCOPE_CLASS:
            kind = overrides.KIND_CLASS_ATTRIBUTE
        #
        if commons.DOT in name:
            raise IgnoredItem(f"{name}: ignored namespaced assignment")
        #
        super().__init__(
            name,
            namespace=namespace,
            scope=scope,
            superconfig=superconfig,
        )
        logging.debug("ATTRIBUTE NAME: %s", name)
        logging.debug("ATTRIBUTE SCOPE: %s", scope)
        logging.debug("ATTRIBUTE KIND: %s", kind)
        self.check_private()
        self.kind = kind
        self.set_docstring_from_override()
        self.check_ignored()
        self.assignment = assignment
        if self.sc.mor[self.namespaced_name].value_is_stripped:
            self.assignment.operator = None
        #

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        yield mde.Paragraph(self.assignment.as_markdown())
        yield nodes.DocString(self.docstring).as_markdown()

    def as_md_list_item(self) -> mde.ListItem:
        """Return aa a MarkDown list item"""
        return mde.ListItem(*self.markdown_elements())


class MorastSection(MorastDocumentableItem):
    """Documentation section with a headline and other nodes.
    May also contain other sections.

    Initialization arguments:

    * _name_: the name of the section (public attribute)
    * _level_: section level in the document hierarchy
    * _headline_: deviant headline if provided
      (else, the headline will just be _name_)

    Keeps an internal collection of contained
    MorastBaseNode and MorastSection instances.
    """

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        name: str,
        namespace: str = "",
        scope=SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
        level: int = 1,
        headline: Optional[str] = None,
    ) -> None:
        """Store the attributes and initialize
        the internal collection of contained items.
        """
        super().__init__(
            name, namespace=namespace, scope=scope, superconfig=superconfig
        )
        if isinstance(headline, str):
            self._headline = headline
        else:
            self._headline = self.name
        #
        self._level = level
        self._contents: collections.OrderedDict[
            str, Union[nodes.MorastBaseNode, MorastDocumentableItem]
        ] = collections.OrderedDict()
        self._naming_lock = Lock()

    def __getitem__(
        self,
        name: str,
    ) -> Union[nodes.MorastBaseNode, MorastDocumentableItem]:
        """Directly return the node or subsection stored as _name_"""
        return self._contents[name]

    def __len__(self) -> int:
        """Total number of contained nodes and subsections"""
        return len(self._contents)

    def items(
        self,
    ) -> Iterator[
        Tuple[str, Union[nodes.MorastBaseNode, MorastDocumentableItem]]
    ]:
        """Return an iterator (_name_, _item_ tuples)
        over all contained nodes and subsections
        """
        yield from self._contents.items()

    def subsections(self) -> Iterator[Tuple[str, "MorastSection"]]:
        """Return an iterator (_name_, _subsection_ tuples)
        over all contained subsections"""
        for sub_name, subnode in self.items():
            if isinstance(subnode, MorastSection):
                yield sub_name, subnode
            #
        #

    def adjust_level(self, new_level: int) -> None:
        """Change the level to _new\\_level_,
        recurse into all subsections and
        propagate the change.
        If a docstring is present,
        adjust its level as well.
        """
        # return None
        self._level = new_level
        for _, child_section in self.subsections():
            child_section.adjust_level(new_level + 1)
        #
        try:
            docstring = self[_MORAST_DOCSTRING]
        except KeyError:
            return
        #
        if isinstance(docstring, nodes.DocString):
            docstring.adjust_level(new_level)
        #

    def _get_unique_name(self, name: str) -> str:
        """Return a new unique name instead of _name_.
        Should be called only while holding `self._naming_lock`.
        """
        number = 0
        candidate = name
        while candidate in self._contents:
            number += 1
            candidate = f"{name}_{number}"
            if number > 1000:
                raise ValueError("Exhausted renaming attempts")
            #
        #
        return candidate

    def add_subnode(
        self,
        name: str,
        subitem: Union[nodes.MorastBaseNode, "MorastSection"],
    ) -> None:
        """Add _subitem_ (a node or section)
        and make it accessible through _name_.
        """
        self._contents.setdefault(name, subitem)
        if subitem is not self._contents[name]:
            with self._naming_lock:
                unique_name = self._get_unique_name(name)
                self._contents[unique_name] = subitem
            #
        #

    def add_subsection(
        self,
        name: str = "undefined",
        subsection: Optional["MorastSection"] = None,
    ) -> None:
        """Add a new subsection.
        If a MorastSection instance is provided through _subsection_,
        store it, make it available under its own name,
        and adjust its level to reflect the sections hierarchy.
        else initialize a new one and and make it available as _name_.
        """
        if subsection is None:
            subsection = MorastSection(name, level=self._level + 1)
        else:
            sub_name = subsection.name
            subsection.adjust_level(self._level + 1)
        #
        self.add_subnode(sub_name, subsection)

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements for all
        contained nodes, recursing into all subsections.
        """
        if self._level > 1:
            yield nodes.MD_HR20
        #
        logging.debug("Section: %r", self.name)
        yield mde.Header(self._level, self._headline)
        for sub_name, sub_element in self._contents.items():
            logging.debug("MarkDown Elements from: %r", sub_name)
            if isinstance(sub_element, MorastDocumentableItem):
                yield from sub_element.markdown_elements()
            else:
                yield sub_element.as_markdown()
            #
        #


class MorastAttributesList(MorastSection):
    """Attributes List"""

    supported_scopes = (SCOPE_CLASS, SCOPE_MODULE)

    def __init__(
        self,
        name: str,
        superconfig=DUMMY_SUPERCONFIG,
        scope: str = SCOPE_MODULE,
        headline: Optional[str] = None,
    ) -> None:
        """Store the attributes and initialize
        the internal collection of contained items.
        """
        level = 2 if scope == SCOPE_MODULE else 4
        super().__init__(
            name,
            namespace="",
            scope=scope,
            superconfig=superconfig,
            level=level,
            headline=headline,
        )
        self._attributes: collections.OrderedDict[str, MorastAttribute] = (
            collections.OrderedDict()
        )

    def add(self, mor_attr: MorastAttribute) -> None:
        """Store _mor_attr_ under its name"""
        self._attributes[mor_attr.name] = mor_attr

    def remove(self, attr_name) -> None:
        """Remove the attribute named _attr_name_ if it exists"""
        self._attributes.pop(attr_name, None)

    def __len__(self) -> int:
        """Total number of contained nodes and subsections"""
        return len(self._attributes)

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Yield markdown elements"""
        yield mde.Header(self._level, self._headline)
        md_list_items: List[mde.ListItem] = []
        for mor_attr in self._attributes.values():
            md_list_items.append(mor_attr.as_md_list_item())
        #
        yield mde.UnorderedList(*md_list_items)


class MorastFunctionDef(MorastSection):
    """Represents a module-level function,
    or a class, static, or instance method.

    Initialization arguments:

    * _element_: the ast.FunctionDef instance from which
      the function name, signature and docstring are determined
    * _level_: the level in the document hierarchy:
      `3` for module-level functions,
      `4` for methods
    * _function\\_type_: the function type
    * _parent\\_name_: the name of the containing parent (module or class)
    """

    supported_scopes = (SCOPE_CLASS, SCOPE_INSTANCE, SCOPE_MODULE)

    # pylint: disable=too-many-branches

    def __init__(
        self,
        element: ast.FunctionDef,
        namespace: str = "",
        superconfig=DUMMY_SUPERCONFIG,
        scope: str = SCOPE_MODULE,
    ) -> None:
        """Determine and store attributes"""
        parent_name = namespace.split(commons.DOT)[-1]
        self.function_type = MODULE_LEVEL_FUNCTION
        level = 3
        if scope != SCOPE_MODULE:
            level = 4
            self.function_type = INSTANCE_METHOD
            for dec in element.decorator_list:
                if isinstance(dec, ast.Name):
                    try:
                        self.function_type = TYPES_BY_DECORATOR[dec.id]
                    except KeyError:
                        continue
                    #
                    break
                #
            #
        #

        name = element.name
        logging.debug("%s - accepted %s", namespace, name)
        skip_first_arg = False
        if self.function_type in (CLASS_METHOD, INSTANCE_METHOD):
            skip_first_arg = True
        #
        if self.function_type == INSTANCE_METHOD:
            headline_prefix = f"{camel_to_snake_case(parent_name)}_instance."
            signature_prefix = "."
            kind = overrides.KIND_INSTANCE_METHOD
        else:
            signature_prefix = f"{parent_name}."
            if self.function_type == MODULE_LEVEL_FUNCTION:
                headline_prefix = "Function: "
                kind = overrides.KIND_FUNCTION
            else:
                headline_prefix = signature_prefix
                kind = overrides.KIND_CLASS_METHOD
            #
        #
        if self.function_type == STATIC_METHOD:
            signature_prefix = f"staticmethod {signature_prefix}"
        #
        super().__init__(
            name,
            namespace=namespace,
            scope=scope,
            superconfig=superconfig,
            level=level,
            headline=f"{headline_prefix}{name}()",
        )
        self.check_private()
        ds_level = 1
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr):
                # self.docstring =
                if isinstance(sub_element.value, ast.Constant):
                    self.docstring = sub_element.value.value
                    ds_level = self._level
                    break
                #
            #
        #
        signature_prefix = (
            f"{self.sc.emoji.signature_prefix} {signature_prefix}"
        )
        self.add_subnode(
            _MORAST_SIGNATURE,
            nodes.Signature(
                self.name,
                element.args,
                returns=element.returns,
                prefix=signature_prefix,
                skip_first_arg=skip_first_arg,
            ),
        )
        self.kind = kind
        self.set_docstring_from_override()
        self.check_ignored()
        self.add_subnode(
            _MORAST_DOCSTRING,
            nodes.DocString(self.docstring, level=ds_level),
        )


class MorastClassDef(MorastSection):
    """Represents a class.

    Initialization arguments:

    * _element_: the ast.ClassDef instance from which
      the class name, signature, docstring, attributes
      and methods are determined
    * ...
    * _level_: the level in the document hierarchy: `3`
    * _superconfig_: ...
    """

    kind = overrides.KIND_CLASS

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals

    def __init__(
        self,
        element: ast.ClassDef,
        namespace: str = "",
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        """Determine and store attributes"""
        name = element.name
        decorators: List[nodes.MorastBaseNode] = [
            nodes.get_node(single_dec) for single_dec in element.decorator_list
        ]
        class_prefix = "Class"
        self.is_a_dataclass = False
        for item in decorators:
            dec_str = str(item)
            if PRX_DATACLASS.match(dec_str):
                self.is_a_dataclass = True
                class_prefix = "Dataclass"
                if "(frozen=True)" in dec_str:
                    class_prefix = "Frozen dataclass"
                #
                break
            #
        #
        super().__init__(
            name,
            namespace=namespace,
            superconfig=superconfig,
            level=3,
            headline=f"{class_prefix} {name}()",
        )
        self.check_private()
        inheritance_prefix = self.sc.emoji.inheritance_prefix
        self._init_method: Optional[ast.FunctionDef] = None
        self.existing_attributes: Dict[str, Set[str]] = {
            SCOPE_CLASS: set(),
            SCOPE_INSTANCE: set(),
        }
        self.attribute_lists: Dict[str, MorastAttributesList] = {}
        self.methods: Dict[str, MorastSection] = {}
        for scope in (SCOPE_CLASS, SCOPE_INSTANCE):
            self.attribute_lists[scope] = MorastAttributesList(
                f"{scope} attributes",
                superconfig=superconfig,
                scope=scope,
            )
            self.methods[scope] = MorastSection(
                f"{scope} methods", superconfig=superconfig, level=self._level
            )
        #
        ds_level = 1
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr):
                if isinstance(sub_element.value, ast.Constant):
                    self.docstring = sub_element.value.value
                    ds_level = self._level
                    continue
                #
            elif isinstance(sub_element, (ast.Assign, ast.AnnAssign)):
                if self.is_a_dataclass:
                    self._add_instance_attribute(sub_element, check_self=False)
                    continue
                self._add_class_attribute(sub_element)
            elif isinstance(sub_element, ast.FunctionDef):
                self._add_method(sub_element)
            #
        #
        # TODO: handle inheritance
        bases: List[Any] = getattr(element, "bases", [])
        if bases:
            self.add_subnode(
                _MORAST_BASES,
                nodes.MorastClassBases(
                    *bases, prefix=f"{inheritance_prefix} "
                ),
            )
        #
        if isinstance(self._init_method, ast.FunctionDef):
            self._add_signature(self._init_method)
        #
        self.set_docstring_from_override()
        self.check_ignored()
        self.add_subnode(
            _MORAST_DOCSTRING,
            nodes.DocString(self.docstring, level=ds_level),
        )
        for scope in (SCOPE_CLASS, SCOPE_INSTANCE):
            if len(self.attribute_lists[scope]):
                self.add_subsection(subsection=self.attribute_lists[scope])
            #
        #
        for scope in (SCOPE_CLASS, SCOPE_INSTANCE):
            for method_name, method_sect in self.methods[scope].subsections():
                self.add_subsection(method_name, method_sect)
            #
        #

    def _add_method(self, element: ast.FunctionDef) -> None:
        """Add method"""
        method_name = str(element.name)
        if method_name == "__init__":
            self._init_method = element
            for init_statement in self._init_method.body:
                if isinstance(init_statement, (ast.Assign, ast.AnnAssign)):
                    self._add_instance_attribute(init_statement)
                #
            #
            return
        #
        try:
            method = MorastFunctionDef(
                element,
                namespace=self.namespaced_name,
                superconfig=self.sc,
                scope=SCOPE_CLASS,
            )
        except IgnoredItem as ignored:
            logging.info(ignored.message)
            return
        #
        self.methods[METHOD_TARGETS[method.function_type]].add_subsection(
            subsection=method
        )

    def _add_attribute(
        self,
        element: Union[ast.Assign, ast.AnnAssign],
        scope: str,
        check_self: bool = False,
    ) -> None:
        """Add an attribute

        _scope_ may be SCOPE_CLASS or SCOPE_INSTANCE
        """
        try:
            new_attribute = MorastAttribute(
                element,
                namespace=self.namespaced_name,
                superconfig=self.sc,
                scope=scope,
                check_self=check_self,
            )
        except IgnoredItem as ignored:
            logging.info(ignored.message)
            return
        #
        if new_attribute.name in self.existing_attributes[scope]:
            return
        #
        self.attribute_lists[scope].add(new_attribute)
        self.existing_attributes[scope].add(new_attribute.name)
        logging.debug(
            "%s: accepted %s attribute %r",
            self.namespaced_name,
            scope,
            new_attribute.name,
        )
        if (
            scope == SCOPE_INSTANCE
            and new_attribute.name in self.existing_attributes[SCOPE_CLASS]
        ):
            self.attribute_lists[SCOPE_CLASS].remove(new_attribute.name)
            self.existing_attributes[SCOPE_CLASS].remove(new_attribute.name)
        #

    def _add_class_attribute(
        self, element: Union[ast.Assign, ast.AnnAssign]
    ) -> None:
        """Add an instance attribute if it does not exist yet"""
        if self.is_a_dataclass:
            raise ValueError("this is a dataclass and has no class attributes")
        #
        self._add_attribute(element, SCOPE_CLASS)

    def _add_instance_attribute(
        self,
        element: Union[ast.Assign, ast.AnnAssign],
        check_self: bool = True,
    ) -> None:
        """Add an instance attribute if it does not exist yet"""
        self._add_attribute(element, SCOPE_INSTANCE, check_self=check_self)

    def _add_signature(
        self,
        init_method: ast.FunctionDef,
    ) -> None:
        """Add the signature"""
        self.add_subnode(
            _MORAST_SIGNATURE,
            nodes.Signature(
                self.name,
                init_method.args,
                returns=None,
                prefix=f"{self.sc.emoji.signature_prefix} {self.namespace}.",
                skip_first_arg=True,
            ),
        )


class MorastModule(MorastSection):
    """Represents a module in the document tree

    Initialization arguments:

    *   _module_: an ast.Module instance from which this instance is built
    *   _name_: the module name (public attribute, set in the ancestor class)
    *   _namespace_: the module namespace (only used in the headline)
    *   _superconfig_: a **SuperConfig** instance (passed through
        to the parent class)
    """

    kind = overrides.KIND_MODULE

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        module: ast.Module,
        name: str,
        namespace: str = "",
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        """Store the attributes and build a sequence of
        MorastSection instances:

        *   module contents
        *   module-level functions
        *   classes
        """
        namespace_prefix = f"{namespace}." if namespace else ""
        headline_prefix = superconfig.emoji.module_prefix or "Module"
        super().__init__(
            name,
            superconfig=superconfig,
            headline=f"{headline_prefix} {namespace_prefix}{name}",
        )
        self.module_contents = MorastAttributesList(
            "Module contents", superconfig=superconfig
        )
        self.classes = MorastSection(
            "Classes", namespace=name, superconfig=superconfig, level=2
        )
        self.functions = MorastSection(
            "Functions", namespace=name, superconfig=superconfig, level=2
        )
        for element in module.body:
            if isinstance(element, ast.Expr):
                if self.docstring:
                    continue
                #
                if isinstance(element.value, ast.Constant):
                    self.docstring = element.value.value
                    continue
                #
            else:
                try:
                    self._add_element(element)
                except TypeError as error:
                    logging.info(str(error))
                #
            #
        #
        self.set_docstring_from_override()
        self.add_subnode(_MORAST_DOCSTRING, nodes.DocString(self.docstring))
        for subsection in (self.module_contents, self.functions, self.classes):
            if len(subsection):
                self.add_subsection(subsection=subsection)
            #
        #
        if self.sc.advertise:
            self.add_subnode(
                _MORAST_ADVERTISEMENT,
                nodes.Advertisement(self.sc.emoji.advertisement_prefix),
            )
        #

    def _add_element(
        self,
        element: ast.AST,
    ) -> None:
        """Add _element_ to the body blocks if not ignored.

        Currently, ast assignment (ie. ast.Assign, ast.AnnAssign),
        ast.ClassDef and ast.FunctionDef instances are supported.
        """
        if isinstance(element, (ast.Assign, ast.AnnAssign)):
            try:
                module_constant = MorastAttribute(
                    element,
                    namespace=self.name,
                    scope=SCOPE_MODULE,
                    superconfig=self.sc,
                )
            except IgnoredItem as ignored:
                logging.info(ignored.message)
                return
            #
            self.module_contents.add(module_constant)
        elif isinstance(element, ast.ClassDef):
            try:
                class_sub = MorastClassDef(
                    element,
                    namespace=self.name,
                    superconfig=self.sc,
                )
            except IgnoredItem as ignored:
                logging.info(ignored.message)
                return
            #
            self.classes.add_subsection(subsection=class_sub)
        elif isinstance(element, ast.FunctionDef):
            try:
                func_sub = MorastFunctionDef(
                    element,
                    namespace=self.name,
                    scope=SCOPE_MODULE,
                    superconfig=self.sc,
                )
            except IgnoredItem as ignored:
                logging.info(ignored.message)
                return
            #
            self.functions.add_subsection(subsection=func_sub)
        else:
            raise TypeError(
                f"{ast.dump(element)} (line {element.lineno})"
                " not supported yet"
            )
        #

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Iterator over MarkDown elements,
        appending a verbatim section if defined in the overrides
        """
        yield from super().markdown_elements()
        try:
            # refs = self.module_overrides[f"{self.name}.{MORAST_REF}"]
            refs = self.sc.mor[_MORAST_VERBATIM]
        except KeyError:
            pass
        else:
            yield mde.BlockElement(mds.declare_as_safe(refs.docstring))
        #

    def render(self) -> str:
        """Generate MarkDown output from this instance"""
        return mde.render(*self.markdown_elements())

    def get_extracted_overrides(self) -> str:
        """Return extracted overrides for the extract subcommand"""
        overrides_list: List[str] = []
        for section in self.sc.get_nested_sections(self.name):
            overrides_list.extend((str(section).rstrip(), commons.EMPTY))
        #
        verbatim_section = self.sc.mor[_MORAST_VERBATIM]
        if verbatim_section:
            overrides_list.extend(
                (str(verbatim_section).rstrip(), commons.EMPTY)
            )
        #
        return commons.LF.join(overrides_list)

    @classmethod
    def from_file(
        cls,
        path: pathlib.Path,
        encoding: str = commons.UTF8,
        superconfig=DUMMY_SUPERCONFIG,
    ) -> "MorastModule":
        """**Factory method:**
        read the Python module at _path_,
        analyze it, and return a new MorastModule instance from the
        syntax tree returned by **ast.parse()**.

        The module name is simply derived from the file name,
        and in src-based paths, the namespace is determined automatically.

        Remaining arguments:

        *   _encoding_: source file encoding (defaults to `utf-8`)
        *   _superconfig_: a **SuperConfig** instance
            (passed through to the initialization method)
        """
        source = path.read_text(encoding=encoding)
        module_path_parts = path.parent.parts
        namespace = ""
        src_path = "src"
        if src_path in module_path_parts:
            namespace_root_pos = 0
            while src_path in module_path_parts[namespace_root_pos:]:
                namespace_root_pos = (
                    module_path_parts.index("src", namespace_root_pos) + 1
                )
            #
            namespace = ".".join(module_path_parts[namespace_root_pos:])
            logging.debug("Module namespace: %s", namespace)
        #
        module_file = path.name
        module_name = module_file.rsplit(".", 1)[0]
        return cls(
            ast.parse(source=source, filename=path.name),
            name=module_name,
            namespace=namespace,
            superconfig=superconfig,
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
