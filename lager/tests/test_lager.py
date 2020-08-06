# -*- coding: utf-8 -*-
"""
test_lager
----------------------------------

Tests for `lager` module.
"""

# from lager import pour_lager
# from os import remove, chdir, path

# def test_write_to_logfile(tmpdir):
#     """
#     Should log to a file.
#     """
#     chdir(tmpdir)
#     temp_file = 'sometempfile.log'
#     logger = pour_lager(filepath=temp_file)

#     logger.info('yeah yeah yeah')
#     logger.info('no no no')

#     logger.warning('yeah yeah yeah')
#     logger.warning('no no no')

#     logger.error('yeah yeah yeah')
#     logger.error('no no no')

#     logger.debug('yeah yeah yeah')
#     logger.debug('no no no')

#     assert path.exists('sometempfile.log')
#     with open('sometempfile.log') as f:
#         a = f.read()
#     print(a)
#     assert len(a.splitlines()) == 8


# def test_write_stdthing():
#     logger = pour_lager()
#     logger.info('yeah yeah yeah')


def test_lager_port():
    from lager import const

    assert const.LAGER_PORT == 52437
