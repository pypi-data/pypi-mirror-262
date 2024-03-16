from notion_client import Client
import pandas as pd

from src.utils.config import config, secret, load_config
from src.utils.logger import create_logger


class NotionClient:
    """Wrapper for the Notion API. Loads data from a database.

    Attributes:
        api: NotionClient object
        projects_db: List of all projects from the projects database (config)
        project_names: dict, project ids as keys, project names as values
    """

    def __init__(self):
        assert secret("NOTION_SECRET"), "Could not load NOTION_SECRET from environment variables"
        self.log = create_logger("Notion")
        self.api = Client(auth=secret("NOTION_SECRET"))

    def _get_title(self, page, property_name) -> str:
        return page["properties"][property_name]["title"][0]["plain_text"]

    def _get_text(self, page, property_name) -> str:
        return page["properties"][property_name]["rich_text"][0]["plain_text"]

    def _get_number(self, page, property_name) -> float:
        return page["properties"][property_name]["number"]

    def _get_select(self, page, property_name) -> object:
        select = page["properties"][property_name]["select"]
        return select

    def _get_select_name(self, page, property_name) -> str:
        select = page["properties"][property_name]["select"]["name"]
        return select

    def _get_multi_select(self, page, property_name) -> list[object]:
        multiselect = page["properties"][property_name]["multi_select"]
        return multiselect

    def _get_multi_select_names(self, page, property_name) -> list[str]:
        multiselect = page["properties"][property_name]["multi_select"]
        return [item["name"] for item in multiselect]

    def _get_date(self, task, property_name) -> tuple[str, str]:
        """Returns the start and end dates as strings of a task, empty if a date is not set"""
        date_property = task["properties"][property_name]["date"]
        start_date, due_date = "", ""
        if date_property is not None and date_property["start"] is not None:
            start_date = date_property["start"]
        if date_property is not None and date_property["end"] is not None:
            due_date = date_property["end"]
        date = (start_date, due_date)
        return date

    def get_properties(self, page, property_mapping) -> dict:
        """ Returns all properties of a page using the property_mapping """

        properties = {}
        for name, property_type in property_mapping.items():
            try:
                match property_type:
                    case "title": properties[name] = self._get_title(page, name)
                    case "text": properties[name] = self._get_text(page, name)
                    case "number": properties[name] = self._get_number(page, name)
                    case "select": properties[name] = self._get_select(page, name)
                    case "select_name": properties[name] = self._get_select_name(page, name)
                    case "multi_select": properties[name] = self._get_multi_select(page, name)
                    case "multi_select_names": properties[name] = self._get_multi_select_names(page, name)
                    case "date": properties[name] = self._get_date(page, name)
                    case _: properties[name] = page["properties"][property_type]
            except Exception as e:
                self.log.debug(f"Could not get property {name} from page: {e}")
                properties[name] = None
        return properties


    def get_db_entries(self, database_id: str, property_mapping: dict[str, str], query_params={}) -> pd.DataFrame:
        """Returns a dataframe with all tasks from the tasks' database (config).

        Currently ignores the project property, as it is not used in TickTick.

        Returns:
            pd.DataFrame: Dataframe with all tasks and their properties
        """

        all_tasks = pd.DataFrame()
        query = self.api.databases.query(database_id, **query_params)["results"]
        for page in query:
            properties = self.get_properties(page, property_mapping)
            all_tasks = all_tasks._append(properties, ignore_index=True)
        return all_tasks


if __name__ == "__main__":
    notion = NotionClient()
    config = load_config("config.yml")
    db_id = config["NOTION_DB_ID"]
    mapping = config["NOTION_MAPPING"]

    query_params = config["NOTION_QUERY_PARAMS"]

    df = notion.get_db_entries(db_id, mapping, query_params)
