import os


TOTAL = 0


def get_lines(folder, exclude):
    result = 0
    base = os.listdir(folder)
    # print(folder, base)
    for b in base:
        if b in exclude:
            continue
        # print(b)
        if os.path.isdir(os.path.join(folder, b)):
            result += get_lines(os.path.join(folder, b), exclude)
        else:
            # open and find amount of lines
            if b.endswith(".py"):
                print(os.path.join(folder, b))
                with open(os.path.join(folder, b), 'r') as file:
                    size = len(file.read().split("\n"))
                    file.close()
                result += size
    return result


folder = os.getcwd()
exclude = set(["venv","__pycache__", ".gitignore","README.md", "flex.py", "assets", ".git"])
print(get_lines(folder, exclude))