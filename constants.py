REGULATION_CATEGORIES = {
    'AD': 'Aerospace and Transportation',
    'AEP': 'Agriculture, Environment, and Public Lands',
    'BFS': 'Banking and Financial',
    'CT': 'Commerce and International',
    'LES': 'Defense, Law Enforcement, and Security',
    'EELS': 'Education, Labor, Presidential, and Government Services',
    'EUMM': 'Energy, Natural Resources, and Utilities',
    'HCFP': 'Food Safety, Health, and Pharmaceutical',
    'PRE': 'Housing, Development, and Real Estate',
    'ITT': 'Technology and Telecommunications',
}
QUERY_CATEGORY = 'ITT'  # enter regulation category of interest here
RESULTS_PER_QUERY = 10  # will fetch this #/2 'PR' and 'FR' records from the regulation category above
QUERY_IS_OPEN = True  # whether to filter by comment period open or closed
