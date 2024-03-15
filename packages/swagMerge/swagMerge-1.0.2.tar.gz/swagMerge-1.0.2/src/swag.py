import argparse
import yaml
import os

def combine_swagger_files(input_folder, output_file):
    print(f"Input Folder: {input_folder}")
    print(f"Output File: {output_file}")

    combined_swagger = {
        "openapi": "3.0.0",
        "info": {
            "title": "Combined API",
            "version": "1.0.0",
            "description": "Merged Swagger files",
            "license": {
                "name": "MIT",
                "url": "https://spdx.org/licenses/MIT.html"
            }
        },
        "servers": [],
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {},
            "responses": {}
        },
        "tags": []
    }

    # Variable to keep track if the first server is found
    first_server_found = False

    # Iterate through each YAML file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            file_path = os.path.join(input_folder, filename)

            # Load the content of the current YAML file
            with open(file_path, 'r') as file:
                current_swagger = yaml.safe_load(file)

            # Merge the content into the combined Swagger definition
            if not first_server_found and "servers" in current_swagger:
                combined_swagger["servers"].extend(current_swagger["servers"])
                first_server_found = True

            combined_swagger["paths"].update(current_swagger.get("paths", {}))

            # Merge components (schemas, securitySchemes, responses)
            for component_key in ["schemas", "securitySchemes", "responses"]:
                if component_key in current_swagger.get("components", {}):
                    combined_swagger["components"][component_key].update(current_swagger["components"][component_key])

            combined_swagger["tags"].extend(current_swagger.get("tags", []))

    # Save the combined Swagger definition to a new YAML file with specified order
    with open(output_file, 'w') as output_file:
        yaml.dump(
            combined_swagger,
            output_file,
            default_flow_style=False,
            explicit_start=True,  # Add '---' at the start of the document
            explicit_end=True  # Add '...' at the end of the document
        )

def main():
    parser = argparse.ArgumentParser(description="Combine Swagger files into a single YAML file.")
    parser.add_argument("input_folder", help="Path to the input folder containing Swagger files.")
    parser.add_argument("output_file", help="Path to the output combined Swagger YAML file.")
    args = parser.parse_args()

    combine_swagger_files(args.input_folder, args.output_file)

if __name__ == "__main__":
    main()
