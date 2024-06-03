SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "ALTER", "ADD", "DROP", "TRUNCATE", "JOIN", "INNER", "LEFT",
    "RIGHT", "FULL", "OUTER", "GROUP", "BY", "ORDER", "HAVING", "UNION", "DISTINCT",
    "LIMIT", "OFFSET"
] 

ALL_DB: dict[str, str] = {
    'california schools': "california_schools",
    'card games': "card_games",
    'codebase community': "codebase_community",
    'debit card specializing': "debit_card_specializing",
    'european football': "european_football_2",
    'financial': "financial",
    'formula 1': "formuala_1",
    'student club': "student_club",
    'superhero': "superhero",
    'thrombosis prediction': "thrombosis_prediction",
    'toxicology': "toxicology",     
}

db_list = sorted([key for key in ALL_DB])