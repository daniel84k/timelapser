def format_shutter_value(seconds):
    if seconds >= 1.0:
        return f"{round(seconds, 1)}s"
    else:
        denominator = round(1.0 / seconds)
        return f"1/{denominator}s"

def print_max_exposures(rule):
    print("Max shutter times for each lens with rule", rule)
    for focal in [24, 35, 135]:
        print(f" - {focal}mm: {rule / focal:.2f} s")

