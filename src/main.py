from utils.arg_parser import MyArgumentParser
from utils.employee_data import EmployeeData

if __name__ == "__main__":
    arg_parser = MyArgumentParser()
    args = arg_parser.parse_args()

    ed = EmployeeData(args.files, output_dir=args.output)
    ed.report(args.report, args.format)
