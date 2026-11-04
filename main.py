import CLI
import GUI

choice = input("1. Command-Line Interface\n2. Graphical Interface\n>>> ")
while choice not in ["1", "2"]:
    choice = input("\nInvalid input. Please enter either '1' or '2':\n>>> ")

if choice == "1":
    CLI.run_cli()
elif choice == "2":
    GUI.run_gui()
