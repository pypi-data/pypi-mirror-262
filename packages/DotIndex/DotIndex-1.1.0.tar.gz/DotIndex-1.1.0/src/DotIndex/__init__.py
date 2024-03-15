from typing import Union, Any

class DotIndex:
    def __init__(
        self,
        obj: dict,
        recursive: bool=True,
        verbose_logs: bool=False,
        ignore_errors: bool=False,
        recurse_lists: bool=True
    ) -> None:
        """Recreates dicts and lists as class objects, where keys are variables.
        Disclaimer: keys are ordered alphabetically, original order is not preserved. Along with that, keys can't start with '__'.

        - obj (`dict[str, Any]`) - The object to DotIndex-ify
        - recursive (`bool`) - Whether or not to dot index lists and dicts nested in the original object
        - verbose_logs (`bool`) - Whether or not to show more detailed logs
        - ignore_errors (`bool`) - Whether or not to ignore any non-critical TypeErrors
        - recurse_lists (`bool`) - Whether or not to recurse through lists. Ignored if `recursive` is False."""

        self.__settings__ = {
            "recursive": recursive,
            "verbose_logs": verbose_logs,
            "ignore_errors": ignore_errors
        }

        if verbose_logs:
            print(self.__settings__)

        def recur_lists(list_obj: list[Any]) -> list:
            output = []

            for i in list_obj:
                if isinstance(i, dict):
                    output.append(DotIndex(i, verbose_logs=verbose_logs, ignore_errors=ignore_errors))
                elif isinstance(i, list):
                    output.append(recur_lists(i))
                else:
                    output.append(i)

            return output

        if isinstance(obj, dict):
            for i in obj:
                if not isinstance(i, str):
                    if not ignore_errors:
                        raise TypeError(f"'obj' key '{i}' should be type str, not {type(i)}")
                    if verbose_logs:
                        print(f"'obj' key '{i}' should be type str, not {type(i)}")
                    continue

                if i[:2:] == "__":
                    if not ignore_errors:
                        raise NameError(f"Variable '{i}' cannot be created as it starts with '__'")
                    if verbose_logs:
                        print(f"Variable '{i}' cannot be created as it starts with '__'")
                    continue

                if recursive and recurse_lists and isinstance(obj[i], list):
                    obj[i] = recur_lists(obj[i])

                elif recursive and isinstance(obj[i], dict):
                    obj[i] = DotIndex(obj[i], verbose_logs=verbose_logs, ignore_errors=ignore_errors, recurse_lists=recurse_lists)

                setattr(self, i, obj[i])

                try:
                    getattr(self, i)
                except:
                    if verbose_logs:
                        print(f"Unable to set variable {i} to {obj[i]}")

        else:
            if not ignore_errors:
                raise TypeError(f"'obj' should be type dict, not {type(obj)}")
            if verbose_logs:
                print(f"'obj' should be type dict, not {type(obj)}")

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f".{{{', '.join([f''''{i}': {repr(self[i])}''' for i in self])}}}"

    def __int__(self) -> int:
        return len(self)

    def __float__(self) -> float:
        return float(len(self))

    def __iter__(self) -> iter:
        return iter([attr for attr in dir(self) if not attr.startswith("__")])

    def __call__(self, item: str) -> Any:
        return getattr(self, item)

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def __setitem__(self, item: str, value: Any) -> None:
        def recurse_lists(list_obj: list[Any]) -> list:
            output = []

            for i in list_obj:
                if isinstance(i, dict):
                    output.append(DotIndex(i))
                elif isinstance(i, list):
                    output.append(recurse_lists(i))
                else:
                    output.append(i)

            return output

        if self.__settings__["recursive"] and isinstance(value, list):
            setattr(self, item, recurse_lists(value))

        elif self.__settings__["recursive"] and isinstance(value, dict):
            setattr(self, item, DotIndex(value))

        else:
            setattr(self, item, value)
            return

    def __delitem__(self, item: str) -> None:
        delattr(self, item)

    def __len__(self) -> int:
        return len([attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")])

    def __contains__(self, item) -> bool:
        return item in list(iter(self))

    def __pos__(self) -> int:
        return len(self)

    def __neg__(self) -> int:
        return -len(self)

    def __bool__(self) -> bool:
        return len(self) != 0

    def __add__(self, other: Union['DotIndex', dict]) -> 'DotIndex':
        if type(other) != type(self) and not isinstance(other, dict):
            return NotImplemented

        new = {}

        for i in self:
            new[i] = self[i]

        for i in other:
            new[i] = other[i]

        return DotIndex(
            new,
            recursive=self.__settings__["recursive"],
            verbose_logs=self.__settings__["verbose_logs"],
            ignore_errors=self.__settings__["ignore_errors"]
        )

    def __radd__(self, other: Union['DotIndex', dict]) -> 'DotIndex':
        if type(other) != type(self) and not isinstance(other, dict):
            raise TypeError(f"Can't add types {type(other)} and DotIndex")

        new = {}

        for i in other:
            new[i] = other[i]

        for i in self:
            new[i] = self[i]

        return DotIndex(
            new,
            recursive=self.__settings__["recursive"],
            verbose_logs=self.__settings__["verbose_logs"],
            ignore_errors=self.__settings__["ignore_errors"]
        )

    def __iadd__(self, other: Union['DotIndex', dict]) -> 'DotIndex':
        return self + other

    def __lt__(self, other: Union['DotIndex', dict]) -> bool:
        if type(other) != type(self) and not isinstance(other, dict):
            return NotImplemented

        return len(self) < len(other)

    def __gt__(self, other: Union['DotIndex', dict]) -> bool:
        if type(other) != type(self) and not isinstance(other, dict):
            return NotImplemented

        return len(self) > len(other)

    def __le__(self, other: Union['DotIndex', dict]) -> bool:
        if type(other) != type(self) and not isinstance(other, dict):
            return NotImplemented

        return len(self) <= len(other)

    def __ge__(self, other: Union['DotIndex', dict]) -> bool:
        if type(other) != type(self) and not isinstance(other, dict):
            return NotImplemented

        return len(self) >= len(other)

    def __eq__(self, other: Union['DotIndex', dict]) -> bool:
        def recurse_lists(list_a: list[Any], list_b: list[Any]) -> bool:
            if len(list_a) != len(list_b):
                return False

            for i in range(len(list_a)):
                if isinstance(list_a[i], list) and isinstance(list_b[i], list):
                    if not recurse_lists(list_a[i], list_b[i]):
                        return False
                else:
                    if list_a[i] != list_b[i]:
                        return False

            return True

        if not isinstance(other, dict) and type(other) != type(self):
            return False

        if len(other) != len(self):
            return False

        for i in self:
            if i not in other:
                return False

            if isinstance(self[i], list) and isinstance(other[i], list):
                if not recurse_lists(self[i], other[i]):
                    return False

            else:
                if self[i] != other[i]:
                    return False

        return True

    def __ne__(self, other: Union['DotIndex', dict]) -> bool:
        return not self == other
