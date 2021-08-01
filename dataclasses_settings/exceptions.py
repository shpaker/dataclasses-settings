from typing import List, Tuple


class ValidationError(ValueError):
    def __init__(
        self,
        errors: List[Tuple[str, str, str]],
    ) -> None:
        errors_msg = list()
        for err in errors:
            errors_msg.append(
                f"arg \"{err[0]}\":\n"
                f"  value: {err[1]}\n"
                f"  error: {err[2]}\n"
            )
        super().__init__("\n"+"\n".join(errors_msg))
