from wrapper import BinWrapper


class Helm(BinWrapper):
    __command_aliases = {
        "hist": "history",
        "ls": "list"
    }

    def __init__(self, **kwargs):
        super().__init__("helm", **kwargs)

    def __getattr__(self, item):
        h = Helm(**self._parent_kwargs)
        h._parent_attrs = self._parent_attrs.copy()
        h._parent_attrs.append(item)

        return h

    def _pre(self, args, parent_kwargs, kwargs) -> tuple:
        command = self._parent_attrs[0]
        if command in self.__command_aliases:
            command = self._parent_attrs[0] = self.__command_aliases[command]

        if "n" in parent_kwargs:
            parent_kwargs["namespace"] = parent_kwargs.pop("n", None)

        if command in ["history", "install", "list", "status", "upgrade"] or \
                ".".join(self._parent_attrs) in ["repo.list", "search.hub", "search.repo", "get.values"]:
            out_short = parent_kwargs.pop("o", "json")
            out_long = parent_kwargs.pop("output", out_short)
            out_short = kwargs.pop("o", out_long)
            kwargs.setdefault("output", out_short)

        if command == "list":
            kwargs.setdefault("time_format", "2006-01-02 15:04:05Z0700")

        args = list(args)
        for arg_name in ["values", "set", "set_file", "set_string", "show_only"]:
            v = kwargs.pop(arg_name, None)
            if v:
                arg_name.replace("_", "-")
                args.extend(f"--{arg_name}={v}" for v in v)

        return tuple(args)
