from datetime import datetime, timedelta

from timekeeper import slice
from timekeeper import log

DEFAULT_DB_PATH = ".timekeeper.db"

COL_WIDTH = 15

def print_splash():
    """
    Prints the splash text
    """
    splash = "Timekeeper 0.3.0\n"
    splash += "-" * 80 + "\n"
    splash += "    view    - views current_log\n"
    splash += "    save    - saves current_log\n"
    splash += "    load    - loads current_log\n"
    splash += "    new     - adds new slice\n"
    splash += "    report  - displays aggregates\n"
    splash += "    quit    - quits\n"
    splash += "    help    - displays help text\n"

    print(splash)

def new_prompt(current_log):
    """
    Prompts the user for slice information (start, end, category, description)
    """
    in_start = input("Start:       ")
    in_end = input("End:         ")
    in_category = input("Category:    ")
    in_description = input("Description: ")

    current_log.set_slice(slice.Slice(datetime.strptime(in_start,
                                                        current_log.DT_FMT),
                        datetime.strptime(in_end, current_log.DT_FMT),
                        in_category, in_description))

def save_prompt(current_log):
    """
    Prompts the user to confirm save operation then file path to database file
    """
    save_choice = input("Save? ")
    
    if save_choice == "Y":
        db_path = input("Enter filepath (" + DEFAULT_DB_PATH + "): ")

        if db_path == "":
            db_path = DEFAULT_DB_PATH
        
        current_log.save(db_path)

def load_prompt(current_log):
    """
    Prompts the user to confirm load operation then file path to database file
    """
    load_choice = input("Load (Y/N)? ")

    if load_choice == "Y":
        db_path = input("Enter filepath (" + DEFAULT_DB_PATH + "): ")

        if db_path == "":
            db_path = DEFAULT_DB_PATH

        current_log.load(db_path)

def help_text():
    """
    Displays the help text to the user
    """
    help_text = "Commands:\n"

    # view
    help_text += "view\n"
    help_text += "    Displays the current time log. Note that this could"
    help_text += " include slices that have\n"
    help_text += "    *not* been saved yet.\n\n"

    # save
    help_text += "save\n"
    help_text += "    Saves the current time log (viewable with `view` to the"
    help_text += " provided database\n"
    help_text += "    file.\n\n"

    # load
    help_text += "load\n"
    help_text += "    Loads a the time log from the provided database file."
    help_text += " Note that this will\n"
    help_text += "    clobber any unsaved slices in the"
    help_text += " current time log (even if they are the\n"
    help_text += "    same log).\n\n"

    # new
    help_text += "new\n"
    help_text += "    Creates a new slice with the provided information. Note"
    help_text += " that this does *not*\n"
    help_text += "    save the new slice to disk (use `save`"
    help_text += " for this).\n\n"

    # report
    help_text += "report\n"
    help_text += "    Prints an aggregate of time spent (in minutes) for each"
    help_text += " category in the log\n"
    help_text += "    *for the past week*.\n\n"

    # quit
    help_text += "quit\n"
    help_text += "    Exits the program. *All unsaved slices will be lost*.\n\n"

    # help
    help_text += "help\n"
    help_text += "    Displays this help text.\n\n"

    print(help_text)

def print_report(current_log):
    # calculate date offsets
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    report = current_log.ranged_category_aggregate(week_ago, now)

    s = "For " + str(week_ago) + " to " + str(now) + "\n"
    s += "Category        | Duration (min)  |\n"
    s += "----------------+-----------------+\n"

    for k, v in report.items():
        s += k + (COL_WIDTH - len(k) ) * " " + " | " + str(v) + (
            COL_WIDTH - len(str(v))) * " " + " |\n"

    print(s)

def main():
    current_log = log.Log([])
    print_splash()

    while True: # main shell loop
        cmd = input("> ")

        if cmd == "quit":
            exit()
        elif cmd == "help":
            help_text()
        elif cmd == "view":
            print(current_log)
        elif cmd == "save":
            save_prompt(current_log)
        elif cmd == "load":
            load_prompt(current_log)
        elif cmd == "new":
            new_prompt(current_log)
            print("-" * 80)
        elif cmd == "report":
            print_report(current_log)
            
if __name__ == "__main__":
    main()
