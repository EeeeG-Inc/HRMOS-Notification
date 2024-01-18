# left, right \d{1,3}:\d{2}$\ を想定.
def sub_hours(left:str, right: str) -> str:
    left_minutes = __get_minutes(left)
    right_minutes = __get_minutes(right)
    diff_minutes = abs(left_minutes - right_minutes)

    return __format(diff_minutes, left_minutes < right_minutes)

def __get_minutes(hours: str) -> int:
	hours, minutes = map(int, hours.split(':'))

	return hours * 60 + minutes

def __format(minutes: int, is_negative: bool) -> str:
    filled_minutes = str(minutes % 60).zfill(2)
    hours_str = f'{minutes // 60}:{filled_minutes}'

    return f'-{hours_str}' if is_negative else hours_str