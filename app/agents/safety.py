WRITE_TOOLS = {
    "create_ticket",
}


def requires_confirmation(tool_name: str) -> bool:
    return tool_name in WRITE_TOOLS