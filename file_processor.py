import os
import json
import csv
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher, unified_diff

class FileProcessor:
    """Handle various file types without external dependencies"""
    
    SUPPORTED_FORMATS = {
        '.txt': 'text',
        '.csv': 'csv',
        '.json': 'json',
        '.xml': 'xml',
    }
    
    def extract_text_from_file(self, file_path):
        """Extract text from various file types"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.txt':
            return self._read_text(file_path)
        elif ext == '.csv':
            return self._read_csv(file_path)
        elif ext == '.json':
            return self._read_json(file_path)
        elif ext == '.xml':
            return self._read_xml(file_path)
        else:
            return f"Unsupported format: {ext}\nSupported: {list(self.SUPPORTED_FORMATS.keys())}"
    
    def _read_text(self, file_path):
        """Read plain text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            for encoding in ['latin-1', 'utf-16', 'gb2312']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except:
                    continue
            raise Exception("Could not read file with any encoding")
    
    def _read_csv(self, file_path):
        """Read CSV files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                return '\n'.join([' | '.join(row) for row in rows[:100]])
        except Exception as e:
            raise Exception(f"CSV read error: {str(e)}")
    
    def _read_json(self, file_path):
        """Read JSON files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2, ensure_ascii=False)[:2000]
        except Exception as e:
            raise Exception(f"JSON read error: {str(e)}")
    
    def _read_xml(self, file_path):
        """Read XML files"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return ET.tostring(root, encoding='unicode')[:2000]
        except Exception as e:
            raise Exception(f"XML read error: {str(e)}")
    
    def compare_text(self, file1, file2):
        """Compare two text files"""
        try:
            text1 = self.extract_text_from_file(file1)
            text2 = self.extract_text_from_file(file2)
            
            matcher = SequenceMatcher(None, text1, text2)
            ratio = matcher.ratio()
            
            diff_lines = list(unified_diff(
                text1.splitlines(),
                text2.splitlines(),
                lineterm='',
                n=1
            ))
            
            result = f"Similarity: {ratio*100:.2f}%\n\n"
            result += "Differences:\n"
            result += '\n'.join(diff_lines[:50])
            
            return result
        except Exception as e:
            return f"Comparison error: {str(e)}"
