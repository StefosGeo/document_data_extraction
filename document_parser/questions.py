from enum import Enum


class GreekQuestion(Enum):
    AREA = "Ποσα τ.μ (τετραγωνικα μετρα) ειναι το διαμερισμα/ακινητο?"
    LOCATION = ("Σε ποια οδο (τοποθεσια) βρισκεται το διαμερισμα/ακινητο? Βρες οδο και αριθμό, "
                "απαντησε σε μορφη: οδος|αριθμος")
    FLOOR = "Σε ποιον όροφο ειναι το διαμερισμα/ακινητο? Δωσε την απαντηση σε αριθμο"
    CONSTRUCTION_YEAR = "Ποιο ειναι το ετος κατασκευής του διαμερισματος/ακινητου?"
    OWNERSHIP_PERCENTAGE = "Τι ποσοστό ιδοκτησίας του διαμερισματος/ακινητου διατίθεται?"


class EnglishQuestion(Enum):
    AREA = "How many square meters is the apartment / property?"
    LOCATION = ("In which street (location) is the apartment / property located? Find street and number, "
                "answer in the form: street | number")
    FLOOR = "What floor is the apartment / property on? Give the answer in number"
    CONSTRUCTION_YEAR = "What is the year of construction of the apartment / property?"
    OWNERSHIP_PERCENTAGE = "What percentage of the apartment / property is available?"


def get_questions(language):
    if language == "en":
        return EnglishQuestion
    elif language == "gr":
        return GreekQuestion
    else:
        raise ValueError(f"Language {language} not supported")
