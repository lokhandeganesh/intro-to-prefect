from typing import Literal

import pydantic
from prefect import flow, pause_flow_run
from prefect.input import RunInput


class ShirtOrder(RunInput):
    size: Literal["small", "medium", "large", "xlarge"]
    color: Literal["red", "green", "black"]

    @pydantic.validator("color")
    def validate_age(cls, value, values, **kwargs):
        if value == "green" and values["size"] == "small":
            raise ValueError("Green is only in-stock for medium, large, and XL sizes.")

        return value


@flow(log_prints=True)
def get_shirt_order():
    shirt_order = None

    while shirt_order is None:
        try:
            shirt_order = pause_flow_run(wait_for_input=ShirtOrder)
            print(f"Shirt order: {shirt_order}")
        except pydantic.ValidationError:
            print("Invalid shirt order. Please try again.")


if __name__ == "__main__":
    get_shirt_order()
