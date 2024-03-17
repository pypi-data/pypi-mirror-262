from database_mysql_local.generic_crud import GenericCRUD
from database_mysql_local.point import Point
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .county_ml import CountyMl
from .location_local_constants import LocationLocalConstants
from .util import LocationsUtil

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class County(GenericCRUD):
    county_ml = CountyMl()

    def __init__(self, is_test_data: bool = False):
        logger.start("start init County")

        GenericCRUD.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.COUNTY_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.COUNTY_VIEW_NAME,
            default_id_column_name=LocationLocalConstants.COUNTY_ID_COLUMN_NAME,
            is_test_data=is_test_data
        )

        logger.end("end init County")

    def insert(
            self, county: str, lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE,
            title_approved: bool = False, coordinate: Point = None,
            group_id: int = None) -> int or None:
        logger.start("start insert county",
                     object={'coordinate': coordinate, 'county': county,
                             'lang_code': lang_code,
                             'title_approved': title_approved})
        is_valid = LocationsUtil.validate_insert_args(
            name=county, lang_code=lang_code, title_approved=title_approved, coordinate=coordinate)
        if not is_valid:
            logger.end(log_message="County was not inserted because no county name was provided")
            return None
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        county_json = {'coordinate': coordinate,
                       'group_id': group_id}

        county_id = GenericCRUD.insert(self, data_json=county_json)

        county_ml_id = self.county_ml.insert(county_id=county_id,
                                             county=county,
                                             lang_code=lang_code,
                                             title_approved=title_approved)

        logger.end("end insert county",
                   object={'county_id': county_id,
                           'county_ml_id': county_ml_id})
        return county_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = GenericCRUD.select_one_dict_by_id(
            self,
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.COUNTY_TABLE_COLUMNS)

        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)

        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_county_id_by_county_name_state_id(county_name: str, state_id: int = None,
                                              lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE) -> int or None:
        logger.start("start get_county_id_by_county_name_state_id",
                     object={'county_name': county_name, 'state_id': state_id})
        if county_name is None:
            logger.end(log_message="end get_county_id_by_county_name_state_id",
                       object={'county_id': None})
            return None
        LangCode.validate(lang_code)
        lang_code = lang_code or LangCode.detect_lang_code(county_name)
        where_clause = f"title='{county_name}' AND lang_code='{lang_code.value}'"
        # TODO: Shall we add state_id to county_ml_table and county_ml_view?
        # if state_id is not None:
        #    where_clause += f" AND state_id={state_id}"

        county_id_json = County.county_ml.select_one_dict_by_where(
            select_clause_value=LocationLocalConstants.COUNTY_ID_COLUMN_NAME,
            where=where_clause,
            order_by="county_id DESC")
        county_id = county_id_json.get(
            LocationLocalConstants.COUNTY_ID_COLUMN_NAME)

        logger.end("end get_county_id_by_county_name_state_id",
                   object={'county_id': county_id})
        return county_id
