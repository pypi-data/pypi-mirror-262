import os


def find_ditamap_in_directory(input_directory):
    if not os.path.exists(input_directory):
        raise ValueError(f"Input path {input_directory} does not exist.")

    ditamap_files = [file for file in os.listdir(input_directory) if file.endswith('.ditamap')]
    if len(ditamap_files) == 0:
        raise ValueError(f"Ditamap not found in input folder {input_directory}.")
    if len(ditamap_files) > 1:
        raise ValueError(
            f"Multiple ditamap files found in input folder {input_directory}. Please ensure only one exists.")

    return os.path.join(input_directory, ditamap_files[0])


def list_dita_files(input_directory):
    dita_files = [os.path.join(input_directory, file) for file in os.listdir(input_directory) if file.endswith('.dita')]
    if not dita_files:
        raise ValueError(f"No .dita files found in input folder {input_directory}.")
    return dita_files


def validate_referenced_dita_files(ditamap_structure, dita_files, input_directory):
    missing_files = []

    # If ditamap_structure is not a list, wrap it in a list
    if not isinstance(ditamap_structure, list):
        ditamap_structure = [ditamap_structure]

    def validate_structure(structure):
        for item in structure:
            file_path = item.get('path')
            full_path = os.path.join(input_directory, file_path)
            if full_path not in dita_files:
                missing_files.append(file_path)
            if item.get('children'):
                validate_structure(item['children'])

    validate_structure(ditamap_structure)
    return missing_files
