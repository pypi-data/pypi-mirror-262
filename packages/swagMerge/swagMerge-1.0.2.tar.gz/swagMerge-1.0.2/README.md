# Script Overview 
## Script Functionality 

The script iterates through each YAML file in the specified input folder, combines their contents into a single Swagger definition, and saves it to the specified output file.

# Combined Swagger Structure
## The combined Swagger definition includes:

- openapi: Version of the OpenAPI specification used (currently set to 3.0.0).
- info: Information about the combined API.
- servers: Server details.
- paths: Endpoint paths and their operations.
- components: Definitions of reusable components such as schemas, security schemes, and responses.
- tags: Grouping of operations by tags.
## How the Script Works
- Argument Parsing:
The script accepts two command-line arguments: input_folder and output_file.

## Combining Swagger Files:

It iterates through each YAML file in the input folder.
Merges server details, endpoint paths, components, and tags from each YAML file into the combined Swagger definition.
Ensures the first server found is added to the combined Swagger.
## Saving Combined Swagger:
The combined Swagger definition is saved to the output file in YAML format.