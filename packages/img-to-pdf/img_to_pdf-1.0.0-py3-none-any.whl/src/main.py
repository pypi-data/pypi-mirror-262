import sys
from src.cli import map_flags, generate_help_message, help_map, operation_map


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Please provide an operation:\nimg: merge images to PDF\npdf: merge PDFs together\nhelp: show details about the operations")
        sys.exit(1)
    
    if args[0] == "help":
        if len(args) < 2:
            print(generate_help_message())
        else:
            flag = args[1]
            if flag in help_map:
                print(f"{flag}: {help_map[flag]}")
            else:
                print(f"Flag {flag} not found. Please use 'help' to see the available flags.")
        sys.exit(0)

    if len(args) < 1:
        if args[0] not in operation_map:
            print("Incorrect operation. Please use 'help' to see the available operations.")
            sys.exit(1)
        operation = operation_map[args[0]]
        operation()
    
    operation = operation_map[args[0]]
    flags = map_flags(args)
    indir = flags.get("-in") if flags.get("-in") else flags.get("--input", "./")
    outdir = flags.get("-out") if flags.get("-out") else flags.get("--output", "./")
    if flags.get("-name"):
        output_filename = flags.get("-name")
        output_filename = output_filename if output_filename.endswith(".pdf") else output_filename + ".pdf"
        operation(indir, outdir, output_filename)
    else:
        operation(indir, outdir)
    
if __name__ == "__main__":
    main()
    