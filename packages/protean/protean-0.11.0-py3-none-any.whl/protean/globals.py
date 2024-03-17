from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from protean import Domain, UnitOfWork

from functools import partial

from werkzeug.local import LocalProxy, LocalStack

_domain_ctx_err_msg = """\
Working outside of domain context.
This typically means that you attempted to use functionality that needed
to interface with the current domain object in some way. To solve
this, set up an domain context with domain.domain_context().  See the
documentation for more information.\
"""


def _lookup_domain_object(name) -> Any:
    top = _domain_context_stack.top
    if top is None:
        raise RuntimeError(_domain_ctx_err_msg)
    return getattr(top, name)


def _find_domain() -> Domain:
    top = _domain_context_stack.top
    if top is None:
        raise RuntimeError(_domain_ctx_err_msg)
    return top.domain


def _find_uow() -> UnitOfWork:
    return _uow_context_stack.top


# context locals
_domain_context_stack = LocalStack()
_uow_context_stack = LocalStack()
current_domain: Domain = LocalProxy(_find_domain)  # type: ignore  # noqa: F821
current_uow: UnitOfWork = LocalProxy(_find_uow)  # type: ignore  # noqa: F821
g = LocalProxy(partial(_lookup_domain_object, "g"))  # type: ignore
