from __future__ import annotations

import inspect
import typing as t
from gracy import Gracy, GracyReplay

from gpokeapi.clients.api import PokeApi
from gpokeapi.igracy import exceptions, models
from rich.prompt import Prompt

RESOLVER_MAP: t.Dict[t.Type, t.Callable[[], models.InputOption]] = {
    GracyReplay: lambda: models.ReplayInputOption(value=[])
}


def _import_custom_type(klass: t.Type[Gracy], name: str):
    module = __import__(klass.__module__, fromlist=[name])
    return getattr(module, name)


def _parse_type(param_type: t.Any, api_class: t.Type[Gracy]) -> models.InputOption:
    if isinstance(param_type, str):
        param_type = _import_custom_type(api_class, param_type)

    param_origin = getattr(param_type, "__origin__", None)

    if param_origin:
        if param_origin is t.Union:
            options = [_parse_type(arg, api_class) for arg in param_type.__args__]
            return models.DeeperInputOption(options)

        elif param_origin is t.Literal:
            options = list(param_type.__args__)
            return models.UserChoiceInputOption(options)

        raise NotImplementedError(param_origin)

    if inspect.isclass(param_type):
        if param_type in RESOLVER_MAP:
            return RESOLVER_MAP[param_type]()

    raise NotImplementedError(param_type)


def parse_parameter(param: inspect.Parameter, api_class: t.Type[Gracy]) -> models.UserInputParams:
    name = param.name
    default = param.default
    param_type = _parse_type(param.annotation, api_class)

    return models.UserInputParams(
        attr_name=name,
        selected_value=default,
        options=param_type,
    )


class APIClassManager:
    def get_input_params(self, api_class: t.Type[Gracy]) -> t.List[models.UserInputParams]:
        init_signature = inspect.signature(api_class.__init__)
        init_args = list(init_signature.parameters.values())[1:]  # Exclude 'self'

        results: t.List[models.UserInputParams] = []

        for param in init_args:
            arg_name = param.name
            arg_type = param.annotation

            if arg_type is inspect.Signature.empty:
                # No type annotation, can't resolve
                raise exceptions.AttrMissingSignature(arg_name)

            user_param = parse_parameter(param, api_class)
            results.append(user_param)

        return results


if __name__ == "__main__":
    inputs = APIClassManager().get_input_params(PokeApi)

    for user_input in inputs:
        x = user_input.options
        x = x.value[0]
        choices = x.value
        user_input.selected_value = Prompt.ask(
            f"Set a value for {user_input.attr_name}:", default=user_input.selected_value, choices=choices
        )
