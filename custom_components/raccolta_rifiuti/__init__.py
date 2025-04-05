import os
import shutil
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "raccolta_rifiuti"

def setup(hass, config):
    """Set up the raccolta_rifiuti component."""
    source_dir = os.path.join(os.path.dirname(__file__), "images", "img_raccolta_rifiuti")
    target_dir = os.path.join(hass.config.path("www"), "images", "img_raccolta_rifiuti")

    if not os.path.exists(source_dir):
        _LOGGER.error(f"La cartella delle immagini non esiste: {source_dir}")
        return False

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        _LOGGER.info(f"Creata la cartella target: {target_dir}")
    
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        target_file = os.path.join(target_dir, file_name)

        if not os.path.exists(target_file):
            shutil.copy(source_file, target_file)
            _LOGGER.info(f"Copiato {file_name} in www/images/img_raccolta_rifiuti")

    return True
