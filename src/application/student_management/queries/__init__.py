from .check_group_exists_in_uni_query import CheckGroupExistsInUniQuery
from .find_group_by_name_and_uni_query import FindGroupByNameAndUniQuery
from .find_group_headman_query import FindGroupHeadmanQuery
from .find_student_query import FindStudentQuery
from .get_all_universities_query import GetAllUniversitiesQuery
from .get_university_by_alias_query import GetUniversityByAliasQuery

__all__ = [
    "FindStudentQuery",
    "GetUniversityByAliasQuery",
    "GetAllUniversitiesQuery",
    "CheckGroupExistsInUniQuery",
    "FindGroupByNameAndUniQuery",
    "FindGroupHeadmanQuery",
]
