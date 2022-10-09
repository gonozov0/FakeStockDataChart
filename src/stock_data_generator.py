import logging
import time

from repository import SessionLocal, generate_new_ticker_values

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    session = SessionLocal()
    try:
        while True:
            generate_new_ticker_values(session=session)
            logging.info("New stock data has been generated")
            time.sleep(1)
    finally:
        session.close()
