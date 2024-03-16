"""BILKOM train info"""

__version__ = "0.0.4"

import argparse
import logging
from datetime import datetime
from typing import Optional, Tuple

import requests

logger = logging.getLogger(__name__)


class Bilkom:
    def __init__(self, station_name: Optional[str] = None, arrival=False):
        self.station_name = None
        self.arrival = arrival
        self.station_id = None
        self.station_table = []
        self.logger = logging.getLogger("bilkom")

        if station_name:
            self.set_station_info(station_name)

    def search_for_stations(self, station_name: str):

        url = "https://bilkom.pl/stacje/szukaj"

        params = {"q": station_name, "source": "TIMETABLE"}

        r = requests.get(url=url, params=params)

        json = r.json()
        if "stations" in json and len(json["stations"]) > 0:
            return json["stations"]
        else:
            self.logger.error(f"Station with name {station_name} not found.")
            return

    def set_station_info(self, station_name: str):

        stations = self.search_for_stations(station_name)

        if stations:
            self.station_name = stations[0]["name"]
            self.station_id = stations[0]["extId"]
            self.logger.info(
                f"Setting station to {self.station_name}, id: {self.station_id}"
            )
        else:
            self.logger.error(f"Station with name {station_name} not found.")

    def get_station_table(self, date=datetime.now()):

        url = "https://bilkom.pl/stacje/tablica"

        if date.date() < datetime.now().date():
            self.logger.error("Cannot check past timetables.")
            return

        date_str, time_str = self.parse_date_format(date)

        params = {
            "nazwa": self.station_name,
            "stacja": self.station_id,
            "data": date_str,
            "time": time_str,
            "przyjazd": True if self.arrival else False,
            "_csrf": "",
        }

        r = requests.get(url=url, params=params)

        html = r.text

        self.parse_station_table_html(html)

        return self.station_table

    def parse_date_format(self, date: datetime) -> Tuple[str, str]:

        date_str = date.strftime("%d%m%Y%H%M")
        time_str = date.strftime("%H:%M")
        return (date_str, time_str)

    def parse_station_table_html(self, html: str):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        train_list = soup.find("ul", id="timetable")

        if train_list is None:
            return

        self.station_table = []

        for train in train_list.findChildren("li"):
            self.parse_train_list_item(train)

    def parse_train_list_item(self, item):
        train_no = getattr(item.find("div", class_="mobile-carrier"), "text", None)

        time_epoch = getattr(item.find("div", class_="date-time-hidden"), "text", None)
        time = datetime.fromtimestamp(int(time_epoch) / 1000) if time_epoch else None

        time_diff_elem = item.find(
            "div", class_="time", attrs={"data-difference": True}
        )
        time_diff = time_diff_elem["data-difference"] if time_diff_elem else None

        direction = getattr(item.find("div", class_="direction"), "text", None)

        track = getattr(item.find("div", class_="track"), "text", None)

        self.station_table.append(
            {
                "train_no": train_no,
                "direction": direction,
                "track": track,
                "time": time,
                "time_diff": time_diff,
            }
        )

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Bilkom train info")
        parser.add_argument("--station_name", required=True, help="Train station name")
        parser.add_argument(
            "--date",
            type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
            default=datetime.now(),
            help="Date",
        )
        return parser.parse_args()


def main():
    args = Bilkom.parse_arguments()
    bilkom = Bilkom()
    bilkom.set_station_info(args.station_name)
    table = bilkom.get_station_table(args.date)
    logger.info(table)


if __name__ == "__main__":
    main()
