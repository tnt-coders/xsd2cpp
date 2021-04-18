import argparse
import os
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree

#TODO: Top level class should be named "File"

def main(argv):

    # Validator for input argument
    def cpp_class_name(arg):
        pattern = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")
        if not pattern.match(arg):
            raise argparse.ArgumentTypeError("Value must match '^[A-Za-z][A-Za-z0-9]*$'")
        return arg;

    # Parse input arguments
    parser = argparse.ArgumentParser(
        description="Converts XML schema files (.xsd) into C++ classes")
    parser.add_argument("schema",
        help="XML schema file (.xsd) to convert into C++ classes")
    args = parser.parse_args()

    # Verify the schema file exists
    schema_file = pathlib.Path(args.schema)
    if not schema_file.exists():
        print("File not found '" + str(schema_file) + "'")
        sys.exit()

    # Parse the XML schema
    parse_xml_schema(schema_file)

def parse_xml_schema(schema_file):
    print("Processing " + str(schema_file) + "...")

    # Extract the namespaces from the XML document
    ns = dict(
        node for _, node in xml.etree.ElementTree.iterparse(schema_file, events=["start-ns"])
    )

    print(ns)
    exit()

    # Get the root node
    tree = xml.etree.ElementTree.parse(schema_file)
    root_node = tree.getroot()

    import_nodes = root_node.findall("xs:import", ns)
    for import_node in import_nodes:
        process_import_node(import_node)

    documentation_nodes = root_node.findall("xs:annotation/xs:documentation", ns)
    #for documentation_node in documentation_nodes:
    #    print(documentation_node.text)

def process_import_node(import_node):

    schema_location = import_node.get("schemaLocation")
    schema_filename = schema_location.rsplit("/", 1).pop()
    cache_dir = pathlib.Path("cache")
    cache_dir.mkdir(exist_ok=True)
    schema_file = cache_dir.joinpath(schema_filename)

    # If the import is not in the cache, download it
    if not schema_file.exists():
        print("Retrieving " + schema_location + "...")
        urllib.request.urlretrieve(schema_location, schema_file)

    #TODO: parse imported files and load them into the correct namespaces
    #os.system(sys.argv[0])

if __name__ == "__main__":
    main(sys.argv[1:])

# exit()
# print(root.attrib)

# n = root.get('xs')
# print(n)

# ns = {'xs' : 'http://www.w3.org/2001/XMLSchema'}
# elements = root.findall('xs:element', ns)

# print(elements)