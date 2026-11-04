from fishing_conditions import cli, gui

choice = input("1. Command-Line Interface\n2. Graphical Interface\n>>> ")
while choice not in ["1", "2"]:
    choice = input("\nInvalid input. Please enter either '1' or '2':\n>>> ")

if choice == "1":
    cli.run_cli()
elif choice == "2":
    gui.run_gui()
