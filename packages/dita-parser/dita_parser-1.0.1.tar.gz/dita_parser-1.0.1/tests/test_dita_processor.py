import os.path
import unittest
from unittest.mock import patch, mock_open, call

from src.dita_processor import *


class TestDitaProcessor(unittest.TestCase):
    test_dir = "test_dita_files"
    output_dir = os.path.join(test_dir, "output")
    ditamap_path = os.path.join(test_dir, "example.ditamap")
    topic1_path = os.path.join(test_dir, "topic1.dita")
    topic2_path = os.path.join(test_dir, "topic2.dita")

    ditamap_nested_path = os.path.join(test_dir, "example_nested.ditamap")
    subtopic1_path = os.path.join(test_dir, "subtopic1.dita")

    @classmethod
    def setUpClass(cls):
        os.makedirs(cls.test_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)

        # Create example .ditamap file
        ditamap_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE map PUBLIC "-//OASIS//DTD DITA 1.3 Map//EN" "technicalContent/dtd/map.dtd" []>
        <map>
            <topicref href="topic1.dita"/>
            <topicref href="topic2.dita"/>
        </map>'''

        # Create nested example .ditamap file
        ditamap_nested_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE map PUBLIC "-//OASIS//DTD DITA 1.3 Map//EN" "technicalContent/dtd/map.dtd" []>
        <map>
            <topicref href="topic1.dita">
                <topicref href="subtopic1.dita"/>
            </topicref>
            <topicref href="topic2.dita"/>
        </map>'''

        with open(cls.ditamap_path, "w") as f:
            f.write(ditamap_content)
        with open(cls.ditamap_nested_path, "w") as f:
            f.write(ditamap_nested_content)

        # Create example .dita files
        topic1_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Topic//EN" "topic.dtd">
        <topic id="topic1">
            <title>Topic 1</title>
            <body>
                <p>This is the content of Topic 1.</p>
            </body>
        </topic>'''
        topic2_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Composite//EN" "composite.dtd">
        <topic id="topic2">
            <title>Topic 2</title>
            <body>
                <p>This is the content of Topic 2.</p>
            </body>
        </topic>'''
        subtopic1_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Topic//EN" "topic.dtd">
        <topic id="subtopic1">
            <title>Subtopic 1</title>
            <body>
                <p>This is the content of Subtopic 1 nested within Topic 1.</p>
            </body>
        </topic>'''
        with open(cls.topic1_path, "w") as f:
            f.write(topic1_content)
        with open(cls.topic2_path, "w") as f:
            f.write(topic2_content)
        with open(cls.subtopic1_path, "w") as f:
            f.write(subtopic1_content)

    def test_parse_ditamap(self):
        # Test parsing the .ditamap file
        structure = parse_ditamap(self.ditamap_path)
        self.assertEqual(len(structure), 2, "Should have two top-level topicrefs")

        paths = [item['path'] for item in structure]
        self.assertIn("topic1.dita", paths, "topic1.dita should be in the parsed structure")
        self.assertIn("topic2.dita", paths, "topic2.dita should be in the parsed structure")

    def test_parse_ditamap_nested(self):
        structure = parse_ditamap(self.ditamap_nested_path)

        # Find the entry for topic1.dita to check for nested structure
        topic1_entry = next((item for item in structure if item['path'] == 'topic1.dita'), None)
        self.assertIsNotNone(topic1_entry, "topic1.dita should be in the parsed structure")

        # Check that topic1.dita has a nested topicref
        self.assertTrue('children' in topic1_entry, "topic1.dita should have nested topicrefs")
        self.assertEqual(len(topic1_entry['children']), 1, "topic1.dita should have one nested topicref")

        nested_topic_path = topic1_entry['children'][0]['path']
        self.assertEqual(nested_topic_path, 'subtopic1.dita', "The nested topic should be subtopic1.dita")

    def test_merge_dita_files(self):
        # Prepare input
        dita_files = [self.topic1_path, self.topic2_path]
        ditamap_structure = parse_ditamap(self.ditamap_path)

        # Execute the merge function
        merge_dita_files(dita_files, self.test_dir, self.output_dir, ditamap_structure)

        # Check if the merged XML files exist
        file1 = os.path.join(self.output_dir, "topic1.xml")
        file2 = os.path.join(self.output_dir, "topic2.xml")
        self.assertTrue(os.path.exists(file1), "Merged file for topic1.dita does not exist")
        self.assertTrue(os.path.exists(file2), "Merged file for topic2.dita does not exist")

    def test_merged_xml_structure_with_declarations(self):
        dita_files = [self.topic1_path, self.topic2_path]
        ditamap_structure = parse_ditamap(self.ditamap_path)
        merge_dita_files(dita_files, self.test_dir, self.output_dir, ditamap_structure)

        # Check if the merged XML files exist
        file1 = os.path.join(self.output_dir, "topic1.xml")
        file2 = os.path.join(self.output_dir, "topic2.xml")
        self.assertTrue(os.path.exists(file1), "Merged file for topic1.dita does not exist")
        self.assertTrue(os.path.exists(file2), "Merged file for topic2.dita does not exist")

        # Parse the merged files
        for file in [file1, file2]:
            tree = ET.parse(file)
            root = tree.getroot()

            self.assertEqual(root.tag, 'items', "Merged file root element is not <items>.")

            # Retrieve original XML and DOCTYPE declarations from the .dita files
            original_declarations = {}
            for file in dita_files:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    xml_decl = re.search(r'(<\?xml .+?\?>)', content)
                    doctype = re.search(r'(<!DOCTYPE .+?>)', content)
                    original_declarations[os.path.basename(file)] = {
                        'xml': xml_decl.group(1) if xml_decl else '',
                        'doctype': doctype.group(1) if doctype else ''
                    }

            # Check for each <item>
            for item in root.findall('item'):
                self.assertIn('source', item.attrib, "<item> element is missing 'source' attribute")
                source = item.attrib['source']
                expected_xml_decl = original_declarations[source]['xml']
                expected_doctype = original_declarations[source]['doctype']
                xml_decl_in_item = item.attrib.get('xml_decl', '')
                doctype_in_item = item.attrib.get('doctype', '')

                # Check the XML declaration
                self.assertEqual(xml_decl_in_item, expected_xml_decl,
                                 f"XML declaration in <item> does not match original for {source}")

                # Check the DOCTYPE declaration
                self.assertEqual(doctype_in_item, expected_doctype,
                                 f"DOCTYPE declaration in <item> does not match original for {source}")

                # Check for well-formed XML content
                self.assertTrue(list(item), f"The <item> element for '{source}' does not contain well-formed XML")

    def test_merged_xml_structure_with_nesting(self):
        dita_files = [self.topic1_path, self.topic2_path, self.subtopic1_path]
        ditamap_structure = parse_ditamap(self.ditamap_nested_path)
        merge_dita_files(dita_files, self.test_dir, self.output_dir, ditamap_structure)

        file_path = os.path.join(self.output_dir, "topic1.xml")
        self.assertTrue(os.path.exists(file_path), "Merged file for topic1.dita does not exist")

        tree = ET.parse(file_path)
        root = tree.getroot()

        self.assertEqual(root.tag, 'items', "Root element should be <items>")
        self.assertEqual(root.attrib.get('source'), 'topic1.dita', "Root source attribute should be 'topic1.dita'")

        topic = root.find('topic')
        self.assertIsNotNone(topic, "Topic should be present in the merged structure")
        self.assertEqual(topic.attrib.get('id'), 'topic1', "Topic id should be 'topic1'")

        item = root.find('item')
        self.assertIsNotNone(item, "Item should be present in the merged structure")
        self.assertEqual(item.attrib.get('source'), 'subtopic1.dita',
                         "Item source attribute should be 'subtopic1.dita'")

    def _assert_no_subtopics(self, root, topic):
        topic_xpath = f"./item[@source='{topic}.dita']/item"
        subtopic_items = root.findall(topic_xpath)
        self.assertEqual(len(subtopic_items), 0, f"No subtopics should be present under {topic}")

    @patch('os.path.isfile', return_value=True)
    @patch('xml.etree.ElementTree.parse')
    def test_split_dita_files(self, mock_et_parse, mock_isfile):
        # Define the XML structure as a string (For illustrative purposes)
        merged_xml_content = """
            <items source="topic1.dita" xml_decl="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;" doctype="&lt;!DOCTYPE topic PUBLIC &quot;-//OASIS//DTD DITA Topic//EN&quot; &quot;topic.dtd&quot;&gt;">
                    <topic id="topic1">
                        <title>Topic 1</title>
                        <body>
                            <p>This is the content of Topic 1.</p>
                        </body>
                    </topic>
                    <item source="subtopic1.dita" xml_decl="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;" doctype="&lt;!DOCTYPE topic PUBLIC &quot;-//OASIS//DTD DITA Topic//EN&quot; &quot;topic.dtd&quot;&gt;">
                        <topic id="subtopic1">
                            <title>Subtopic 1</title>
                            <body>
                                <p>This is the content of Subtopic 1 nested within Topic 1.</p>
                            </body>
                        </topic>
                    </item>
            </items>
            """

        tree = ET.ElementTree(ET.fromstring(merged_xml_content))
        mock_et_parse.return_value = tree

        input_directory = os.path.join('path', 'to', 'merged')
        output_directory = os.path.join('path', 'to', 'split')

        with patch('builtins.open', mock_open(), create=True) as mocked_open:
            split_dita_files(os.path.join(input_directory, 'merged.xml'), output_directory)

            # Expected calls to the mocked open function
            expected_calls = [
                call(os.path.join(output_directory, 'topic1.dita'), 'w', encoding='utf-8'),
                call(os.path.join(output_directory, 'subtopic1.dita'), 'w', encoding='utf-8'),
            ]

            # Verify the mocked open function was called as expected
            mocked_open.assert_has_calls(expected_calls, any_order=True)


if __name__ == '__main__':
    unittest.main()
