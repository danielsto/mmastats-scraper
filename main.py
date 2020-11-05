import src.scraper as scraper
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrapes NBA data from NBA Reference website'
        )
    parser.add_argument(
        '-mode',
        type=str,
        default="full",
        help='simple: just leagues data. full: leagues + player data')
    parser.add_argument(
        '-league',
        type=str,
        default="all",
        help='NBA, ABA, BAA or all of them')
    args = parser.parse_args()

    data = scraper.retrieve_data_leagues(args.mode, args.league)
    scraper.save_output_csv(data)
