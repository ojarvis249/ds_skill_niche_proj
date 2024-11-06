import re


class SalaryProcessor:
    """
    A class to process and convert salary information from job descriptions.
    """

    @staticmethod
    def extract_salary(job_description):
        """
        Extracts the salary from a job description string if it matches a specific pattern.

        Args:
            job_description (str): The job description text that may contain salary information.

        Returns:
            str or None: The extracted salary as a string if a match is found (e.g., "£30,000");
                         otherwise, returns None if no match is found.

        Example:
            >>> SalaryProcessor.extract_salary("This position offers a salary of £30,000 per year.")
            '£30,000'
        """
        salary_pattern = r"£[\d,]+"
        match = re.search(salary_pattern, job_description)
        if match:
            return match.group(0)
        return None

    @staticmethod
    def convert_salary(salary):
        """
        Converts a salary string with optional currency symbols and suffixes to an integer.
        Handles both lowercase and uppercase "K" suffixes (e.g., "45K" becomes 45000, "45k" becomes 45000).

        Args:
            salary (str or int or float): The salary value, which can be a string with
                                          currency symbols (e.g., "£30,000", "70K"), an integer,
                                          or a float.

        Returns:
            int or None: The salary as an integer (e.g., "70K" becomes 70000, "£30,000" becomes 30000)
                         if conversion is successful; otherwise, None if the salary cannot be converted.
        """
        # Convert to string, remove symbols, commas, and unnecessary whitespace
        salary = str(salary).replace("£", "").replace(",", "").strip()

        # Handle the salary range format '45k - 50k' and extract the first value
        salary_range_match = re.search(
            r"(\d{2,})(k|K)", salary
        )  # Match a number followed by 'K' or 'k'
        if salary_range_match:
            # Extract the first salary value and convert it
            salary_value = salary_range_match.group(1)  # Get the salary number before K
            return int(salary_value) * 1000  # Convert '45k' -> 45000

        # Handle 'K' or 'k' suffix (e.g., '45K' or '45k' becomes 45000)
        match_k = re.match(r"(\d+)(k|K)?", salary)  # Match numbers with optional 'K'
        if match_k:
            number = int(match_k.group(1))  # Extract the number part
            if match_k.group(2):  # If 'K' or 'k' is present
                return number * 1000  # Convert '45k' -> 45000
            return number  # No 'K', return the number itself

        # If the salary is not valid or doesn't match expected patterns, return None
        return None


# Example string with mixed content
