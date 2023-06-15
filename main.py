from argparse import ArgumentParser

from src.ClientGenerator import ClientGenerator

def parse_args():
    parser = ArgumentParser(prog="OpenAPI Client Generator", description="Generates a lightweight human-readable SDK from an OpeanAPI json file")
    parser.add_argument("-f", "--file", default="inputs/blockchainapis.json", help="The path to the file that you are willing to create the client from")
    parser.add_argument("-c", "--config", default="inputs/config.yml", help="The YAML configuration file that contains the config for the run")
    parser.add_argument("-a", "--additional", default="inputs/additional", help="The path to the folder containing the additional code to append")
    parser.add_argument("-d", "--dest", default="dest", help="The path to the folder to which you want the client to be generated (must not exist or be empty)")
    return parser.parse_args()

def main():
    args = parse_args()
    runner = ClientGenerator(args)
    runner.create_client()

if __name__ == "__main__":
    main()
