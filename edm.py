#! /usr/bin/python3
import argparse


def float_range(start, stop, step):
    # Forces at least one value to be returned
    yield start

    if step > 0:
        while start < stop:
            start += step
            yield start
    else:
        while start > stop:
            start += step
            yield start


def plunge(depth, flutter_depth, flutter_cycles, feed, retract_height):
    plunge_code = []

    for increment in float_range(0, -depth, -feed):
        # Plunge the tool into the work
        plunge_code.append(f"G0 Z{increment-retract_height:.2f}\n")

        # Generate the code for the flutter cycle. Each flutter cycle the tool is
        # lifted by the fluter distance then plunged by the same amount.
        for _ in range(flutter_cycles * 2):
            plunge_code.append(f"G0 Z{flutter_depth}\n")
            flutter_depth *= -1

        # Retract the tool after the flutter cycles to allow flushing
        plunge_code.append(f"G0 Z{-increment+retract_height:.2f}\n")

    return plunge_code


def main():
    # Commandline argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("depth", help="The plunge depth", type=int)
    parser.add_argument(
        "--flutter-depth",
        help="Amount the tool will flutter up and down when at depth",
        type=float,
        default=0.1,
    )
    parser.add_argument(
        "--flutter-cycles",
        help="The number of cycles the tool will flutter",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--feed",
        help="Amount to advance the tool per plunge. Minimum feed is 0.01mm, max feed resolution is 0.01mm",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--retract-height",
        help="The distance the tool will be retracted above the workpiece for flushing",
        type=int,
        default=10,
    )
    args = parser.parse_args()

    # Gcode starting script
    header = f"""G28 ; Home all axis
    M25 ; Pause to for manual positioning of tool over workpiece
    G91 ; Set relative positioning
    G0 Z{args.retract_height} ; List tool to the safe retract height\n"""

    body = plunge(**vars(args))

    # Write the generated gocde to the output file
    with open("output.gcode", "w+") as out_file:
        out_file.write(header)
        out_file.writelines(body)


if __name__ == "__main__":
    main()