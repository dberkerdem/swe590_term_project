import io


def prepare_csv(file_obj: object) -> str:
    # Get the body
    body = file_obj.get('Body')
    # Decode content
    lines = body.read().decode('utf-8').splitlines()
    # Set the results
    results = ' '
    for line in lines:
        results.join(line)
    return results
