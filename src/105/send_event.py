from prefect.events import emit_event


def emit_name_event(name: str = "ganesh"):
    """Emit a basic Prefect event with a dynamically populated name"""
    print(f"Hi {name}!")
    emit_event(
        event=f"{name}.sent.event!",
        resource={"prefect.resource.id": f"developer.{name}"},
        payload={"name": name},
    )


if __name__ == "__main__":
    emit_name_event()
