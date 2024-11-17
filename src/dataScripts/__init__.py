SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "ALTER", "ADD", "DROP", "TRUNCATE", "JOIN", "INNER", "LEFT",
    "RIGHT", "FULL", "OUTER", "GROUP", "BY", "ORDER", "HAVING", "UNION", "DISTINCT",
    "LIMIT", "OFFSET"
] 

ALL_DB: dict[str, str] = {
    'california_schools': "california_schools",
    'card_games': "card_games",
    'codebase_community': "codebase_community",
    'debit_card_specializing': "debit_card_specializing",
    'european_football_2': "european_football_2",
    'financial': "financial",
    'formula_1': "formula_1",
    'student_club': "student_club",
    'superhero': "superhero",
    'thrombosis_prediction': "thrombosis_prediction",
    'toxicology': "toxicology",     
}

db_list = sorted([key for key in ALL_DB])