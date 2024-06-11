import logging
import os
import time
from argparse import ArgumentParser

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)-7s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("patriot")

from patriot.patriot import Radar, IFF, MissileLauncher, Target


def main(csv_path: str):
    logger.info("Starting simulation")
    radar = Radar(csv_path)
    iff = IFF()
    missile_launcher = MissileLauncher()

    radar.attach(iff)
    iff.attach(missile_launcher)

    with open(csv_path) as src:
        for line in src.readlines():
            target: Target = radar.update(line)
            if target.disposition == "hostile":
                logger.warning(target)
            else:
                logger.info(target)
            time.sleep(1)


parser = ArgumentParser()
parser.add_argument("radar_output_path", type=str, help="path to radar-output csv file")
args = parser.parse_args()
if os.path.exists(args.radar_output_path):
    main(args.radar_output_path)
else:
    logger.error("Radar csv file does not exist")
