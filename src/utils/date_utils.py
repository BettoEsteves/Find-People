"""Date utility functions."""
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import Tuple, Optional
from loguru import logger


class DateUtils:
    """Utility functions for date calculations."""

    @staticmethod
    def calculate_age(birth_date: date, reference_date: date = None) -> int:
        """
        Calculate age from birth date.

        Args:
            birth_date: Date of birth
            reference_date: Reference date (default: today)

        Returns:
            Age in years
        """
        if reference_date is None:
            reference_date = date.today()

        age = relativedelta(reference_date, birth_date).years

        logger.debug(f"Calculated age: {age} years (from {birth_date} to {reference_date})")
        return age

    @staticmethod
    def calculate_age_at_photo(
        birth_date: date,
        photo_date: date = None,
        approximate_age: int = None
    ) -> int:
        """
        Calculate age at the time photo was taken.

        Args:
            birth_date: Date of birth
            photo_date: Date when photo was taken (optional)
            approximate_age: Approximate age in photo (fallback if photo_date unknown)

        Returns:
            Age at photo time
        """
        if photo_date:
            return DateUtils.calculate_age(birth_date, photo_date)
        elif approximate_age is not None:
            return approximate_age
        else:
            raise ValueError("Either photo_date or approximate_age must be provided")

    @staticmethod
    def parse_date(date_string: str) -> Optional[date]:
        """
        Parse date string in various formats.

        Args:
            date_string: Date string (YYYY-MM-DD, DD/MM/YYYY, etc.)

        Returns:
            Date object or None if parsing fails
        """
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt).date()
            except ValueError:
                continue

        logger.error(f"Failed to parse date: {date_string}")
        return None

    @staticmethod
    def validate_birth_date(birth_date: date) -> Tuple[bool, str]:
        """
        Validate birth date.

        Args:
            birth_date: Birth date to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        today = date.today()

        # Check if date is in the future
        if birth_date > today:
            return False, "Birth date cannot be in the future"

        # Check if age is reasonable (0-150 years)
        age = DateUtils.calculate_age(birth_date)
        if age > 150:
            return False, f"Age ({age} years) seems unrealistic"

        return True, ""

    @staticmethod
    def estimate_photo_date(birth_date: date, age_in_photo: int) -> date:
        """
        Estimate when photo was taken based on age in photo.

        Args:
            birth_date: Date of birth
            age_in_photo: Age of person in photo

        Returns:
            Estimated photo date
        """
        photo_date = birth_date + relativedelta(years=age_in_photo)
        return photo_date

    @staticmethod
    def get_age_category(age: int) -> str:
        """
        Get age category label.

        Args:
            age: Age in years

        Returns:
            Age category string
        """
        if age < 3:
            return "Baby"
        elif age < 13:
            return "Child"
        elif age < 20:
            return "Teenager"
        elif age < 30:
            return "Young Adult"
        elif age < 45:
            return "Adult"
        elif age < 60:
            return "Middle-Aged"
        elif age < 75:
            return "Senior"
        else:
            return "Elderly"

    @staticmethod
    def format_date(date_obj: date, format_str: str = "%Y-%m-%d") -> str:
        """
        Format date object to string.

        Args:
            date_obj: Date object
            format_str: Output format string

        Returns:
            Formatted date string
        """
        return date_obj.strftime(format_str)

    @staticmethod
    def get_years_months_days_difference(date1: date, date2: date) -> Tuple[int, int, int]:
        """
        Get difference between two dates in years, months, and days.

        Args:
            date1: First date
            date2: Second date

        Returns:
            Tuple of (years, months, days)
        """
        delta = relativedelta(date2, date1)
        return delta.years, delta.months, delta.days
