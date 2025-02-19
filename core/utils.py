def convert_kobo_to_naira(kobo_value: int):
    return kobo_value // 100


def convert_naira_to_kobo(naira_value: float):
    return int(naira_value * 100)
