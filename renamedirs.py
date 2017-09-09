import os
import sys

if __name__ == '__main__':
    for main_dir in sys.argv[1:]:
        for root, dirs, files in os.walk(main_dir):
            for dir in dirs:
                if 'Lichess4545 League - ' in dir:
                    new_name = dir.replace('Lichess4545 League - ', '')
                    command = 'mv "{}" "{}"'.format(os.path.join(root, dir), os.path.join(root, new_name))
                    print command
                    os.system(command)

    for main_dir in sys.argv[1:]:
        for root, dirs, files in os.walk(main_dir):
            for dir in dirs:
                if 'Lichess4545 - ' in dir:
                    new_name = dir.replace('Lichess4545 - ', '')
                    command = 'mv "{}" "{}"'.format(os.path.join(root, dir), os.path.join(root, new_name))
                    print command
                    os.system(command)



    for main_dir in sys.argv[1:]:
        for root, dirs, files in os.walk(main_dir):
            for dir in dirs:
                new_name = dir.replace(" ", "-").lower()
                if new_name != dir:
                    command = 'mv "{}" "{}"'.format(os.path.join(root, dir), os.path.join(root, new_name))
                    print command
                    os.system(command)
            for file in files:
                new_name = file.replace(" ", "-").lower()
                if new_name != file:
                    command = 'mv "{}" "{}"'.format(os.path.join(root, file), os.path.join(root, new_name))
                    print command
                    os.system(command)
