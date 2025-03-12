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

