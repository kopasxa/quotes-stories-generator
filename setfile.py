import os

path = 'stories/'
dirs = os.listdir(path)

with open("list_of_stories.txt", "w") as f:
    for d in dirs:
        f.write(f"https://womenosophy.com/qstories/{d}\n")