"""Copyright (c) 2024 Bendabir."""

from __future__ import annotations

import functools as ft
from typing import TYPE_CHECKING, Callable, final

from mypy.nodes import (
    CallExpr,
    Decorator,
    Expression,
    MemberExpr,
    NameExpr,
    StrExpr,
    TypeInfo,
)
from mypy.plugin import (
    ClassDefContext,
    FunctionContext,
    MethodContext,
    Plugin,
)
from mypy.types import DEPRECATED_TYPE_NAMES, Type
from typing_extensions import TypeGuard, override

from mypypp.errorcodes import DEPRECATED

if TYPE_CHECKING:
    from mypy.types import Type

# For MyPy cache
__version__ = 1


def plugin(_version: str) -> type[Plugin]:
    """Plugin injection point."""
    return DeprecatedPlugin


@final
class DeprecatedPlugin(Plugin):
    """Plugin that checks for deprecated code."""

    # It might be possible to use visitors instead, probably cleaner
    @staticmethod
    def _is_deprecated(decorator: Expression) -> TypeGuard[CallExpr]:
        if isinstance(decorator, CallExpr):
            return (
                isinstance(decorator.callee, NameExpr)
                and decorator.callee.fullname in DEPRECATED_TYPE_NAMES
            )

        return False

    @staticmethod
    def _resolve_deprecated_reason(call_expr: CallExpr) -> str | None:
        if not call_expr.args:
            return None

        reason = call_expr.args[0]

        if isinstance(reason, StrExpr):
            return reason.value

        return None

    @staticmethod
    def _resolve_nameexpr_name(name_expr: NameExpr) -> str:
        return name_expr.name

    @classmethod
    def _resolve_callexpr_name(cls, call_expr: CallExpr) -> str | None:
        if isinstance(call_expr.callee, NameExpr):
            return cls._resolve_nameexpr_name(call_expr.callee)

        if isinstance(call_expr.callee, MemberExpr):
            if isinstance(call_expr.callee.expr, NameExpr):
                root = cls._resolve_nameexpr_name(call_expr.callee.expr)
            elif isinstance(call_expr.callee.expr, CallExpr):
                root = cls._resolve_callexpr_name(call_expr.callee.expr) or ""
            else:
                root = ""

            return f"{root}.{call_expr.callee.name}".strip(".")

        return None

    @classmethod
    def _no_deprecated_function(cls, context: FunctionContext, *, reason: str) -> Type:
        if isinstance(context.context, CallExpr):
            name = cls._resolve_callexpr_name(context.context)

            context.api.fail(
                f'The function "{name}" is deprecated : {reason}',
                context.context,
                code=DEPRECATED,
            )

        return context.default_return_type

    @classmethod
    def _no_deprecated_class(cls, context: FunctionContext, *, reason: str) -> Type:
        if isinstance(context.context, CallExpr):
            name = cls._resolve_callexpr_name(context.context)

            context.api.fail(
                f'The class "{name}" is deprecated : {reason}',
                context.context,
                code=DEPRECATED,
            )

        return context.default_return_type

    @override
    def get_function_hook(
        self,
        fullname: str,
    ) -> Callable[[FunctionContext], Type] | None:
        sym = self.lookup_fully_qualified(fullname)

        if sym is None:
            return None

        if isinstance(sym.node, Decorator):
            for d in sym.node.decorators:
                if self._is_deprecated(d):
                    return ft.partial(
                        self._no_deprecated_function,
                        reason=self._resolve_deprecated_reason(d) or "Unknown reason",
                    )

        if isinstance(sym.node, TypeInfo):
            for info in sym.node.mro:
                if "deprecated" in info.metadata:
                    return ft.partial(
                        self._no_deprecated_class,
                        reason=info.metadata["deprecated"]["reason"],
                    )

        return None

    @classmethod
    def _no_deprecated_method(cls, context: MethodContext, *, reason: str) -> Type:
        if isinstance(context.context, CallExpr):
            name = cls._resolve_callexpr_name(context.context)

            context.api.fail(
                f'The method "{name}" is deprecated : {reason}',
                context.context,
                code=DEPRECATED,
            )

        return context.default_return_type

    @override
    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        sym = self.lookup_fully_qualified(fullname)

        if sym is None:
            return None

        if isinstance(sym.node, Decorator):
            for d in sym.node.decorators:
                if self._is_deprecated(d):
                    return ft.partial(
                        self._no_deprecated_method,
                        reason=self._resolve_deprecated_reason(d) or "Unknown reason",
                    )

        return None

    @classmethod
    def _mark_deprecated_class(cls, context: ClassDefContext) -> None:
        if cls._is_deprecated(context.reason):
            context.cls.info.metadata["deprecated"] = {
                "reason": (
                    cls._resolve_deprecated_reason(context.reason) or "Unknown reason"
                )
            }

    @override
    def get_class_decorator_hook(
        self,
        fullname: str,
    ) -> Callable[[ClassDefContext], None] | None:
        # The logic for classes is a bit difference
        if fullname in DEPRECATED_TYPE_NAMES:
            return self._mark_deprecated_class

        return None
