from database import execute_query

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


# function to getcase details case id
def get_case_details_by_id(case_id: int):
    query = """
        SELECT 
            cases.*, 
            unit.unit_name, 
            division.division_name, 
            case_status.case_status_desc as case_status, 
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

    return results[0] if results else None


# function to get case parties
def get_case_parties(case_id: int):
    query = """
        SELECT 
            user_accounts.uacc_suspend, 
            user_accounts.uacc_active, 
            user_accounts.uacc_id, 
            user_accounts.uacc_email, 
            cases.case_id, 
            case_party.case_party_id, 
            demo_user_profiles.prefered_name, 
            demo_user_profiles.upro_first_name, 
            demo_user_profiles.nationality, 
            demo_user_profiles.gender, 
            demo_user_profiles.upro_phone, 
            user_groups.ugrp_name, 
            case_party_types.description, 
            case_party_types.case_party_type_id, 
            case_party_types.innitiator, 
            case_party.level, 
            user_groups.ugrp_id, 
            case_party.uacc_id_fk, 
            case_party.entered_by_fk, 
            COUNT(files.file_id) AS files_count
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
            user_accounts.uacc_suspend, 
            user_accounts.uacc_id, 
            user_accounts.uacc_email, 
            cases.case_id, 
            case_party.case_party_id, 
            demo_user_profiles.prefered_name, 
            demo_user_profiles.upro_first_name, 
            demo_user_profiles.nationality, 
            demo_user_profiles.gender, 
            demo_user_profiles.upro_phone,  
            user_groups.ugrp_name, 
            case_party_types.description, 
            case_party_types.innitiator, 
            case_party.level, 
            user_groups.ugrp_id, 
            case_party_types.case_party_type_id, 
            case_party.uacc_id_fk
        ORDER BY case_party_types.innitiator DESC;
    """

    results = execute_query(query, (case_id,))
    
    return results if results else []


# function to get case activities by case id
def get_case_activities(case_id: int):
    query = """
        SELECT 
            case_activities.case_activity_id,
            case_activities.activity_date, 
            court_actions.court_actions_name, 
            case_activities.remarks, 
            court_actions.court_actions_id,
            case_activities.activity_deleted,
            case_type_outcome.case_outcome_id_fk, 
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
            case_activities.case_activity_id,
            case_activities.activity_date, 
            court_actions.court_actions_name, 
            case_activities.remarks, 
            court_actions.court_actions_id,
            case_activities.activity_deleted,
            case_type_outcome.case_outcome_id_fk, 
            mediation_referral.mediation_number, 
            mediation_referral.mediation_status, 
            mediation_referral.mediation_outcome
        ORDER BY case_activities.activity_date DESC;
    """

    results = execute_query(query, (case_id,))
    
    return results if results else []


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


