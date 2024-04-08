
def print_with_hashtag(string):
    """
    Print a string surrounded by hashtags.

    Args:
        string (str): The string to print.

    Returns:
        None
    """
    length = len(string)
    print("#" * (length + 4))
    print("# " + string + " #")
    print("#" * (length + 4))


def print_chunks(chunkers):
    """
    Print document chunks.

    This function prints document chunks with hashtags separating each chunk.

    Args:
        chunkers (list): List of document chunks.

    Returns:
        None
    """
    for i, chunk in enumerate(chunkers):
        print_with_hashtag(f"Chunk {i}")
        print(chunk)
        print("\n\n" + "-"*80)
