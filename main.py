import LurePicker
import CLI
import subprocess as sub

choice = input("1. Fishing Conditions Check\n2. Lure Helper\n>>> ")
while choice not in ["1", "2"]:
    choice = input("\nInvalid input. Please enter either '1' or '2':\n>>> ")
if choice == "1":
    sub.run(["python", "CLI.py"])
elif choice == "2":
    sub.run(["python", "LurePicker.py"])
