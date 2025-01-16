import os

class FileNameMatcher:
    def __init__(self, dir1, dir2, sample_filename):
        """
        Initialize the FileNameMatcher with directories and a sample filename.

        Parameters:
            dir1 (str): Path to the first directory.
            dir2 (str): Path to the second directory.
            sample_filename (str): A sample filename to determine the matching length.
        """
        self.dir1 = dir1
        self.dir2 = dir2
        self.match_length = len(os.path.splitext(sample_filename)[0])

    def extract_base(self, filename):
        """
        Extract the base portion of the filename up to the specified match length.

        Parameters:
            filename (str): The filename to process.

        Returns:
            str: The extracted base portion of the filename.
        """
        base_name = os.path.splitext(filename)[0]
        return base_name[:self.match_length]

    def find_matches(self):
        """
        Find matches between filenames in the two directories based on the extracted base portion.

        Returns:
            list: A list of tuples containing matched file names.
        """
        files1 = os.listdir(self.dir1)
        files2 = os.listdir(self.dir2)

        # Create dictionaries with extracted bases as keys and original filenames as values
        base_map1 = {self.extract_base(file): file for file in files1}
        base_map2 = {self.extract_base(file): file for file in files2}

        matches = []

        # Find common bases between the two dictionaries
        for base in base_map1:
            if base in base_map2:
                matches.append((base_map1[base], base_map2[base]))

        return matches

if __name__ == "__main__":
    dir1 = input("Enter the path to the first directory: ").strip()
    dir2 = input("Enter the path to the second directory: ").strip()
    sample_filename = input("Enter a sample filename to determine the matching length: ").strip()

    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        print("One or both of the provided paths are not valid directories.")
    else:
        matcher = FileNameMatcher(dir1, dir2, sample_filename)
        matches = matcher.find_matches()

        if matches:
            print("\nMatches found:")
            for match in matches:
                print(f"File1: {match[0]}\nFile2: {match[1]}\n")
        else:
            print("No matches found.")


# from file_name_matcher import FileNameMatcher
#
# # Example directories and sample filename
# dir1 = "/path/to/dir1"
# dir2 = "/path/to/dir2"
# sample_filename = "1MC08-BBV_MSD-ME-DGA-NS01_NL01-250301-S4-C01.pdf"
#
# # Instantiate the matcher
# matcher = FileNameMatcher(dir1, dir2, sample_filename)
#
# # Find matches
# matches = matcher.find_matches()
#
# # Print matches
# if matches:
#     print("Matches found:")
#     for match in matches:
#         print(f"File1: {match[0]}, File2: {match[1]}")
# else:
#     print("No matches found.")
