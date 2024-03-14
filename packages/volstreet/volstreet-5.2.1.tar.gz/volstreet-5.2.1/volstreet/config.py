import urllib
import requests
import pandas as pd
import logging
import pickle
import os
from datetime import datetime
import joblib
from importlib.resources import files
from pathlib import Path
from threading import local, Event
from bs4 import BeautifulSoup
from twilio.rest import Client as TwilioClient


def get_ticker_file():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    data = urllib.request.urlopen(url).read().decode()
    df = pd.read_json(data)
    return df


def fetch_holidays():
    url = "https://www.angelone.in/nse-holidays-2023"
    backup_file = Path("holidays.csv")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find("table", attrs={"class": "inner-table"})
        headers = [th.text.strip() for th in table.find("tr").find_all("th")]
        rows = [
            [td.text.strip() for td in tr.find_all("td")]
            for tr in table.find_all("tr")[1:]
        ]

        df = pd.DataFrame(rows, columns=headers)
        df["Date"] = pd.to_datetime(df["Date"])

        # Check if the dataframe is empty and use the backup if it is
        if not df.empty:
            # Save to a CSV file
            df.to_csv(backup_file, index=False)
            holidays = df["Date"].values.astype("datetime64[D]")
        else:
            raise ValueError("Fetched data is empty, falling back to local backup.")

    except Exception as e:
        message = f"Failed to fetch holidays from {url}: {e}"
        logger.error(message)
        holidays = load_holidays_local()

    return holidays


def load_holidays_local():
    backup_file = Path("holidays.csv")
    if os.path.exists(backup_file):
        df = pd.read_csv(backup_file)
        df["Date"] = pd.to_datetime(df["Date"])
        holidays = df["Date"].values.astype("datetime64[D]")
    else:
        # Handle the case where the backup file doesn't exist
        logger.info(f"Backup file {backup_file} not found. Holidays set to empty.")
        holidays = pd.to_datetime([])
    return holidays


def get_symbol_df():
    try:
        url = "https://symbolinfo.s3.ap-south-1.amazonaws.com/symbol_info.csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df["SYMBOL"] = df["SYMBOL"].str.strip()
        return df
    except Exception as e:
        logger.error(f"Error while fetching symbols: {e}")
        return pd.DataFrame()


def load_historical_expiry_dates():
    resource_path = files("volstreet").joinpath("historical_info")
    # noinspection PyTypeChecker
    expiry_path = Path(resource_path.joinpath("index_expiries.pkl"))
    # noinspection PyTypeChecker
    with open(expiry_path, "rb") as f:
        historical_expiries = pickle.load(f)

    return historical_expiries


def load_iv_models():
    resource_path = files("volstreet").joinpath("iv_models")

    # noinspection PyTypeChecker
    curve_model_path = Path(resource_path.joinpath("iv_curve_adjuster.joblib"))
    # noinspection PyTypeChecker
    vix_to_iv_model_path = Path(resource_path.joinpath("vix_to_iv.joblib"))
    # noinspection PyTypeChecker
    atm_iv_on_expiry_day_model_path = Path(
        resource_path.joinpath("atm_iv_on_expiry_day.joblib")
    )

    models = []
    for model_path in [
        curve_model_path,
        vix_to_iv_model_path,
        atm_iv_on_expiry_day_model_path,
    ]:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
            models.append(model)
    return tuple(models)


def create_logger(
    logger_name,
    file_prefix: str = "",
    info_handler=True,
    error_handler=True,
    stream_handler=True,
):
    """
    Creates a logger with specified configurations.

    Parameters:
    logger_name (str): The name of the logger.
    file_prefix (str): The prefix for log file names.
    use_info_handler (bool): Whether to use the info file handler.
    use_error_handler (bool): Whether to use the error file handler.
    use_stream_handler (bool): Whether to use the stream handler.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    today = datetime.now().strftime("%Y-%m-%d")

    file_prefix = file_prefix + "-" if file_prefix else ""

    # Common formatter
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    )

    if info_handler:
        # Info handler
        info_log_filename = f"{file_prefix}info-{today}.log"
        info_handler = logging.FileHandler(info_log_filename)
        info_handler.setFormatter(formatter)
        info_handler.setLevel(logging.INFO)
        logger.addHandler(info_handler)

    if error_handler:
        # Error handler
        error_log_filename = f"{file_prefix}error-{today}.log"
        error_handler = logging.FileHandler(error_log_filename)
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)

    if stream_handler:
        # Stream handler for console output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)  # Set the level as per your requirement
        logger.addHandler(stream_handler)

    return logger


class Twilio:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    content_sid = os.getenv("TWILIO_CONTENT_SID")
    service_sid = os.getenv("TWILIO_SERVICE_SID")
    if account_sid is not None and auth_token is not None:
        client = TwilioClient(account_sid, auth_token)
    else:
        client = None


# Set the default values for critical variables
NOTIFIER_LEVEL = "INFO"
LARGE_ORDER_THRESHOLD = 30
ERROR_NOTIFICATION_SETTINGS = {"url": None}
LIMIT_PRICE_BUFFER = 0.01
MAX_PRICE_MODIFICATION = 0.3
MODIFICATION_STEP_SIZE = 0.05
MODIFICATION_SLEEP_INTERVAL = 0.5
CACHE_INTERVAL = 3  # in seconds

# Create loggers
logger = create_logger("volstreet")  # Main logger
bs_logger = create_logger("bs", file_prefix="bs", error_handler=False)
latency_logger = create_logger(
    "latency", file_prefix="latency", error_handler=False, stream_handler=False
)

# Get the list of scrips
scrips = get_ticker_file()
scrips["expiry_dt"] = pd.to_datetime(
    scrips[scrips.expiry != ""]["expiry"], format="%d%b%Y"
)
scrips["expiry_formatted"] = scrips["expiry_dt"].dt.strftime("%d%b%y")
scrips["expiry_formatted"] = scrips["expiry_formatted"].str.upper()

implemented_indices = [
    "NIFTY",
    "BANKNIFTY",
    "FINNIFTY",
    "MIDCPNIFTY",
    "SENSEX",
    "BANKEX",
    "INDIA VIX",
]

# Create a dictionary of token and symbol
token_symbol_dict = dict(zip(scrips["token"], scrips["symbol"]))

# Create a dictionary of token and exchange segment
token_exchange_dict = dict(zip(scrips["token"], scrips["exch_seg"]))

# Get the list of holidays
try:
    holidays = fetch_holidays()
except Exception as e:
    logger.error(f"Error while fetching holidays: {e}")
    holidays = pd.to_datetime([])

# Get the list of symbols
symbol_df = get_symbol_df()

# Load the iv models
iv_curve_model, vix_to_iv_model, expiry_day_model = load_iv_models()

# Load the historical expiry dates
historical_expiry_dates = load_historical_expiry_dates()

# Create a thread local object
thread_local = local()

modification_fields = [
    "orderid",
    "variety",
    "symboltoken",
    "price",
    "ordertype",
    "transactiontype",
    "producttype",
    "exchange",
    "tradingsymbol",
    "quantity",
    "duration",
    "status",
]
order_placed = Event()
