import pytesseract
from PIL import Image

# TODO: add error logging

def tesseract_auto_blocks(image: Image.Image, lang: str = 'eng+jpn') -> list[dict]:
    
    data = pytesseract.image_to_data(image, 
        output_type=pytesseract.Output.DICT, 
        lang=lang, 
        config='--oem 1'
    )

    blocks = []
    current_block = {
        'block_num': -1,
        'lines': [
            {
                'line_num': -1,
                'text': '',
                'confidence': 0,
                'bbox': (0, 0, 0, 0)
            }
        ]
    }
    
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 30:
            text = data['text'][i].strip()
            if text:
                block_num = data['block_num'][i]
                line_num = data['line_num'][i]
                confidence = int(data['conf'][i])
                bbox = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                
                current_block_num = current_block.get('block_num')
                current_line = current_block['lines'][-1]['line_num']
                
                if block_num != current_block.get('block_num'):
                    blocks.append(current_block)
                    current_block = {
                        'block_num': block_num,
                        'lines': [
                            {
                                'line_num': line_num,
                                'text': text,
                                'confidence': confidence,
                                'bbox': bbox
                            }
                        ]
                    }
                    
                if line_num != current_line:
                    if current_block['lines'][-1]['text']:
                        current_block['lines'][-1]['text'] = current_block['lines'][-1]['text'].strip()
                    current_block['lines'].append({
                        'line_num': line_num,
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
                    current_line = line_num
                else:
                    current_block['lines'][-1]['text'] += ' ' + text
                
    blocks.append(current_block)
    
    blocks.pop(0)
    
    return blocks

def ocr(image: Image.Image, lang: str = 'eng+jpn') -> list[dict]:
    blocks = tesseract_auto_blocks(image, lang=lang)

    return blocks

if __name__ == "__main__":
    pass