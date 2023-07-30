try:
    import lxml.etree as ET
except:
    import subprocess

    subprocess.run(["pip", "install", "lxml"])
    import lxml.etree as ET

import csv
import sys
import pathlib

# Get the command line arguments
xml_path = sys.argv[1]
csv_path = sys.argv[2]

def generate_bom(xml_path, csv_path):
        # Load the EESCHEMA XML Partlist Format file
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Define the namespace for the XML file
        ns = {"xsl": "http://www.w3.org/1999/XSL/Transform"}
        
        # Load the XSL stylesheet to transform the XML file to CSV
        #xslt_tree = ET.parse("D:/git_repos/imu-geolocator-hw/scripts/bom2grouped_csv_jlcpcb.xsl")
        xslt_tree = ET.parse(f"{pathlib.Path().resolve()}/scripts/bom2grouped_csv_jlcpcb.xsl")
        transform = ET.XSLT(xslt_tree)
        
        # Apply the transformation to the XML file
        csv_data = transform(root)
        
        # Convert the XSLTResultTree object to a string and split into lines
        csv_data_str = str(csv_data)
        csv_lines = csv_data_str.splitlines()
        
        # Write the transformed CSV data to file
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar="'", quoting=csv.QUOTE_NONE)
            for line in csv_lines:
                writer.writerow(line.split(","))

# Example usage
generate_bom(xml_path, csv_path)