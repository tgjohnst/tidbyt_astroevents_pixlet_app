import requests
import json
import logging
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
from argparse import ArgumentParser

def parse_cmd(args: list):
    """ Parses user-supplied command line arguments """
    parser = ArgumentParser(description=__doc__)
    # Basic Configuration
    parser.add_argument('--api-url', '-a', type=str, default="https://astronomy-calendar.p.rapidapi.com/events.php", help='URL of the astro API to scrape data from (default: https://astronomy-calendar.p.rapidapi.com/events.php)')
 
    # Output Data Configuration
    parser.add_argument('--data-dir', '-d', type=str, default="event_data/", help='General directory to store event data in (default: ./event_data)')
    parser.add_argument('--store-raw', '-s', action='store_true', help='Store raw data from API in addition to processed data')
    parser.add_argument('--data-format', '-f', type=str, default="json", choices=["json", "csv"], help='Format to store raw flight data in. (default: json). JSON is recommended for now')
    parser.add_argument('--no-combine-years', '-n', action='store_true', help='Do not combine data from multiple years into a single file, output separate files instead')

    # Scraping Configuration
    parser.add_argument('--scrape-interval', type=int, default=1, help='Interval (in seconds) between scraping requests')
    parser.add_argument('--scrape-timeout', type=int, default=5, help='Timeout (in seconds) for scraping requests')
    parser.add_argument('--scrape-max-retries', type=int, default=3, help='Maximum number of retries for scraping requests before quitting')
    parser.add_argument('--scrape-years', '-y', type=int, default=10, help='Years to scrape data for (default: 10)')

    # Parsing configuration
    parser.add_argument('--date-range', '-r', )

    # Interaction
    parser.add_argument('--logfile-dir', '-l', default='logs/', type=str, help='Log file output path (Default is current directory)')
    parser.add_argument('--verbose','-v', action='store_true', help='Output log events to stout/stderr as well as the log file')
    parser.add_argument('--debug', action='store_true', help='Enable more detailed logging for debug purposes (will blow up log file size, use for testing only)')
    optS = parser.parse_args(args)
    return optS

def init_log(logfile_dir: str = '.', debug: bool = False, verbose: bool = False) -> None:
    """ Initialize logging
    Arguments:
        logfile_dir: Directory to write log file to
        debug: Enable debug logging
        verbose: Enable verbose logging (to stdout/stderr)
    """
    os.makedirs(logfile_dir, exist_ok=True)
    filedate = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level = log_level,
        format = '[%(asctime)s] %(message)s',
        datefmt = '%d/%m/%Y %H:%M:%S',
        filename = os.path.join(logfile_dir, filedate + "_scraping_log.txt")
    )
    if verbose:
        logging.getLogger().addHandler(logging.StreamHandler())

def log_args(args: list) -> None:
    """ Log args to logfile at level INFO
    Arguments:
        args: list of command line arguments
    """
    logging.info('Command line arguments:')
    logging.info('-----')
    for arg in vars(args):
        logging.info(f'{arg}: {getattr(args, arg)}')
    logging.info('-----')

def validate_args(args: list) -> None:
    """ Validate user-supplied command line arguments """
    if args.scrape_interval < 1:
        raise ValueError(f'Invalid scrape interval: {args.scrape_interval}')
    if args.scrape_timeout < 1:
        raise ValueError(f'Invalid scrape timeout: {args.scrape_timeout}')
    if args.scrape_max_retries < 1:
        raise ValueError(f'Invalid scrape max retries: {args.scrape_max_retries}')
    if args.data_format not in ['json']:
        raise ValueError(f'Invalid data format: {args.data_format} (must be json)')
    if args.data_dir == '':
        raise ValueError(f'Invalid data directory: {args.data_dir}')
    if args.logfile_dir == '':
        raise ValueError(f'Invalid logfile directory: {args.logfile_dir}')
    # TODO more args to validate
    
# Method stub for pulling data for a given year
def pull_data(api_url: str, api_key: str, api_host: str, year: int) -> dict:
    """ Pull data for a given year from the astro API """
    logging.info(f'Pulling data for year {year} from API')
    querystring = {"year":str(year)}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }
    response = requests.get(api_url, headers=headers, params=querystring)
    logging.debug(f'API response: {response}')
    pass

def pull_data_range(start_year: int, num_years: int) -> list[dict]:
    """ Pull data for a range of years from the astro API """
    # not yet implemented
    pass

def main() -> None:
    """ MAIN """
    # Parse command line arguments and init logging
    args = parse_cmd(sys.argv[1:])
    load_dotenv()
    validate_args(args)
    init_log(args.logfile_dir, debug=args.debug, verbose=args.verbose)
    log_args(args)
    # TODO

    api_key = os.getenv("x-rapidapi-key")
    host = os.getenv("x-rapidapi-host")


if __name__ == "__main__":
    main()