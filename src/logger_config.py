import logging 
from pathlib import Path 

def setup_logger():
    log_dir=Path("logs")
    log_dir.mkdir(parents=True,exist_ok=True)
    
    log_file=log_dir / "automation.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file,encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )
    logger=logging.getLogger(__name__)
    return logger