from database_mysql_local.generic_crud import GenericCRUD
from database_mysql_local.point import Point
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .location_local_constants import LocationLocalConstants
from .region_ml import RegionMl
from .util import LocationsUtil

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class Region(GenericCRUD):
    region_ml = RegionMl()

    def __init__(self, is_test_data: bool = False):
        logger.start("start init Region")
        GenericCRUD.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.REGION_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.REGION_VIEW_NAME,
            default_id_column_name=LocationLocalConstants.REGION_ID_COLUMN_NAME,
            is_test_data=is_test_data
        )

        logger.end("end init Region")

    def insert(
            self, coordinate: Point,
            region: str, lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE, title_approved: bool = False,
            country_id: int = None, group_id: int = None) -> int or None:
        logger.start("start insert Region",
                     object={'coordinate': coordinate, 'region': region,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'country_id': country_id, 'group_id': group_id})
        is_valid = LocationsUtil.validate_insert_args(
            name=region, lang_code=lang_code, title_approved=title_approved, coordinate=coordinate)
        if not is_valid:
            logger.end(log_message="Region was not inserted because no region name was provided")
            return None
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        region_json = {
            key: value for key, value in {
                'coordinate': coordinate,
                'country_id': country_id,
                'group_id': group_id
            }.items() if value is not None
        }

        region_id = GenericCRUD.insert(self, data_json=region_json)

        region_ml_id = self.region_ml.insert(region_id=region_id,
                                             region=region,
                                             lang_code=lang_code,
                                             title_approved=title_approved)

        logger.end("end insert region",
                   object={'region_id': region_id,
                           'region_ml_id': region_ml_id})
        return region_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = GenericCRUD.select_one_dict_by_id(
            self,
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.REGION_TABLE_COLUMNS)
        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_region_id_by_region_name(region_name: str, country_id: int = None,
                                     lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE) -> int or None:
        logger.start("start get_region_id_by_region_name",
                     object={'region_name': region_name,
                             'country_id': country_id})
        if region_name is None:
            logger.end(log_message="end get_region_id_by_region_name",
                       object={'region_id': None})
            return None
        LangCode.validate(lang_code)
        lang_code = lang_code or LangCode.detect_lang_code(region_name)
        where_clause = f"title='{region_name}' AND lang_code='{lang_code.value}'"
        # TODO: Shall we add country_id to region_ml_table and region_ml_view?
        # if country_id is not None:
        #     where_clause += f" AND country_id={country_id}"

        region_id_json = Region.region_ml.select_one_dict_by_where(
            select_clause_value=LocationLocalConstants.REGION_ID_COLUMN_NAME,
            where=where_clause,
            order_by="region_id DESC")
        region_id = region_id_json.get(
            LocationLocalConstants.REGION_ID_COLUMN_NAME)

        logger.end("end get_region_id_by_region_name",
                   object={'region_id': region_id})
        return region_id
