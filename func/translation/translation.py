import html_to_json
from shared.translate import translate


# Translate text
def run_translation_on_text(page):
    #print('page from translation.py: ',page)
    try:
        output_json = html_to_json.convert_tables(page)
        output = output_json[0]
        translated = []

        for item in output:
            try:
                translated_item = {}  # Use a proper dictionary to hold key-value pairs
                for k, v in item.items():
                    # Translate text and store in dictionary
                    translated_item[k] = translate(v).text
                    #time.sleep(1)  # Throttle API calls to avoid exhausting memory and network resources

                translated.append(translated_item)
            except Exception as e:
                # Log or handle translation errors and continue processing other items
                print(f"Error translating item {item}: {e}")


        result = {'output': translated, 'message': 'Done', 'code': 'SUCCESS'}
        return result
    except Exception as e:
        print(f"Error in run_translation_on_text: {e}")
        return {'output': None, 'message': f'Error: {e}', 'code': 'FAILED'}