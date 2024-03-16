# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""Entry point for pyinstaller"""


def main():
    import sys
    import logging
    import pyi_splash

    # Update the text on the splash screen
    pyi_splash.update_text("Loading...")
    pyi_splash.close()

    # Setup
    logger = logging.getLogger('orion_logger')
    logger.setLevel(logging.DEBUG)

    if sys.platform.startswith('win'):
        import multiprocessing
        logger.debug('Setting multiprocessing configuration for windows devices...')
        multiprocessing.freeze_support()

    logger.info('Launching ORION')
    import orion

    orion._frontend = 'tkinter'
    from orion.gui import orion_gui
    orion_gui.launch_gui('', verbose=True)

    # orion._frontend = ''
    # from orion.managers import orion_manager
    # orion_manager.run_manager('')

    logger.info('Done!')


if __name__ == "__main__":
    main()
