import os
import platform
from pathlib import Path

from file_converter.exceptions import ConvertError
from file_converter.utils.commands import run


def get_pandoc_command():
    """
    Creates pandoc command executor function.
    Much simpler than LibreOffice - Pandoc is cross-platform with consistent interface.
    """
    ext_d = Path(os.path.abspath(" ")).parent
    static_folder = ext_d / 'static'
    
    async def command_exec(filename: str, new_filename: str):
        # Extract extensions from filenames
        old_path = static_folder / filename
        new_path = static_folder / new_filename
        
        # Get file extensions to determine conversion format
        input_ext = Path(filename).suffix.lower()
        output_ext = Path(new_filename).suffix.lower()
        
        # Mapping of file extensions to Pandoc formats
        format_map = {
            '.docx': 'docx',
            '.doc': 'docx',  # Pandoc treats .doc as docx input
            '.odt': 'odt',
            '.rtf': 'rtf',
            '.pdf': 'pdf',
            '.html': 'html',
            '.htm': 'html'
        }
        
        input_format = format_map.get(input_ext, 'docx')
        output_format = format_map.get(output_ext, 'pdf')
        
        # Build pandoc command
        command = f'pandoc "{old_path}" -f {input_format} -t {output_format} -o "{new_path}"'
        
        # For PDF output, we need to specify a PDF engine and handle Unicode
        if output_format == 'pdf':
            # Use xelatex for better Unicode support (including Cyrillic)
            command += ' --pdf-engine=xelatex -V mainfont="DejaVu Sans" -V geometry:margin=2cm'
            
        # Execute conversion
        exit_code = await run(command)
        
        # Clean up source file
        if os.path.exists(old_path):
            os.remove(old_path)
            
        # Check if conversion was successful
        if exit_code != 0 or not os.path.exists(new_path):
            raise ConvertError()
                
    return command_exec