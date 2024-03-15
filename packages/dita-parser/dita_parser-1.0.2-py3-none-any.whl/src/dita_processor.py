# Contains functions like parse_ditamap(), merge_dita_files(), and split_dita_files()
import os
import re
import sys
import xml.etree.ElementTree as ET

import file_utils


def parse_ditamap(ditamap_path):
    # Parse the .ditamap file
    tree = ET.parse(ditamap_path)
    root = tree.getroot()

    def parse_topicref(topicref_element):
        href = topicref_element.get('href', None)
        if href:
            # Assuming href might contain a path to the file and an ID separated by a '#'
            file_path = href.split('#')[0]
            # Only consider direct children topicref elements to avoid redundancy
            child_topicrefs = [
                parse_topicref(child) for child in topicref_element.findall("topicref")
            ]
            return {'path': file_path, 'children': [child for child in child_topicrefs if child is not None]}
        return None

    ditamap_structure = [parse_topicref(topicref) for topicref in root.findall("topicref")]

    # Filter out None entries
    ditamap_structure = [entry for entry in ditamap_structure if entry is not None]

    return ditamap_structure


def indent(elem, level=0):
    i = "\n" + level * "  "  # Define indentation: two spaces per level
    j = "\n" + (level - 1) * "  "  # For the tail of the element

    # Indent the start of the element's text if it has children
    if len(elem) > 0:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level > 0 and (not elem.tail or not elem.tail.strip()):
            elem.tail = j

    # Recursively apply to child elements
    for child in elem:
        indent(child, level + 1)


def extract_declaration(content, declaration_type='xml'):
    # Regular expression patterns for XML and DOCTYPE declarations
    patterns = {
        'xml': r'(<\?xml .+?\?>)',  # For XML declaration
        'doctype': r'(<!DOCTYPE .+?>)'  # For DOCTYPE declaration
    }
    pattern = patterns.get(declaration_type, None)

    if pattern:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1), re.sub(pattern, '', content, count=1, flags=re.DOTALL)
    return "", content


def merge_topicref(item_element, topicref, input_directory, dita_files):
    file_path = topicref['path']
    full_path = os.path.join(input_directory, file_path)
    if full_path in dita_files:
        with open(full_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Extract XML declaration and DOCTYPE and remove them from the content
        xml_declaration, file_content = extract_declaration(file_content, 'xml')
        doctype_declaration, file_content = extract_declaration(file_content, 'doctype')

        # Store declarations as attributes of the item element
        item_element.set('xml_decl', xml_declaration)
        item_element.set('doctype', doctype_declaration)

        # Proper XML parsing
        try:
            # Wrap the content in a root element and parse it
            fragment_root = ET.fromstring(f"<root>{file_content}</root>")
            # Append the parsed content into the new item element
            for child in fragment_root:
                item_element.append(child)
        except ET.ParseError as e:
            print(f"Error parsing {full_path}: {e}", file=sys.stderr)

    # Recursively process any nested topicrefs
    for child_topicref in topicref.get('children', []):
        child_item_element = ET.SubElement(item_element, 'item', attrib={'source': child_topicref['path']})
        merge_topicref(child_item_element, child_topicref, input_directory, dita_files)


def remove_empty_items(element):
    """
    Recursively remove all empty <item> elements from the XML element.
    An <item> is considered empty if it has no children and no text content.
    """
    for child in list(element):  # list() to make a copy so we can remove items
        if child.tag == 'item':
            remove_empty_items(child)  # Recurse
            if not list(child) and not (child.text and child.text.strip()):
                element.remove(child)


def merge_topicref_to_file(item_element, topicref, input_directory, dita_files, output_file_path):
    merge_topicref(item_element, topicref, input_directory, dita_files)

    # Cleanup phase: Remove all empty <item> elements
    remove_empty_items(item_element)

    ET.ElementTree(item_element).write(output_file_path, encoding='utf-8', xml_declaration=True)
    print(f"Content saved to {output_file_path}")


def merge_dita_files(dita_files, input_directory, output_directory, ditamap_structure):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for topicref in ditamap_structure:
        # Create a new XML Element for each topicref, which might refer to a DITA file itself
        item_element = ET.Element('items', attrib={'source': topicref['path']})
        # Construct output file path
        output_file_name = topicref['path'].split('#')[0]  # Assuming 'path' includes the file name
        output_file_path = os.path.join(output_directory, output_file_name)
        # Strip the file extension and add .xml
        output_file_path = os.path.splitext(output_file_path)[0] + '.xml'

        # Write each topicref and its children to a separate file
        merge_topicref_to_file(item_element, topicref, input_directory, dita_files, output_file_path)

        missing_files = file_utils.validate_referenced_dita_files(topicref, dita_files, input_directory)
        if missing_files:
            print(
                f"Following .dita files were referenced but not found for the merged output {os.path.basename(output_file_path)}:")
            for missing in missing_files:
                print(f"  {missing}")


def has_content_or_nonempty_children(item):
    """Recursively check if the item has text content or non-empty descendants."""
    if item.text and item.text.strip():
        return True  # Item has text content
    for child in item:
        if child.tag == 'item':
            # Recursive check for non-empty descendant items
            if has_content_or_nonempty_children(child):
                return True
        else:
            return True  # Item has non-item children, which count as content
    return False


def contains_dita_content(item):
    """Check if the item contains DITA-specific content elements."""
    dita_content_tags = {'concept', 'task', 'reference', 'topic',
                         'section', 'troubleshooting', 'glossentry, glossgroup', 'bookmap'}
    return any(child.tag in dita_content_tags for child in item)


def is_leaf_and_has_content(item):
    """Check if the item is a suitable candidate for extraction as a DITA file."""
    # Check if the item contains direct DITA content or text that's not just whitespace
    has_content = (item.text and item.text.strip()) or contains_dita_content(item)
    return has_content


def decode_attribute(text):
    """Decodes XML and DOCTYPE declarations from stored attributes."""
    if not text:
        return ""
    return text.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')


def split_dita_files(merged_xml_path, output_directory):
    try:
        tree = ET.parse(merged_xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return

    # Check if the root is an <items> element with a source attribute
    if root.tag == 'items' and 'source' in root.attrib:
        source = root.attrib.get('source')
        if source and is_leaf_and_has_content(root):
            # Prepare the XML declaration and doctype, if present
            xml_decl = decode_attribute(root.attrib.get('xml_decl', ''))
            doctype = decode_attribute(root.attrib.get('doctype', ''))

            # Construct content for extraction
            content = f"{xml_decl}\n{doctype}\n" + ''.join(
                ET.tostring(child, encoding='unicode') for child in root if child.tag != 'item')

            dita_file_path = os.path.join(output_directory, source)
            os.makedirs(os.path.dirname(dita_file_path), exist_ok=True)
            try:
                with open(dita_file_path, 'w', encoding='utf-8') as dita_file:
                    dita_file.write(content)
            except IOError as e:
                print(f"Error writing to file {dita_file_path}: {e}", file=sys.stderr)

    # Continue with the existing logic for <item> elements
    for item in root.iter('item'):
        source = item.attrib.get('source')
        if not source or not is_leaf_and_has_content(item):
            continue  # Skip items without source or that do not contain relevant content

        # Prepare the XML declaration and doctype, if present
        xml_decl = decode_attribute(item.attrib.get('xml_decl', ''))
        doctype = decode_attribute(item.attrib.get('doctype', ''))

        # Construct content for extraction
        content = f"{xml_decl}\n{doctype}\n" + ''.join(
            ET.tostring(child, encoding='unicode') for child in item if child.tag != 'item')

        dita_file_path = os.path.join(output_directory, source)
        os.makedirs(os.path.dirname(dita_file_path), exist_ok=True)
        try:
            with open(dita_file_path, 'w', encoding='utf-8') as dita_file:
                dita_file.write(content)
        except IOError as e:
            print(f"Error writing to file {dita_file_path}: {e}", file=sys.stderr)


def validate_merged_xml(input_directory):
    xml_files = [file for file in os.listdir(input_directory) if file.endswith('.xml')]
    if not xml_files:
        raise FileNotFoundError(f"No valid merged .xml files found in input folder {input_directory}.")
    return xml_files
