import logging
import os
import sys

import plac

import dita_processor
import file_utils


@plac.annotations(
    action=plac.Annotation("Action to perform: 'merge' or 'split'", choices=['merge', 'split']),
    input_dir=plac.Annotation("Path to input directory containing .dita files or .xml files"),
    output_dir=plac.Annotation("Path to output directory where merged .xml files or split .dita files will be saved")
)
def main(action, input_dir, output_dir):
    # Validate input directory
    if input_dir and not os.path.isdir(input_dir):
        logging.error(
            f"Error: The specified input path '{input_dir}' is not a directory or does not exist. Please provide a valid input folder.")
        sys.exit(1)

    # Validate output directory
    if output_dir and not os.path.isdir(output_dir):
        logging.error(
            f"Error: The specified output path '{output_dir}' is not a directory or does not exist. Please provide a valid output folder.")
        sys.exit(1)

    if action == 'merge':
        merge_operation(input_dir, output_dir)
    elif action == 'split':
        split_operation(input_dir, output_dir)
    else:
        logging.error(f"Invalid action '{action}'. Action must be either 'merge' or 'split'.")
        sys.exit(1)


def merge_operation(input_directory, output_directory):
    try:
        ditamap_path = file_utils.find_ditamap_in_directory(input_directory)
        ditamap_structure = dita_processor.parse_ditamap(ditamap_path)
        dita_files = file_utils.list_dita_files(input_directory)

        dita_processor.merge_dita_files(dita_files, input_directory, output_directory,
                                        ditamap_structure)

    except ValueError as e:
        print(e)
        sys.exit(1)


def split_operation(input_directory, output_directory):
    try:
        xml_files = dita_processor.validate_merged_xml(input_directory)
        for xml_file in xml_files:
            merged_xml_path = os.path.join(input_directory, xml_file)
            dita_processor.split_dita_files(merged_xml_path, output_directory)
        print(f"Split operation completed. Check {output_directory} for .dita files.")
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    plac.call(main)
