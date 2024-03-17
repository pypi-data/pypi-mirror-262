# -*- coding: utf-8 -*-

"""

tests.test_core

Unit test the core module


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

from typing import Iterator
from unittest import TestCase

from smdg import elements as mde
from smdg import strings as mds

from morast import core
from morast import overrides


# from morast import nodes


EXPECTED_MBN_REPR = "<MorastBaseNode instance>"

PAPERCLIP_EMOJI = "\N{PAPERCLIP}"
CONSTRUCTION_SIGN_EMOJI = "\N{CONSTRUCTION SIGN}"

EMPTY = ""
LF = "\n"
EXAMPLE_MOD_NAME = "mod_name"
EXAMPLE_MOD_NAMESPACE = f"example_namespace.{EXAMPLE_MOD_NAME}"
C1 = "const_1"
C2 = "const_2"
C3 = "const_3"
C4 = "_private_const_3"

C1_DOC = f"documentation of {C1}"
C3_DOC = f"documentation of {C3}"

EXAMPLE_MOD_OVERRIDE = f"""# {EXAMPLE_MOD_NAME}

## {C1}

{C1_DOC}

## {C2} – ignore

## {C3} (strip-value)

{C3_DOC}
"""

EXAMPLE_SUPERCONFIG = core.SuperConfig(
    module_overrides=overrides.ModuleOverrides.from_string(
        EXAMPLE_MOD_NAME,
        EXAMPLE_MOD_OVERRIDE,
        EXAMPLE_MOD_NAMESPACE,
    )
)

EXAMPLE_ASSIGNMENT_1 = f"{C1}: str = 'abcd'"
EXAMPLE_ASSIGNMENT_3 = f"{C3}: List[str] = [{EXAMPLE_MOD_NAME}.{C2}]"


SIMPLE_DATACLASS = '''
@dataclasses.dataclass
class DataStorage:
    """class docstring"""

    number: int
    flag: bool = False
    identifier: str = "dummy"
'''

FROZEN_DATACLASS = '''
@dataclasses.dataclass(frozen=True)
class EmojiConfiguration:
    """Configuration of emoji for …"""

    enabled: bool = True
'''


def parsed_body(source: str) -> Iterator[ast.AST]:
    """Return the body od a parsed module"""
    parsed_module = ast.parse(source)
    for item in parsed_module.body:
        if isinstance(item, ast.AST):
            yield item
        #
    #


class Functions(TestCase):
    """Module-level functions"""


class MorastDocumentableItem(TestCase):
    """MorastDocumentableItem class"""

    maxDiff = None

    def test_docstring(self) -> None:
        """initialization and docstring of a simple item"""
        item = core.MorastDocumentableItem(
            C1,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        item.set_docstring_from_override()
        self.assertEqual(item.docstring, C1_DOC)

    def test_ignored(self) -> None:
        """.is_ignored property and .check_ignored()"""
        for name, ignored in ((C1, False), (C2, True)):
            item = core.MorastDocumentableItem(
                name,
                namespace=EXAMPLE_MOD_NAME,
                superconfig=EXAMPLE_SUPERCONFIG,
            )
            item.set_docstring_from_override()
            with self.subTest(name, ignored=ignored):
                self.assertEqual(item.is_ignored, ignored)
            #
            with self.subTest(f"{name} raises exception"):
                if ignored:
                    self.assertRaisesRegex(
                        core.IgnoredItem,
                        f"\\A{EXAMPLE_MOD_NAME}: ignored {name!r} as specified"
                        " through override",
                        item.check_ignored,
                    )
                else:
                    self.assertFalse(item.check_ignored())
                #
            #
        #

    def test_check_private(self) -> None:
        """.check_private() method"""
        item = core.MorastDocumentableItem(
            C4,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        self.assertRaisesRegex(
            core.IgnoredItem,
            f"\\A{EXAMPLE_MOD_NAME}: ignored private member {C4!r}",
            item.check_private,
        )

    def test_markdown_elements(self) -> None:
        """.markdown_elements() method"""
        item = core.MorastDocumentableItem(
            C1,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        item.set_docstring_from_override()
        self.assertEqual(
            list(item.markdown_elements()),
            [
                mde.Paragraph(f"{EXAMPLE_MOD_NAME}.{C1}"),
                mde.BlockQuote(mds.SafeString(C1_DOC)),
            ],
        )


class MorastAttribute(TestCase):
    """MorastAttribute class"""

    maxDiff = None

    def test_simple_docstring(self) -> None:
        """initialization and docstring of a simple item"""
        element = list(parsed_body(EXAMPLE_ASSIGNMENT_1))[0]
        if not isinstance(element, (ast.AnnAssign, ast.AugAssign, ast.Assign)):
            self.skipTest("wrong type")
            return
        #
        item = core.MorastAttribute(
            element,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        self.assertEqual(item.docstring, C1_DOC)

    def test_stripped_value_as_markdown(self) -> None:
        """docstring of a simple item"""
        element = list(parsed_body(EXAMPLE_ASSIGNMENT_3))[0]
        if not isinstance(element, (ast.AnnAssign, ast.AugAssign, ast.Assign)):
            self.skipTest("wrong type")
            return
        #
        item = core.MorastAttribute(
            element,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        self.assertEqual(
            list(item.markdown_elements()),
            [
                mde.Paragraph(
                    mde.CompoundInlineElement(
                        mde.InlineElement(
                            f"{EXAMPLE_SUPERCONFIG.emoji.constants_prefix}"
                            f" {EXAMPLE_MOD_NAME}."
                        ),
                        mde.BoldText(mde.InlineElement(C3)),
                        mde.InlineElement(": "),
                        mde.CompoundInlineElement(
                            mde.InlineElement("List"),
                            mde.InlineElement("["),
                            mde.InlineElement("str"),
                            mde.InlineElement("]"),
                        ),
                    ),
                ),
                mde.BlockQuote(mds.SafeString(C3_DOC)),
            ],
        )


class MorastClassDef(TestCase):
    """MorastClassDef class"""

    maxDiff = None

    def rest_simple_dataclass(self) -> None:
        """test initialization of a simple data class"""
        ast_class_def = list(parsed_body(SIMPLE_DATACLASS))[0]
        if isinstance(ast_class_def, ast.ClassDef):
            class_def = core.MorastClassDef(ast_class_def)
        else:
            raise ValueError("Excpected a class definition")
        #
        with self.subTest("name"):
            self.assertEqual(class_def.name, "DataStorage")
        #
        with self.subTest("is a dataclass"):
            self.assertTrue(class_def.is_a_dataclass)
        #
        # =============================================================================
        #         for item in ("number", "flag", "identifier"):
        #             with self.subTest("instance_attribute", item=item):
        #                 current_node = class_def.instance_attrs[item]
        #                 if isinstance(current_node, nodes.Assignment):
        #                     self.assertEqual(
        #                         str(nodes.MorastName(item)),
        #                         str(current_node.target),
        #                     )
        #                 else:
        #                     raise ValueError("expected an Assignment")
        #                 #
        #             #
        # =============================================================================
        #
        with self.subTest("MarkDown elements"):
            self.assertEqual(
                list(class_def.markdown_elements()),
                [
                    mde.HorizontalRule(20),
                    mde.Header(3, "Dataclass DataStorage()"),
                    mde.BlockQuote(mds.sanitize("class docstring")),
                    mde.HorizontalRule(20),
                    mde.Header(4, "instance attributes"),
                    mde.CompoundInlineElement(
                        mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                        mde.BoldText(mde.InlineElement("number")),
                        mde.InlineElement(": "),
                        mde.InlineElement("int"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize(
                            f"{CONSTRUCTION_SIGN_EMOJI}"
                            " write number documentation"
                        )
                    ),
                    mde.CompoundInlineElement(
                        mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                        mde.BoldText(mde.InlineElement("flag")),
                        mde.InlineElement(": "),
                        mde.InlineElement("bool"),
                        mde.InlineElement(" = "),
                        mde.CodeSpan("False"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize(
                            f"{CONSTRUCTION_SIGN_EMOJI}"
                            " write flag documentation"
                        )
                    ),
                    mde.CompoundInlineElement(
                        mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                        mde.BoldText(mde.InlineElement("identifier")),
                        mde.InlineElement(": "),
                        mde.InlineElement("str"),
                        mde.InlineElement(" = "),
                        mde.CodeSpan("'dummy'"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize(
                            f"{CONSTRUCTION_SIGN_EMOJI}"
                            " write identifier documentation"
                        )
                    ),
                ],
            )

    def rest_frozen_dataclass(self) -> None:
        """test initialization of a frozen data class"""
        ast_class_def = list(parsed_body(FROZEN_DATACLASS))[0]
        if isinstance(ast_class_def, ast.ClassDef):
            class_def = core.MorastClassDef(ast_class_def)
        else:
            raise ValueError("Excpected a class definition")
        #
        with self.subTest("name"):
            self.assertEqual(class_def.name, "EmojiConfiguration")
        #
        with self.subTest("is a dataclass"):
            self.assertTrue(class_def.is_a_dataclass)
        #
        # =============================================================================
        #         item = "enabled"
        #         with self.subTest("instance_attribute", item=item):
        #             current_node = class_def.instance_attrs[item]
        #             if isinstance(current_node, nodes.Assignment):
        #                 self.assertEqual(
        #                     str(nodes.MorastName(item)),
        #                     str(current_node.target),
        #                 )
        #             else:
        #                 raise ValueError("expected an Assignment")
        #             #
        #         #
        # =============================================================================
        #
        with self.subTest("MarkDown elements"):
            self.assertEqual(
                list(class_def.markdown_elements()),
                [
                    mde.HorizontalRule(20),
                    mde.Header(3, "Frozen dataclass EmojiConfiguration()"),
                    mde.BlockQuote(
                        mds.sanitize("Configuration of emoji for …")
                    ),
                    mde.HorizontalRule(20),
                    mde.Header(4, "instance attributes"),
                    mde.CompoundInlineElement(
                        mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                        mde.BoldText(mde.InlineElement("enabled")),
                        mde.InlineElement(": "),
                        mde.InlineElement("bool"),
                        mde.InlineElement(" = "),
                        mde.CodeSpan("True"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize(
                            f"{CONSTRUCTION_SIGN_EMOJI}"
                            " write enabled documentation"
                        )
                    ),
                ],
            )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
