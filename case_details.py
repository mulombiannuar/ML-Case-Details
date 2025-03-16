from database import execute_query

# function to get head stations
def get_heads():
    excluded_ids = (9, 10, 11, 12)
    query = """
        SELECT head_id, head_name 
        FROM head 
        WHERE head_id NOT IN (%s, %s, %s, %s)
        ORDER BY head_id
    """
    results = execute_query(query, excluded_ids)

    return [{"head_id": row[0], "head_name": row[1]} for row in results]


# function to get head stations
def get_head_stations(head_id: str):
    query = """
        SELECT unit_id, unit_name 
        FROM unit 
        WHERE head_id_fk = %s 
        ORDER BY unit_name ASC;
    """
    results = execute_query(query, (head_id,))

    return [{"unit_id": row[0], "unit_name": row[1]} for row in results]


# function to get head stations by station ID
def get_head_stations_by_station_id(head_id: str, station_id: str):
    query = """
        SELECT unit_id, unit_name
        FROM unit 
        WHERE head_id_fk = %s AND unit_id = %s;
    """
    results = execute_query(query, (head_id, station_id))

    return [{"unit_id": row[0], "unit_name": row[1]} for row in results]


# function to get unit divisions
def get_unit_divisions(unit_id: str):
    query = """
        SELECT ud.unit_division_id, d.division_name
        FROM unit_division ud
        JOIN division d ON d.division_id = ud.division_id_fk
        WHERE ud.unit_id_fk = %s;
    """
    results = execute_query(query, (unit_id,))

    return [{"unit_division_id": row[0], "division_name": row[1]} for row in results]



# function to getcase details
def get_case_details(case_id: int):
    return {"case_id": case_id, "details": f"Details for Case ID {case_id}"}


# function to getcase details case id
def get_case_details_by_id(case_id: int):
    query = """
        SELECT 
            cases.case_id, 
            cases.case_year, 
            cases.case_code, 
            cases.case_index, 
            cases.number_on_file, 
            cases.citation, 
            cases.filing_date, 
            case_status.case_status_desc, 
            unit.unit_name, 
            division.division_name, 
            case_types.name AS case_type_name, 
            case_categories.name AS case_category, 
            case_categories.code
        FROM cases
        INNER JOIN unit_div_case_type ON unit_div_case_type.unit_div_case_type_id = cases.unit_div_case_type_id_fk
        INNER JOIN unit_division ON unit_div_case_type.unit_division_id_fk = unit_division.unit_division_id
        INNER JOIN unit ON unit_division.unit_id_fk = unit.unit_id
        INNER JOIN division ON division.division_id = unit_division.division_id_fk
        INNER JOIN case_types ON unit_div_case_type.case_type_id_fk = case_types.case_type_id
        INNER JOIN case_status ON cases.case_status_id_fk = case_status.case_status_id
        INNER JOIN case_categories ON case_types.case_category_id_fk = case_categories.category_id
        WHERE cases.case_id = %s;
    """

    results = execute_query(query, (case_id,))

    return [
        {
            "case_id": row[0], 
            "case_year": row[1], 
            "case_code": row[2], 
            "case_index": row[3],
            "number_on_file": row[4],
            "citation": row[5],
            "filing_date": row[6],
            "case_status_desc": row[7],
            "unit_name": row[8],
            "division_name": row[9],
            "case_type_name": row[10],
            "case_category": row[11],
        } 
        for row in results
    ] if results else []


# function to get case parties
def get_case_parties(case_id: int):
    query = """
        SELECT 
            user_groups.ugrp_name as user_category, 
            CONCAT(case_party.level, ' ', case_party_types.description) AS party_type, 
            demo_user_profiles.prefered_name AS party_name, 
            demo_user_profiles.nationality, 
            demo_user_profiles.upro_phone, 
            user_accounts.uacc_email, 
            COUNT(files.file_id) AS files_count,
            case_party_types.innitiator
        FROM case_party
        INNER JOIN cases ON case_party.case_id_fk = cases.case_id
        INNER JOIN unit_div_case_type ON unit_div_case_type.unit_div_case_type_id = cases.unit_div_case_type_id_fk
        INNER JOIN case_types ON unit_div_case_type.case_type_id_fk = case_types.case_type_id
        INNER JOIN case_categories ON case_types.case_category_id_fk = case_categories.category_id
        INNER JOIN demo_user_profiles ON case_party.uacc_id_fk = demo_user_profiles.upro_uacc_fk
        INNER JOIN user_accounts ON demo_user_profiles.upro_uacc_fk = user_accounts.uacc_id
        INNER JOIN user_groups ON user_groups.ugrp_id = user_accounts.uacc_group_fk
        LEFT JOIN case_type_party_type ON case_type_party_type.case_type_party_type_id = case_party.case_party_type_id_fk
        LEFT JOIN case_party_types ON case_party.case_party_type_id_fk = case_party_types.case_party_type_id
        LEFT JOIN files ON files.party_id = case_party.case_party_id
        WHERE case_party.case_id_fk = %s
        GROUP BY 
            user_groups.ugrp_name, 
            case_party.level, case_party_types.description,
            demo_user_profiles.prefered_name, 
            demo_user_profiles.nationality, 
            demo_user_profiles.gender, 
            demo_user_profiles.upro_phone, 
            user_accounts.uacc_email, 
            case_party_types.innitiator
        ORDER BY case_party_types.innitiator DESC;
    """

    results = execute_query(query, (case_id,))
    
    return [
    {
        "user_category": row[0], 
        "party_type": row[1], 
        "party_name": row[2], 
        "nationality": row[3],
        "upro_phone": row[4],
        "uacc_email": row[5],
        "files_count": row[6],
    } 
    for row in results
   ] if results else []



# function to get case activities by case id
def get_case_activities(case_id: int):
    query = """
        SELECT 
            court_actions.court_actions_name, 
            case_activities.activity_date, 
            case_activities.remarks, 
            case_activity_outcome.outcome_remarks,
            case_outcome_description,
            case_activities.activity_deleted,
            mediation_referral.mediation_number, 
            mediation_referral.mediation_status, 
            mediation_referral.mediation_outcome
        FROM case_activities
        INNER JOIN cases ON cases.case_id = case_activities.case_id_fk 
        INNER JOIN court_processes ON case_activities.court_processes_id_fk = court_processes.court_processes_id 
        INNER JOIN court_actions ON court_processes.court_action_id_fk = court_actions.court_actions_id 
        LEFT JOIN users_activities ON users_activities.case_activity_id_fk = case_activities.case_activity_id 
        LEFT JOIN case_activity_outcome ON case_activities.case_activity_id = case_activity_outcome.case_activity_id_fk 
        LEFT JOIN outcome_adjournment_reasons ON case_activity_outcome.case_activity_outcome_id = outcome_adjournment_reasons.case_activity_outcome_id_fk 
        LEFT JOIN adjournment_reasons ON adjournment_reasons.adjournment_reasons_id = outcome_adjournment_reasons.adjournment_reasons_id_fk 
        LEFT JOIN case_type_outcome ON case_activity_outcome.case_type_outcome_id_fk = case_type_outcome.case_type_outcome_id 
        LEFT JOIN case_outcomes ON case_type_outcome.case_outcome_id_fk = case_outcomes.case_outcome_id 
        LEFT JOIN taken_out_matters ON taken_out_matters.case_activity_id_fk = case_activities.case_activity_id
        LEFT JOIN mediation_referral ON case_activities.case_activity_id = mediation_referral.case_activity_id_fk
        WHERE cases.case_id = %s
        GROUP BY 
            court_actions.court_actions_name, 
            case_activities.activity_date, 
            case_activities.remarks, 
            case_activity_outcome.outcome_remarks,
            case_outcome_description,
            case_activities.activity_deleted,
            mediation_referral.mediation_number, 
            mediation_referral.mediation_status, 
            mediation_referral.mediation_outcome
        ORDER BY case_activities.activity_date DESC;
    """

    results = execute_query(query, (case_id,))
    
    return [
    {
        "court_actions_name": row[0], 
        "activity_date": row[1], 
        #"remarks": row[2], 
        "outcome_remarks": row[3],
        "case_outcome_description": row[4],
    } 
    for row in results
   ] if results else []


# function to get outcomes activity
def get_activity_outcome(case_activity_id: int):
    query = """
        SELECT case_outcome_description, outcome_remarks, outcome_date
        FROM case_activity_outcome
        INNER JOIN case_type_outcome ON case_activity_outcome.case_type_outcome_id_fk = case_type_outcome.case_type_outcome_id
        INNER JOIN case_outcomes ON case_type_outcome.case_outcome_id_fk = case_outcomes.case_outcome_id
        INNER JOIN case_activities ON case_activity_outcome.case_activity_id_fk = case_activities.case_activity_id 
        AND case_activities.activity_deleted = 0
        LEFT JOIN activity_court_document ON activity_court_document.case_activity_outcome_id_fk = case_activity_outcome.case_activity_outcome_id
        LEFT JOIN user_accounts ON user_accounts.uacc_id = case_activity_outcome.outcome_entered_by_fk
        LEFT JOIN demo_user_profiles ON demo_user_profiles.upro_uacc_fk = user_accounts.uacc_id
        WHERE case_activities.case_activity_id = %s
    """

    results = execute_query(query, (case_activity_id,))
    
    return results if results else []

# function to get unit division case categories
def get_unit_division_case_categories(unit_division_id: int):
   
    query = """
        SELECT case_categories.category_id, 
               CONCAT(case_categories.code, ' - ', case_categories.name) AS category_name
        FROM unit_div_case_type
        INNER JOIN case_types ON case_types.case_type_id = unit_div_case_type.case_type_id_fk
        INNER JOIN case_categories ON case_categories.category_id = case_types.case_category_id_fk
        WHERE unit_div_case_type.unit_division_id_fk = %s
        AND case_categories.merge_to IS NULL
        GROUP BY case_categories.category_id, category_name
        ORDER BY case_categories.category_id ASC
    """

    results = execute_query(query, (unit_division_id,))

    return [{"category_id": row[0], "category_name": row[1]} for row in results]


# search for a case based on the given case parameters
def search_case_number(case_number, category_id, unit_division_id, case_year):
    query = """
        SELECT 
            cases.case_id, cases.case_year, cases.case_code, cases.case_index, cases.number_on_file, 
            cases.citation, cases.filing_date, case_status.case_status_desc
        FROM cases 
        LEFT JOIN case_activities ON case_activities.case_id_fk = cases.case_id 
        INNER JOIN case_status ON case_status.case_status_id = cases.case_status_id_fk 
        INNER JOIN unit_div_case_type ON cases.unit_div_case_type_id_fk = unit_div_case_type.unit_div_case_type_id 
        INNER JOIN case_types ON unit_div_case_type.case_type_id_fk = case_types.case_type_id 
        INNER JOIN case_categories ON case_types.case_category_id_fk = case_categories.category_id 
        INNER JOIN unit_division ON unit_div_case_type.unit_division_id_fk = unit_division.unit_division_id
        INNER JOIN unit ON unit.unit_id = unit_division.unit_id_fk 
        WHERE case_activities.activity_deleted = 0
        AND unit_division.unit_division_id = %s
        AND case_categories.category_id = %s
        AND cases.case_index = %s
        AND cases.case_year = %s
        AND cases.done = 1
        GROUP BY 
            cases.case_id, cases.case_year, cases.case_code, cases.case_index, cases.number_on_file, 
            cases.citation, cases.filing_date, case_status.case_status_desc
        ORDER BY cases.filing_date DESC
    """

    # Corrected query execution using named parameters
    
    results = execute_query(query, (unit_division_id, category_id, case_number, case_year)) 
    
    return [
        {
            "case_id": row[0], 
            "case_year": row[1], 
            "case_code": row[2], 
            "case_index": row[3],
            "number_on_file": row[4],
            "citation": row[5],
            "filing_date": row[6],
            "case_status_desc": row[7],
        } 
        for row in results
    ]




