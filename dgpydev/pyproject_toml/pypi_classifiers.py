# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum

CLASSIFIERS: tuple[str, ...] = (
    "Development Status :: 1 - Planning",
    "Development Status :: 2 - Pre-Alpha",
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Development Status :: 6 - Mature",
    "Development Status :: 7 - Inactive",
    "Environment :: Console",
    "Environment :: Console :: Curses",
    "Environment :: Console :: Framebuffer",
    "Environment :: Console :: Newt",
    "Environment :: Console :: svgalib",
    "Environment :: GPU",
    "Environment :: GPU :: NVIDIA CUDA",
    "Environment :: GPU :: NVIDIA CUDA :: 1.0",
    "Environment :: GPU :: NVIDIA CUDA :: 1.1",
    "Environment :: GPU :: NVIDIA CUDA :: 10.0",
    "Environment :: GPU :: NVIDIA CUDA :: 10.1",
    "Environment :: GPU :: NVIDIA CUDA :: 10.2",
    "Environment :: GPU :: NVIDIA CUDA :: 11.0",
    "Environment :: GPU :: NVIDIA CUDA :: 11.1",
    "Environment :: GPU :: NVIDIA CUDA :: 11.2",
    "Environment :: GPU :: NVIDIA CUDA :: 11.3",
    "Environment :: GPU :: NVIDIA CUDA :: 11.4",
    "Environment :: GPU :: NVIDIA CUDA :: 11.5",
    "Environment :: GPU :: NVIDIA CUDA :: 11.6",
    "Environment :: GPU :: NVIDIA CUDA :: 11.7",
    "Environment :: GPU :: NVIDIA CUDA :: 2.0",
    "Environment :: GPU :: NVIDIA CUDA :: 2.1",
    "Environment :: GPU :: NVIDIA CUDA :: 2.2",
    "Environment :: GPU :: NVIDIA CUDA :: 2.3",
    "Environment :: GPU :: NVIDIA CUDA :: 3.0",
    "Environment :: GPU :: NVIDIA CUDA :: 3.1",
    "Environment :: GPU :: NVIDIA CUDA :: 3.2",
    "Environment :: GPU :: NVIDIA CUDA :: 4.0",
    "Environment :: GPU :: NVIDIA CUDA :: 4.1",
    "Environment :: GPU :: NVIDIA CUDA :: 4.2",
    "Environment :: GPU :: NVIDIA CUDA :: 5.0",
    "Environment :: GPU :: NVIDIA CUDA :: 5.5",
    "Environment :: GPU :: NVIDIA CUDA :: 6.0",
    "Environment :: GPU :: NVIDIA CUDA :: 6.5",
    "Environment :: GPU :: NVIDIA CUDA :: 7.0",
    "Environment :: GPU :: NVIDIA CUDA :: 7.5",
    "Environment :: GPU :: NVIDIA CUDA :: 8.0",
    "Environment :: GPU :: NVIDIA CUDA :: 9.0",
    "Environment :: GPU :: NVIDIA CUDA :: 9.1",
    "Environment :: GPU :: NVIDIA CUDA :: 9.2",
    "Environment :: Handhelds/PDA&#39;s",
    "Environment :: MacOS X",
    "Environment :: MacOS X :: Aqua",
    "Environment :: MacOS X :: Carbon",
    "Environment :: MacOS X :: Cocoa",
    "Environment :: No Input/Output (Daemon)",
    "Environment :: OpenStack",
    "Environment :: Other Environment",
    "Environment :: Plugins",
    "Environment :: Web Environment",
    "Environment :: Web Environment :: Buffet",
    "Environment :: Web Environment :: Mozilla",
    "Environment :: Web Environment :: ToscaWidgets",
    "Environment :: Win32 (MS Windows)",
    "Environment :: X11 Applications",
    "Environment :: X11 Applications :: GTK",
    "Environment :: X11 Applications :: Gnome",
    "Environment :: X11 Applications :: KDE",
    "Environment :: X11 Applications :: Qt",
    "Framework :: AWS CDK",
    "Framework :: AWS CDK :: 1",
    "Framework :: AWS CDK :: 2",
    "Framework :: AiiDA",
    "Framework :: Ansible",
    "Framework :: AnyIO",
    "Framework :: Apache Airflow",
    "Framework :: Apache Airflow :: Provider",
    "Framework :: AsyncIO",
    "Framework :: BEAT",
    "Framework :: BFG",
    "Framework :: Bob",
    "Framework :: Bottle",
    "Framework :: Buildout",
    "Framework :: Buildout :: Extension",
    "Framework :: Buildout :: Recipe",
    "Framework :: CastleCMS",
    "Framework :: CastleCMS :: Theme",
    "Framework :: Celery",
    "Framework :: Chandler",
    "Framework :: CherryPy",
    "Framework :: CubicWeb",
    "Framework :: Dash",
    "Framework :: Datasette",
    "Framework :: Django",
    "Framework :: Django :: 1",
    "Framework :: Django :: 1.10",
    "Framework :: Django :: 1.11",
    "Framework :: Django :: 1.4",
    "Framework :: Django :: 1.5",
    "Framework :: Django :: 1.6",
    "Framework :: Django :: 1.7",
    "Framework :: Django :: 1.8",
    "Framework :: Django :: 1.9",
    "Framework :: Django :: 2",
    "Framework :: Django :: 2.0",
    "Framework :: Django :: 2.1",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3",
    "Framework :: Django :: 3.0",
    "Framework :: Django :: 3.1",
    "Framework :: Django :: 3.2",
    "Framework :: Django :: 4",
    "Framework :: Django :: 4.0",
    "Framework :: Django :: 4.1",
    "Framework :: Django CMS",
    "Framework :: Django CMS :: 3.10",
    "Framework :: Django CMS :: 3.11",
    "Framework :: Django CMS :: 3.4",
    "Framework :: Django CMS :: 3.5",
    "Framework :: Django CMS :: 3.6",
    "Framework :: Django CMS :: 3.7",
    "Framework :: Django CMS :: 3.8",
    "Framework :: Django CMS :: 3.9",
    "Framework :: Django CMS :: 4.0",
    "Framework :: FastAPI",
    "Framework :: Flake8",
    "Framework :: Flask",
    "Framework :: Hatch",
    "Framework :: Hypothesis",
    "Framework :: IDLE",
    "Framework :: IPython",
    "Framework :: Jupyter",
    "Framework :: Jupyter :: JupyterLab",
    "Framework :: Jupyter :: JupyterLab :: 1",
    "Framework :: Jupyter :: JupyterLab :: 2",
    "Framework :: Jupyter :: JupyterLab :: 3",
    "Framework :: Jupyter :: JupyterLab :: 4",
    "Framework :: Jupyter :: JupyterLab :: Extensions",
    "Framework :: Jupyter :: JupyterLab :: Extensions :: Mime Renderers",
    "Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt",
    "Framework :: Jupyter :: JupyterLab :: Extensions :: Themes",
    "Framework :: Kedro",
    "Framework :: Lektor",
    "Framework :: Masonite",
    "Framework :: Matplotlib",
    "Framework :: Nengo",
    "Framework :: Odoo",
    "Framework :: Odoo :: 10.0",
    "Framework :: Odoo :: 11.0",
    "Framework :: Odoo :: 12.0",
    "Framework :: Odoo :: 13.0",
    "Framework :: Odoo :: 14.0",
    "Framework :: Odoo :: 15.0",
    "Framework :: Odoo :: 16.0",
    "Framework :: Odoo :: 8.0",
    "Framework :: Odoo :: 9.0",
    "Framework :: Opps",
    "Framework :: Paste",
    "Framework :: Pelican",
    "Framework :: Pelican :: Plugins",
    "Framework :: Pelican :: Themes",
    "Framework :: Plone",
    "Framework :: Plone :: 3.2",
    "Framework :: Plone :: 3.3",
    "Framework :: Plone :: 4.0",
    "Framework :: Plone :: 4.1",
    "Framework :: Plone :: 4.2",
    "Framework :: Plone :: 4.3",
    "Framework :: Plone :: 5.0",
    "Framework :: Plone :: 5.1",
    "Framework :: Plone :: 5.2",
    "Framework :: Plone :: 5.3",
    "Framework :: Plone :: 6.0",
    "Framework :: Plone :: Addon",
    "Framework :: Plone :: Core",
    "Framework :: Plone :: Theme",
    "Framework :: Pylons",
    "Framework :: Pyramid",
    "Framework :: Pytest",
    "Framework :: Review Board",
    "Framework :: Robot Framework",
    "Framework :: Robot Framework :: Library",
    "Framework :: Robot Framework :: Tool",
    "Framework :: Scrapy",
    "Framework :: Setuptools Plugin",
    "Framework :: Sphinx",
    "Framework :: Sphinx :: Extension",
    "Framework :: Sphinx :: Theme",
    "Framework :: Trac",
    "Framework :: Trio",
    "Framework :: Tryton",
    "Framework :: TurboGears",
    "Framework :: TurboGears :: Applications",
    "Framework :: TurboGears :: Widgets",
    "Framework :: Twisted",
    "Framework :: Wagtail",
    "Framework :: Wagtail :: 1",
    "Framework :: Wagtail :: 2",
    "Framework :: Wagtail :: 3",
    "Framework :: Wagtail :: 4",
    "Framework :: ZODB",
    "Framework :: Zope",
    "Framework :: Zope :: 2",
    "Framework :: Zope :: 3",
    "Framework :: Zope :: 4",
    "Framework :: Zope :: 5",
    "Framework :: Zope2",
    "Framework :: Zope3",
    "Framework :: aiohttp",
    "Framework :: cocotb",
    "Framework :: napari",
    "Framework :: tox",
    "Intended Audience :: Customer Service",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Financial and Insurance Industry",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Legal Industry",
    "Intended Audience :: Manufacturing",
    "Intended Audience :: Other Audience",
    "Intended Audience :: Religion",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Telecommunications Industry",
    "License :: Aladdin Free Public License (AFPL)",
    "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    "License :: CeCILL-B Free Software License Agreement (CECILL-B)",
    "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
    "License :: DFSG approved",
    "License :: Eiffel Forum License (EFL)",
    "License :: Free For Educational Use",
    "License :: Free For Home Use",
    "License :: Free To Use But Restricted",
    "License :: Free for non-commercial use",
    "License :: Freely Distributable",
    "License :: Freeware",
    "License :: GUST Font License 1.0",
    "License :: GUST Font License 2006-09-30",
    "License :: Netscape Public License (NPL)",
    "License :: Nokia Open Source License (NOKOS)",
    "License :: OSI Approved",
    "License :: OSI Approved :: Academic Free License (AFL)",
    "License :: OSI Approved :: Apache Software License",
    "License :: OSI Approved :: Apple Public Source License",
    "License :: OSI Approved :: Artistic License",
    "License :: OSI Approved :: Attribution Assurance License",
    "License :: OSI Approved :: BSD License",
    "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)",
    "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
    "License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)",
    "License :: OSI Approved :: Common Public License",
    "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)",
    "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
    "License :: OSI Approved :: Eiffel Forum License",
    "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)",
    "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
    "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "License :: OSI Approved :: GNU Free Documentation License (FDL)",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)",
    "License :: OSI Approved :: IBM Public License",
    "License :: OSI Approved :: ISC License (ISCL)",
    "License :: OSI Approved :: Intel Open Source License",
    "License :: OSI Approved :: Jabber Open Source License",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: MIT No Attribution License (MIT-0)",
    "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)",
    "License :: OSI Approved :: MirOS License (MirOS)",
    "License :: OSI Approved :: Motosoto License",
    "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
    "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
    "License :: OSI Approved :: Nethack General Public License",
    "License :: OSI Approved :: Nokia Open Source License",
    "License :: OSI Approved :: Open Group Test Suite License",
    "License :: OSI Approved :: Open Software License 3.0 (OSL-3.0)",
    "License :: OSI Approved :: PostgreSQL License",
    "License :: OSI Approved :: Python License (CNRI Python License)",
    "License :: OSI Approved :: Python Software Foundation License",
    "License :: OSI Approved :: Qt Public License (QPL)",
    "License :: OSI Approved :: Ricoh Source Code Public License",
    "License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)",
    "License :: OSI Approved :: Sleepycat License",
    "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)",
    "License :: OSI Approved :: Sun Public License",
    "License :: OSI Approved :: The Unlicense (Unlicense)",
    "License :: OSI Approved :: Universal Permissive License (UPL)",
    "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
    "License :: OSI Approved :: Vovida Software License 1.0",
    "License :: OSI Approved :: W3C License",
    "License :: OSI Approved :: X.Net License",
    "License :: OSI Approved :: Zope Public License",
    "License :: OSI Approved :: zlib/libpng License",
    "License :: Other/Proprietary License",
    "License :: Public Domain",
    "License :: Repoze Public License",
    "Natural Language :: Afrikaans",
    "Natural Language :: Arabic",
    "Natural Language :: Basque",
    "Natural Language :: Bengali",
    "Natural Language :: Bosnian",
    "Natural Language :: Bulgarian",
    "Natural Language :: Cantonese",
    "Natural Language :: Catalan",
    "Natural Language :: Chinese (Simplified)",
    "Natural Language :: Chinese (Traditional)",
    "Natural Language :: Croatian",
    "Natural Language :: Czech",
    "Natural Language :: Danish",
    "Natural Language :: Dutch",
    "Natural Language :: English",
    "Natural Language :: Esperanto",
    "Natural Language :: Finnish",
    "Natural Language :: French",
    "Natural Language :: Galician",
    "Natural Language :: German",
    "Natural Language :: Greek",
    "Natural Language :: Hebrew",
    "Natural Language :: Hindi",
    "Natural Language :: Hungarian",
    "Natural Language :: Icelandic",
    "Natural Language :: Indonesian",
    "Natural Language :: Irish",
    "Natural Language :: Italian",
    "Natural Language :: Japanese",
    "Natural Language :: Javanese",
    "Natural Language :: Korean",
    "Natural Language :: Latin",
    "Natural Language :: Latvian",
    "Natural Language :: Lithuanian",
    "Natural Language :: Macedonian",
    "Natural Language :: Malay",
    "Natural Language :: Marathi",
    "Natural Language :: Nepali",
    "Natural Language :: Norwegian",
    "Natural Language :: Panjabi",
    "Natural Language :: Persian",
    "Natural Language :: Polish",
    "Natural Language :: Portuguese",
    "Natural Language :: Portuguese (Brazilian)",
    "Natural Language :: Romanian",
    "Natural Language :: Russian",
    "Natural Language :: Serbian",
    "Natural Language :: Slovak",
    "Natural Language :: Slovenian",
    "Natural Language :: Spanish",
    "Natural Language :: Swedish",
    "Natural Language :: Tamil",
    "Natural Language :: Telugu",
    "Natural Language :: Thai",
    "Natural Language :: Tibetan",
    "Natural Language :: Turkish",
    "Natural Language :: Ukrainian",
    "Natural Language :: Urdu",
    "Natural Language :: Vietnamese",
    "Operating System :: Android",
    "Operating System :: BeOS",
    "Operating System :: MacOS",
    "Operating System :: MacOS :: MacOS 9",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: MS-DOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier",
    "Operating System :: Microsoft :: Windows :: Windows 7",
    "Operating System :: Microsoft :: Windows :: Windows 8",
    "Operating System :: Microsoft :: Windows :: Windows 8.1",
    "Operating System :: Microsoft :: Windows :: Windows 95/98/2000",
    "Operating System :: Microsoft :: Windows :: Windows CE",
    "Operating System :: Microsoft :: Windows :: Windows NT/2000",
    "Operating System :: Microsoft :: Windows :: Windows Server 2003",
    "Operating System :: Microsoft :: Windows :: Windows Server 2008",
    "Operating System :: Microsoft :: Windows :: Windows Vista",
    "Operating System :: Microsoft :: Windows :: Windows XP",
    "Operating System :: OS Independent",
    "Operating System :: OS/2",
    "Operating System :: Other OS",
    "Operating System :: PDA Systems",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: AIX",
    "Operating System :: POSIX :: BSD",
    "Operating System :: POSIX :: BSD :: BSD/OS",
    "Operating System :: POSIX :: BSD :: FreeBSD",
    "Operating System :: POSIX :: BSD :: NetBSD",
    "Operating System :: POSIX :: BSD :: OpenBSD",
    "Operating System :: POSIX :: GNU Hurd",
    "Operating System :: POSIX :: HP-UX",
    "Operating System :: POSIX :: IRIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: Other",
    "Operating System :: POSIX :: SCO",
    "Operating System :: POSIX :: SunOS/Solaris",
    "Operating System :: PalmOS",
    "Operating System :: RISC OS",
    "Operating System :: Unix",
    "Operating System :: iOS",
    "Programming Language :: APL",
    "Programming Language :: ASP",
    "Programming Language :: Ada",
    "Programming Language :: Assembly",
    "Programming Language :: Awk",
    "Programming Language :: Basic",
    "Programming Language :: C",
    "Programming Language :: C#",
    "Programming Language :: C++",
    "Programming Language :: Cold Fusion",
    "Programming Language :: Cython",
    "Programming Language :: D",
    "Programming Language :: Delphi/Kylix",
    "Programming Language :: Dylan",
    "Programming Language :: Eiffel",
    "Programming Language :: Emacs-Lisp",
    "Programming Language :: Erlang",
    "Programming Language :: Euler",
    "Programming Language :: Euphoria",
    "Programming Language :: F#",
    "Programming Language :: Forth",
    "Programming Language :: Fortran",
    "Programming Language :: Haskell",
    "Programming Language :: Java",
    "Programming Language :: JavaScript",
    "Programming Language :: Kotlin",
    "Programming Language :: Lisp",
    "Programming Language :: Logo",
    "Programming Language :: ML",
    "Programming Language :: Modula",
    "Programming Language :: OCaml",
    "Programming Language :: Object Pascal",
    "Programming Language :: Objective C",
    "Programming Language :: Other",
    "Programming Language :: Other Scripting Engines",
    "Programming Language :: PHP",
    "Programming Language :: PL/SQL",
    "Programming Language :: PROGRESS",
    "Programming Language :: Pascal",
    "Programming Language :: Perl",
    "Programming Language :: Pike",
    "Programming Language :: Pliant",
    "Programming Language :: Prolog",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2 :: Only",
    "Programming Language :: Python :: 2.3",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: IronPython",
    "Programming Language :: Python :: Implementation :: Jython",
    "Programming Language :: Python :: Implementation :: MicroPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Programming Language :: Python :: Implementation :: Stackless",
    "Programming Language :: R",
    "Programming Language :: REBOL",
    "Programming Language :: Rexx",
    "Programming Language :: Ruby",
    "Programming Language :: Rust",
    "Programming Language :: SQL",
    "Programming Language :: Scheme",
    "Programming Language :: Simula",
    "Programming Language :: Smalltalk",
    "Programming Language :: Tcl",
    "Programming Language :: Unix Shell",
    "Programming Language :: Visual Basic",
    "Programming Language :: XBasic",
    "Programming Language :: YACC",
    "Programming Language :: Zope",
    "Topic :: Adaptive Technologies",
    "Topic :: Artistic Software",
    "Topic :: Communications",
    "Topic :: Communications :: BBS",
    "Topic :: Communications :: Chat",
    "Topic :: Communications :: Chat :: ICQ",
    "Topic :: Communications :: Chat :: Internet Relay Chat",
    "Topic :: Communications :: Chat :: Unix Talk",
    "Topic :: Communications :: Conferencing",
    "Topic :: Communications :: Email",
    "Topic :: Communications :: Email :: Address Book",
    "Topic :: Communications :: Email :: Email Clients (MUA)",
    "Topic :: Communications :: Email :: Filters",
    "Topic :: Communications :: Email :: Mail Transport Agents",
    "Topic :: Communications :: Email :: Mailing List Servers",
    "Topic :: Communications :: Email :: Post-Office",
    "Topic :: Communications :: Email :: Post-Office :: IMAP",
    "Topic :: Communications :: Email :: Post-Office :: POP3",
    "Topic :: Communications :: FIDO",
    "Topic :: Communications :: Fax",
    "Topic :: Communications :: File Sharing",
    "Topic :: Communications :: File Sharing :: Gnutella",
    "Topic :: Communications :: File Sharing :: Napster",
    "Topic :: Communications :: Ham Radio",
    "Topic :: Communications :: Internet Phone",
    "Topic :: Communications :: Telephony",
    "Topic :: Communications :: Usenet News",
    "Topic :: Database",
    "Topic :: Database :: Database Engines/Servers",
    "Topic :: Database :: Front-Ends",
    "Topic :: Desktop Environment",
    "Topic :: Desktop Environment :: File Managers",
    "Topic :: Desktop Environment :: GNUstep",
    "Topic :: Desktop Environment :: Gnome",
    "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
    "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes",
    "Topic :: Desktop Environment :: PicoGUI",
    "Topic :: Desktop Environment :: PicoGUI :: Applications",
    "Topic :: Desktop Environment :: PicoGUI :: Themes",
    "Topic :: Desktop Environment :: Screen Savers",
    "Topic :: Desktop Environment :: Window Managers",
    "Topic :: Desktop Environment :: Window Managers :: Afterstep",
    "Topic :: Desktop Environment :: Window Managers :: Afterstep :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: Applets",
    "Topic :: Desktop Environment :: Window Managers :: Blackbox",
    "Topic :: Desktop Environment :: Window Managers :: Blackbox :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: CTWM",
    "Topic :: Desktop Environment :: Window Managers :: CTWM :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: Enlightenment",
    "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Epplets",
    "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR15",
    "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR16",
    "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR17",
    "Topic :: Desktop Environment :: Window Managers :: FVWM",
    "Topic :: Desktop Environment :: Window Managers :: FVWM :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: Fluxbox",
    "Topic :: Desktop Environment :: Window Managers :: Fluxbox :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: IceWM",
    "Topic :: Desktop Environment :: Window Managers :: IceWM :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: MetaCity",
    "Topic :: Desktop Environment :: Window Managers :: MetaCity :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: Oroborus",
    "Topic :: Desktop Environment :: Window Managers :: Oroborus :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: Sawfish",
    "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes 0.30",
    "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes pre-0.30",
    "Topic :: Desktop Environment :: Window Managers :: Waimea",
    "Topic :: Desktop Environment :: Window Managers :: Waimea :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: Window Maker",
    "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Applets",
    "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Themes",
    "Topic :: Desktop Environment :: Window Managers :: XFCE",
    "Topic :: Desktop Environment :: Window Managers :: XFCE :: Themes",
    "Topic :: Documentation",
    "Topic :: Documentation :: Sphinx",
    "Topic :: Education",
    "Topic :: Education :: Computer Aided Instruction (CAI)",
    "Topic :: Education :: Testing",
    "Topic :: Games/Entertainment",
    "Topic :: Games/Entertainment :: Arcade",
    "Topic :: Games/Entertainment :: Board Games",
    "Topic :: Games/Entertainment :: First Person Shooters",
    "Topic :: Games/Entertainment :: Fortune Cookies",
    "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
    "Topic :: Games/Entertainment :: Puzzle Games",
    "Topic :: Games/Entertainment :: Real Time Strategy",
    "Topic :: Games/Entertainment :: Role-Playing",
    "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games",
    "Topic :: Games/Entertainment :: Simulation",
    "Topic :: Games/Entertainment :: Turn Based Strategy",
    "Topic :: Home Automation",
    "Topic :: Internet",
    "Topic :: Internet :: File Transfer Protocol (FTP)",
    "Topic :: Internet :: Finger",
    "Topic :: Internet :: Log Analysis",
    "Topic :: Internet :: Name Service (DNS)",
    "Topic :: Internet :: Proxy Servers",
    "Topic :: Internet :: WAP",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Browsers",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    "Topic :: Internet :: WWW/HTTP :: Session",
    "Topic :: Internet :: WWW/HTTP :: Site Management",
    "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
    "Topic :: Internet :: WWW/HTTP :: WSGI",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
    "Topic :: Internet :: XMPP",
    "Topic :: Internet :: Z39.50",
    "Topic :: Multimedia",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Multimedia :: Graphics :: 3D Modeling",
    "Topic :: Multimedia :: Graphics :: 3D Rendering",
    "Topic :: Multimedia :: Graphics :: Capture",
    "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
    "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
    "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
    "Topic :: Multimedia :: Graphics :: Editors",
    "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
    "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
    "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    "Topic :: Multimedia :: Graphics :: Presentation",
    "Topic :: Multimedia :: Graphics :: Viewers",
    "Topic :: Multimedia :: Sound/Audio",
    "Topic :: Multimedia :: Sound/Audio :: Analysis",
    "Topic :: Multimedia :: Sound/Audio :: CD Audio",
    "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing",
    "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping",
    "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing",
    "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
    "Topic :: Multimedia :: Sound/Audio :: Conversion",
    "Topic :: Multimedia :: Sound/Audio :: Editors",
    "Topic :: Multimedia :: Sound/Audio :: MIDI",
    "Topic :: Multimedia :: Sound/Audio :: Mixers",
    "Topic :: Multimedia :: Sound/Audio :: Players",
    "Topic :: Multimedia :: Sound/Audio :: Players :: MP3",
    "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
    "Topic :: Multimedia :: Video",
    "Topic :: Multimedia :: Video :: Capture",
    "Topic :: Multimedia :: Video :: Conversion",
    "Topic :: Multimedia :: Video :: Display",
    "Topic :: Multimedia :: Video :: Non-Linear Editor",
    "Topic :: Office/Business",
    "Topic :: Office/Business :: Financial",
    "Topic :: Office/Business :: Financial :: Accounting",
    "Topic :: Office/Business :: Financial :: Investment",
    "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    "Topic :: Office/Business :: Financial :: Spreadsheet",
    "Topic :: Office/Business :: Groupware",
    "Topic :: Office/Business :: News/Diary",
    "Topic :: Office/Business :: Office Suites",
    "Topic :: Office/Business :: Scheduling",
    "Topic :: Other/Nonlisted Topic",
    "Topic :: Printing",
    "Topic :: Religion",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Artificial Life",
    "Topic :: Scientific/Engineering :: Astronomy",
    "Topic :: Scientific/Engineering :: Atmospheric Science",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Chemistry",
    "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    "Topic :: Scientific/Engineering :: GIS",
    "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    "Topic :: Scientific/Engineering :: Hydrology",
    "Topic :: Scientific/Engineering :: Image Processing",
    "Topic :: Scientific/Engineering :: Image Recognition",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Security",
    "Topic :: Security :: Cryptography",
    "Topic :: Sociology",
    "Topic :: Sociology :: Genealogy",
    "Topic :: Sociology :: History",
    "Topic :: Software Development",
    "Topic :: Software Development :: Assemblers",
    "Topic :: Software Development :: Bug Tracking",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Disassemblers",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Embedded Systems",
    "Topic :: Software Development :: Internationalization",
    "Topic :: Software Development :: Interpreters",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Java Libraries",
    "Topic :: Software Development :: Libraries :: PHP Classes",
    "Topic :: Software Development :: Libraries :: Perl Modules",
    "Topic :: Software Development :: Libraries :: Pike Modules",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries :: Ruby Modules",
    "Topic :: Software Development :: Libraries :: Tcl Extensions",
    "Topic :: Software Development :: Libraries :: pygame",
    "Topic :: Software Development :: Localization",
    "Topic :: Software Development :: Object Brokering",
    "Topic :: Software Development :: Object Brokering :: CORBA",
    "Topic :: Software Development :: Pre-processors",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
    "Topic :: Software Development :: Testing :: Acceptance",
    "Topic :: Software Development :: Testing :: BDD",
    "Topic :: Software Development :: Testing :: Mocking",
    "Topic :: Software Development :: Testing :: Traffic Generation",
    "Topic :: Software Development :: Testing :: Unit",
    "Topic :: Software Development :: User Interfaces",
    "Topic :: Software Development :: Version Control",
    "Topic :: Software Development :: Version Control :: Bazaar",
    "Topic :: Software Development :: Version Control :: CVS",
    "Topic :: Software Development :: Version Control :: Git",
    "Topic :: Software Development :: Version Control :: Mercurial",
    "Topic :: Software Development :: Version Control :: RCS",
    "Topic :: Software Development :: Version Control :: SCCS",
    "Topic :: Software Development :: Widget Sets",
    "Topic :: System",
    "Topic :: System :: Archiving",
    "Topic :: System :: Archiving :: Backup",
    "Topic :: System :: Archiving :: Compression",
    "Topic :: System :: Archiving :: Mirroring",
    "Topic :: System :: Archiving :: Packaging",
    "Topic :: System :: Benchmark",
    "Topic :: System :: Boot",
    "Topic :: System :: Boot :: Init",
    "Topic :: System :: Clustering",
    "Topic :: System :: Console Fonts",
    "Topic :: System :: Distributed Computing",
    "Topic :: System :: Emulators",
    "Topic :: System :: Filesystems",
    "Topic :: System :: Hardware",
    "Topic :: System :: Hardware :: Hardware Drivers",
    "Topic :: System :: Hardware :: Mainframes",
    "Topic :: System :: Hardware :: Symmetric Multi-processing",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Audio",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Audio/Video (AV)",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Communications Device Class (CDC)",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Diagnostic Device",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Hub",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Human Interface Device (HID)",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Mass Storage",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Miscellaneous",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Printer",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Smart Card",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Vendor",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Video (UVC)",
    "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Wireless Controller",
    "Topic :: System :: Installation/Setup",
    "Topic :: System :: Logging",
    "Topic :: System :: Monitoring",
    "Topic :: System :: Networking",
    "Topic :: System :: Networking :: Firewalls",
    "Topic :: System :: Networking :: Monitoring",
    "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog",
    "Topic :: System :: Networking :: Time Synchronization",
    "Topic :: System :: Operating System",
    "Topic :: System :: Operating System Kernels",
    "Topic :: System :: Operating System Kernels :: BSD",
    "Topic :: System :: Operating System Kernels :: GNU Hurd",
    "Topic :: System :: Operating System Kernels :: Linux",
    "Topic :: System :: Power (UPS)",
    "Topic :: System :: Recovery Tools",
    "Topic :: System :: Shells",
    "Topic :: System :: Software Distribution",
    "Topic :: System :: System Shells",
    "Topic :: System :: Systems Administration",
    "Topic :: System :: Systems Administration :: Authentication/Directory",
    "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
    "Topic :: System :: Systems Administration :: Authentication/Directory :: NIS",
    "Topic :: Terminals",
    "Topic :: Terminals :: Serial",
    "Topic :: Terminals :: Telnet",
    "Topic :: Terminals :: Terminal Emulators/X Terminals",
    "Topic :: Text Editors",
    "Topic :: Text Editors :: Documentation",
    "Topic :: Text Editors :: Emacs",
    "Topic :: Text Editors :: Integrated Development Environments (IDE)",
    "Topic :: Text Editors :: Text Processing",
    "Topic :: Text Editors :: Word Processors",
    "Topic :: Text Processing",
    "Topic :: Text Processing :: Filters",
    "Topic :: Text Processing :: Fonts",
    "Topic :: Text Processing :: General",
    "Topic :: Text Processing :: Indexing",
    "Topic :: Text Processing :: Linguistic",
    "Topic :: Text Processing :: Markup",
    "Topic :: Text Processing :: Markup :: HTML",
    "Topic :: Text Processing :: Markup :: LaTeX",
    "Topic :: Text Processing :: Markup :: Markdown",
    "Topic :: Text Processing :: Markup :: SGML",
    "Topic :: Text Processing :: Markup :: VRML",
    "Topic :: Text Processing :: Markup :: XML",
    "Topic :: Text Processing :: Markup :: reStructuredText",
    "Topic :: Utilities",
    "Typing :: Stubs Only",
    "Typing :: Typed",
)


class PyPiClassifiersEnum(Enum):
    Development_Status____1___Planning = "Development Status :: 1 - Planning"
    Development_Status____2___Pre_Alpha = "Development Status :: 2 - Pre-Alpha"
    Development_Status____3___Alpha = "Development Status :: 3 - Alpha"
    Development_Status____4___Beta = "Development Status :: 4 - Beta"
    Development_Status____5___Production_Stable = (
        "Development Status :: 5 - Production/Stable"
    )
    Development_Status____6___Mature = "Development Status :: 6 - Mature"
    Development_Status____7___Inactive = "Development Status :: 7 - Inactive"
    Environment____Console = "Environment :: Console"
    Environment____Console____Curses = "Environment :: Console :: Curses"
    Environment____Console____Framebuffer = "Environment :: Console :: Framebuffer"
    Environment____Console____Newt = "Environment :: Console :: Newt"
    Environment____Console____svgalib = "Environment :: Console :: svgalib"
    Environment____GPU = "Environment :: GPU"
    Environment____GPU____NVIDIA_CUDA = "Environment :: GPU :: NVIDIA CUDA"
    Environment____GPU____NVIDIA_CUDA____1_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 1.0"
    )
    Environment____GPU____NVIDIA_CUDA____1_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 1.1"
    )
    Environment____GPU____NVIDIA_CUDA____10_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 10.0"
    )
    Environment____GPU____NVIDIA_CUDA____10_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 10.1"
    )
    Environment____GPU____NVIDIA_CUDA____10_2 = (
        "Environment :: GPU :: NVIDIA CUDA :: 10.2"
    )
    Environment____GPU____NVIDIA_CUDA____11_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.0"
    )
    Environment____GPU____NVIDIA_CUDA____11_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.1"
    )
    Environment____GPU____NVIDIA_CUDA____11_2 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.2"
    )
    Environment____GPU____NVIDIA_CUDA____11_3 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.3"
    )
    Environment____GPU____NVIDIA_CUDA____11_4 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.4"
    )
    Environment____GPU____NVIDIA_CUDA____11_5 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.5"
    )
    Environment____GPU____NVIDIA_CUDA____11_6 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.6"
    )
    Environment____GPU____NVIDIA_CUDA____11_7 = (
        "Environment :: GPU :: NVIDIA CUDA :: 11.7"
    )
    Environment____GPU____NVIDIA_CUDA____2_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 2.0"
    )
    Environment____GPU____NVIDIA_CUDA____2_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 2.1"
    )
    Environment____GPU____NVIDIA_CUDA____2_2 = (
        "Environment :: GPU :: NVIDIA CUDA :: 2.2"
    )
    Environment____GPU____NVIDIA_CUDA____2_3 = (
        "Environment :: GPU :: NVIDIA CUDA :: 2.3"
    )
    Environment____GPU____NVIDIA_CUDA____3_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 3.0"
    )
    Environment____GPU____NVIDIA_CUDA____3_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 3.1"
    )
    Environment____GPU____NVIDIA_CUDA____3_2 = (
        "Environment :: GPU :: NVIDIA CUDA :: 3.2"
    )
    Environment____GPU____NVIDIA_CUDA____4_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 4.0"
    )
    Environment____GPU____NVIDIA_CUDA____4_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 4.1"
    )
    Environment____GPU____NVIDIA_CUDA____4_2 = (
        "Environment :: GPU :: NVIDIA CUDA :: 4.2"
    )
    Environment____GPU____NVIDIA_CUDA____5_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 5.0"
    )
    Environment____GPU____NVIDIA_CUDA____5_5 = (
        "Environment :: GPU :: NVIDIA CUDA :: 5.5"
    )
    Environment____GPU____NVIDIA_CUDA____6_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 6.0"
    )
    Environment____GPU____NVIDIA_CUDA____6_5 = (
        "Environment :: GPU :: NVIDIA CUDA :: 6.5"
    )
    Environment____GPU____NVIDIA_CUDA____7_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 7.0"
    )
    Environment____GPU____NVIDIA_CUDA____7_5 = (
        "Environment :: GPU :: NVIDIA CUDA :: 7.5"
    )
    Environment____GPU____NVIDIA_CUDA____8_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 8.0"
    )
    Environment____GPU____NVIDIA_CUDA____9_0 = (
        "Environment :: GPU :: NVIDIA CUDA :: 9.0"
    )
    Environment____GPU____NVIDIA_CUDA____9_1 = (
        "Environment :: GPU :: NVIDIA CUDA :: 9.1"
    )
    Environment____GPU____NVIDIA_CUDA____9_2 = (
        "Environment :: GPU :: NVIDIA CUDA :: 9.2"
    )
    Environment____Handhelds_PDAs = "Environment :: Handhelds/PDA&#39;s"
    Environment____MacOS_X = "Environment :: MacOS X"
    Environment____MacOS_X____Aqua = "Environment :: MacOS X :: Aqua"
    Environment____MacOS_X____Carbon = "Environment :: MacOS X :: Carbon"
    Environment____MacOS_X____Cocoa = "Environment :: MacOS X :: Cocoa"
    Environment____No_Input_Output_Daemon = "Environment :: No Input/Output (Daemon)"
    Environment____OpenStack = "Environment :: OpenStack"
    Environment____Other_Environment = "Environment :: Other Environment"
    Environment____Plugins = "Environment :: Plugins"
    Environment____Web_Environment = "Environment :: Web Environment"
    Environment____Web_Environment____Buffet = (
        "Environment :: Web Environment :: Buffet"
    )
    Environment____Web_Environment____Mozilla = (
        "Environment :: Web Environment :: Mozilla"
    )
    Environment____Web_Environment____ToscaWidgets = (
        "Environment :: Web Environment :: ToscaWidgets"
    )
    Environment____Win32_MS_Windows = "Environment :: Win32 (MS Windows)"
    Environment____X11_Applications = "Environment :: X11 Applications"
    Environment____X11_Applications____GTK = "Environment :: X11 Applications :: GTK"
    Environment____X11_Applications____Gnome = (
        "Environment :: X11 Applications :: Gnome"
    )
    Environment____X11_Applications____KDE = "Environment :: X11 Applications :: KDE"
    Environment____X11_Applications____Qt = "Environment :: X11 Applications :: Qt"
    Framework____AWS_CDK = "Framework :: AWS CDK"
    Framework____AWS_CDK____1 = "Framework :: AWS CDK :: 1"
    Framework____AWS_CDK____2 = "Framework :: AWS CDK :: 2"
    Framework____AiiDA = "Framework :: AiiDA"
    Framework____Ansible = "Framework :: Ansible"
    Framework____AnyIO = "Framework :: AnyIO"
    Framework____Apache_Airflow = "Framework :: Apache Airflow"
    Framework____Apache_Airflow____Provider = "Framework :: Apache Airflow :: Provider"
    Framework____AsyncIO = "Framework :: AsyncIO"
    Framework____BEAT = "Framework :: BEAT"
    Framework____BFG = "Framework :: BFG"
    Framework____Bob = "Framework :: Bob"
    Framework____Bottle = "Framework :: Bottle"
    Framework____Buildout = "Framework :: Buildout"
    Framework____Buildout____Extension = "Framework :: Buildout :: Extension"
    Framework____Buildout____Recipe = "Framework :: Buildout :: Recipe"
    Framework____CastleCMS = "Framework :: CastleCMS"
    Framework____CastleCMS____Theme = "Framework :: CastleCMS :: Theme"
    Framework____Celery = "Framework :: Celery"
    Framework____Chandler = "Framework :: Chandler"
    Framework____CherryPy = "Framework :: CherryPy"
    Framework____CubicWeb = "Framework :: CubicWeb"
    Framework____Dash = "Framework :: Dash"
    Framework____Datasette = "Framework :: Datasette"
    Framework____Django = "Framework :: Django"
    Framework____Django____1 = "Framework :: Django :: 1"
    Framework____Django____1_10 = "Framework :: Django :: 1.10"
    Framework____Django____1_11 = "Framework :: Django :: 1.11"
    Framework____Django____1_4 = "Framework :: Django :: 1.4"
    Framework____Django____1_5 = "Framework :: Django :: 1.5"
    Framework____Django____1_6 = "Framework :: Django :: 1.6"
    Framework____Django____1_7 = "Framework :: Django :: 1.7"
    Framework____Django____1_8 = "Framework :: Django :: 1.8"
    Framework____Django____1_9 = "Framework :: Django :: 1.9"
    Framework____Django____2 = "Framework :: Django :: 2"
    Framework____Django____2_0 = "Framework :: Django :: 2.0"
    Framework____Django____2_1 = "Framework :: Django :: 2.1"
    Framework____Django____2_2 = "Framework :: Django :: 2.2"
    Framework____Django____3 = "Framework :: Django :: 3"
    Framework____Django____3_0 = "Framework :: Django :: 3.0"
    Framework____Django____3_1 = "Framework :: Django :: 3.1"
    Framework____Django____3_2 = "Framework :: Django :: 3.2"
    Framework____Django____4 = "Framework :: Django :: 4"
    Framework____Django____4_0 = "Framework :: Django :: 4.0"
    Framework____Django____4_1 = "Framework :: Django :: 4.1"
    Framework____Django_CMS = "Framework :: Django CMS"
    Framework____Django_CMS____3_10 = "Framework :: Django CMS :: 3.10"
    Framework____Django_CMS____3_11 = "Framework :: Django CMS :: 3.11"
    Framework____Django_CMS____3_4 = "Framework :: Django CMS :: 3.4"
    Framework____Django_CMS____3_5 = "Framework :: Django CMS :: 3.5"
    Framework____Django_CMS____3_6 = "Framework :: Django CMS :: 3.6"
    Framework____Django_CMS____3_7 = "Framework :: Django CMS :: 3.7"
    Framework____Django_CMS____3_8 = "Framework :: Django CMS :: 3.8"
    Framework____Django_CMS____3_9 = "Framework :: Django CMS :: 3.9"
    Framework____Django_CMS____4_0 = "Framework :: Django CMS :: 4.0"
    Framework____FastAPI = "Framework :: FastAPI"
    Framework____Flake8 = "Framework :: Flake8"
    Framework____Flask = "Framework :: Flask"
    Framework____Hatch = "Framework :: Hatch"
    Framework____Hypothesis = "Framework :: Hypothesis"
    Framework____IDLE = "Framework :: IDLE"
    Framework____IPython = "Framework :: IPython"
    Framework____Jupyter = "Framework :: Jupyter"
    Framework____Jupyter____JupyterLab = "Framework :: Jupyter :: JupyterLab"
    Framework____Jupyter____JupyterLab____1 = "Framework :: Jupyter :: JupyterLab :: 1"
    Framework____Jupyter____JupyterLab____2 = "Framework :: Jupyter :: JupyterLab :: 2"
    Framework____Jupyter____JupyterLab____3 = "Framework :: Jupyter :: JupyterLab :: 3"
    Framework____Jupyter____JupyterLab____4 = "Framework :: Jupyter :: JupyterLab :: 4"
    Framework____Jupyter____JupyterLab____Extensions = (
        "Framework :: Jupyter :: JupyterLab :: Extensions"
    )
    Framework____Jupyter____JupyterLab____Extensions____Mime_Renderers = (
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Mime Renderers"
    )
    Framework____Jupyter____JupyterLab____Extensions____Prebuilt = (
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt"
    )
    Framework____Jupyter____JupyterLab____Extensions____Themes = (
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Themes"
    )
    Framework____Kedro = "Framework :: Kedro"
    Framework____Lektor = "Framework :: Lektor"
    Framework____Masonite = "Framework :: Masonite"
    Framework____Matplotlib = "Framework :: Matplotlib"
    Framework____Nengo = "Framework :: Nengo"
    Framework____Odoo = "Framework :: Odoo"
    Framework____Odoo____10_0 = "Framework :: Odoo :: 10.0"
    Framework____Odoo____11_0 = "Framework :: Odoo :: 11.0"
    Framework____Odoo____12_0 = "Framework :: Odoo :: 12.0"
    Framework____Odoo____13_0 = "Framework :: Odoo :: 13.0"
    Framework____Odoo____14_0 = "Framework :: Odoo :: 14.0"
    Framework____Odoo____15_0 = "Framework :: Odoo :: 15.0"
    Framework____Odoo____16_0 = "Framework :: Odoo :: 16.0"
    Framework____Odoo____8_0 = "Framework :: Odoo :: 8.0"
    Framework____Odoo____9_0 = "Framework :: Odoo :: 9.0"
    Framework____Opps = "Framework :: Opps"
    Framework____Paste = "Framework :: Paste"
    Framework____Pelican = "Framework :: Pelican"
    Framework____Pelican____Plugins = "Framework :: Pelican :: Plugins"
    Framework____Pelican____Themes = "Framework :: Pelican :: Themes"
    Framework____Plone = "Framework :: Plone"
    Framework____Plone____3_2 = "Framework :: Plone :: 3.2"
    Framework____Plone____3_3 = "Framework :: Plone :: 3.3"
    Framework____Plone____4_0 = "Framework :: Plone :: 4.0"
    Framework____Plone____4_1 = "Framework :: Plone :: 4.1"
    Framework____Plone____4_2 = "Framework :: Plone :: 4.2"
    Framework____Plone____4_3 = "Framework :: Plone :: 4.3"
    Framework____Plone____5_0 = "Framework :: Plone :: 5.0"
    Framework____Plone____5_1 = "Framework :: Plone :: 5.1"
    Framework____Plone____5_2 = "Framework :: Plone :: 5.2"
    Framework____Plone____5_3 = "Framework :: Plone :: 5.3"
    Framework____Plone____6_0 = "Framework :: Plone :: 6.0"
    Framework____Plone____Addon = "Framework :: Plone :: Addon"
    Framework____Plone____Core = "Framework :: Plone :: Core"
    Framework____Plone____Theme = "Framework :: Plone :: Theme"
    Framework____Pylons = "Framework :: Pylons"
    Framework____Pyramid = "Framework :: Pyramid"
    Framework____Pytest = "Framework :: Pytest"
    Framework____Review_Board = "Framework :: Review Board"
    Framework____Robot_Framework = "Framework :: Robot Framework"
    Framework____Robot_Framework____Library = "Framework :: Robot Framework :: Library"
    Framework____Robot_Framework____Tool = "Framework :: Robot Framework :: Tool"
    Framework____Scrapy = "Framework :: Scrapy"
    Framework____Setuptools_Plugin = "Framework :: Setuptools Plugin"
    Framework____Sphinx = "Framework :: Sphinx"
    Framework____Sphinx____Extension = "Framework :: Sphinx :: Extension"
    Framework____Sphinx____Theme = "Framework :: Sphinx :: Theme"
    Framework____Trac = "Framework :: Trac"
    Framework____Trio = "Framework :: Trio"
    Framework____Tryton = "Framework :: Tryton"
    Framework____TurboGears = "Framework :: TurboGears"
    Framework____TurboGears____Applications = "Framework :: TurboGears :: Applications"
    Framework____TurboGears____Widgets = "Framework :: TurboGears :: Widgets"
    Framework____Twisted = "Framework :: Twisted"
    Framework____Wagtail = "Framework :: Wagtail"
    Framework____Wagtail____1 = "Framework :: Wagtail :: 1"
    Framework____Wagtail____2 = "Framework :: Wagtail :: 2"
    Framework____Wagtail____3 = "Framework :: Wagtail :: 3"
    Framework____Wagtail____4 = "Framework :: Wagtail :: 4"
    Framework____ZODB = "Framework :: ZODB"
    Framework____Zope = "Framework :: Zope"
    Framework____Zope____2 = "Framework :: Zope :: 2"
    Framework____Zope____3 = "Framework :: Zope :: 3"
    Framework____Zope____4 = "Framework :: Zope :: 4"
    Framework____Zope____5 = "Framework :: Zope :: 5"
    Framework____Zope2 = "Framework :: Zope2"
    Framework____Zope3 = "Framework :: Zope3"
    Framework____aiohttp = "Framework :: aiohttp"
    Framework____cocotb = "Framework :: cocotb"
    Framework____napari = "Framework :: napari"
    Framework____tox = "Framework :: tox"
    Intended_Audience____Customer_Service = "Intended Audience :: Customer Service"
    Intended_Audience____Developers = "Intended Audience :: Developers"
    Intended_Audience____Education = "Intended Audience :: Education"
    Intended_Audience____End_Users_Desktop = "Intended Audience :: End Users/Desktop"
    Intended_Audience____Financial_and_Insurance_Industry = (
        "Intended Audience :: Financial and Insurance Industry"
    )
    Intended_Audience____Healthcare_Industry = (
        "Intended Audience :: Healthcare Industry"
    )
    Intended_Audience____Information_Technology = (
        "Intended Audience :: Information Technology"
    )
    Intended_Audience____Legal_Industry = "Intended Audience :: Legal Industry"
    Intended_Audience____Manufacturing = "Intended Audience :: Manufacturing"
    Intended_Audience____Other_Audience = "Intended Audience :: Other Audience"
    Intended_Audience____Religion = "Intended Audience :: Religion"
    Intended_Audience____Science_Research = "Intended Audience :: Science/Research"
    Intended_Audience____System_Administrators = (
        "Intended Audience :: System Administrators"
    )
    Intended_Audience____Telecommunications_Industry = (
        "Intended Audience :: Telecommunications Industry"
    )
    License____Aladdin_Free_Public_License_AFPL = (
        "License :: Aladdin Free Public License (AFPL)"
    )
    License____CC0_1_0_Universal_CC0_1_0_Public_Domain_Dedication = (
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    )
    License____CeCILL_B_Free_Software_License_Agreement_CECILL_B = (
        "License :: CeCILL-B Free Software License Agreement (CECILL-B)"
    )
    License____CeCILL_C_Free_Software_License_Agreement_CECILL_C = (
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)"
    )
    License____DFSG_approved = "License :: DFSG approved"
    License____Eiffel_Forum_License_EFL = "License :: Eiffel Forum License (EFL)"
    License____Free_For_Educational_Use = "License :: Free For Educational Use"
    License____Free_For_Home_Use = "License :: Free For Home Use"
    License____Free_To_Use_But_Restricted = "License :: Free To Use But Restricted"
    License____Free_for_non_commercial_use = "License :: Free for non-commercial use"
    License____Freely_Distributable = "License :: Freely Distributable"
    License____Freeware = "License :: Freeware"
    License____GUST_Font_License_1_0 = "License :: GUST Font License 1.0"
    License____GUST_Font_License_2006_09_30 = "License :: GUST Font License 2006-09-30"
    License____Netscape_Public_License_NPL = "License :: Netscape Public License (NPL)"
    License____Nokia_Open_Source_License_NOKOS = (
        "License :: Nokia Open Source License (NOKOS)"
    )
    License____OSI_Approved = "License :: OSI Approved"
    License____OSI_Approved____Academic_Free_License_AFL = (
        "License :: OSI Approved :: Academic Free License (AFL)"
    )
    License____OSI_Approved____Apache_Software_License = (
        "License :: OSI Approved :: Apache Software License"
    )
    License____OSI_Approved____Apple_Public_Source_License = (
        "License :: OSI Approved :: Apple Public Source License"
    )
    License____OSI_Approved____Artistic_License = (
        "License :: OSI Approved :: Artistic License"
    )
    License____OSI_Approved____Attribution_Assurance_License = (
        "License :: OSI Approved :: Attribution Assurance License"
    )
    License____OSI_Approved____BSD_License = "License :: OSI Approved :: BSD License"
    License____OSI_Approved____Boost_Software_License_1_0_BSL_1_0 = (
        "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)"
    )
    License____OSI_Approved____CEA_CNRS_Inria_Logiciel_Libre_License_version_2_1_CeCILL_2_1 = "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
    License____OSI_Approved____Common_Development_and_Distribution_License_1_0_CDDL_1_0 = "License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)"
    License____OSI_Approved____Common_Public_License = (
        "License :: OSI Approved :: Common Public License"
    )
    License____OSI_Approved____Eclipse_Public_License_1_0_EPL_1_0 = (
        "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)"
    )
    License____OSI_Approved____Eclipse_Public_License_2_0_EPL_2_0 = (
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)"
    )
    License____OSI_Approved____Eiffel_Forum_License = (
        "License :: OSI Approved :: Eiffel Forum License"
    )
    License____OSI_Approved____European_Union_Public_Licence_1_0_EUPL_1_0 = (
        "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)"
    )
    License____OSI_Approved____European_Union_Public_Licence_1_1_EUPL_1_1 = (
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)"
    )
    License____OSI_Approved____European_Union_Public_Licence_1_2_EUPL_1_2 = (
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)"
    )
    License____OSI_Approved____GNU_Affero_General_Public_License_v3 = (
        "License :: OSI Approved :: GNU Affero General Public License v3"
    )
    License____OSI_Approved____GNU_Affero_General_Public_License_v3_or_later_AGPLv3plus = "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
    License____OSI_Approved____GNU_Free_Documentation_License_FDL = (
        "License :: OSI Approved :: GNU Free Documentation License (FDL)"
    )
    License____OSI_Approved____GNU_General_Public_License_GPL = (
        "License :: OSI Approved :: GNU General Public License (GPL)"
    )
    License____OSI_Approved____GNU_General_Public_License_v2_GPLv2 = (
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    )
    License____OSI_Approved____GNU_General_Public_License_v2_or_later_GPLv2plus = (
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)"
    )
    License____OSI_Approved____GNU_General_Public_License_v3_GPLv3 = (
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    )
    License____OSI_Approved____GNU_General_Public_License_v3_or_later_GPLv3plus = (
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    )
    License____OSI_Approved____GNU_Lesser_General_Public_License_v2_LGPLv2 = (
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)"
    )
    License____OSI_Approved____GNU_Lesser_General_Public_License_v2_or_later_LGPLv2plus = "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
    License____OSI_Approved____GNU_Lesser_General_Public_License_v3_LGPLv3 = (
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    )
    License____OSI_Approved____GNU_Lesser_General_Public_License_v3_or_later_LGPLv3plus = "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    License____OSI_Approved____GNU_Library_or_Lesser_General_Public_License_LGPL = (
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)"
    )
    License____OSI_Approved____Historical_Permission_Notice_and_Disclaimer_HPND = (
        "License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)"
    )
    License____OSI_Approved____IBM_Public_License = (
        "License :: OSI Approved :: IBM Public License"
    )
    License____OSI_Approved____ISC_License_ISCL = (
        "License :: OSI Approved :: ISC License (ISCL)"
    )
    License____OSI_Approved____Intel_Open_Source_License = (
        "License :: OSI Approved :: Intel Open Source License"
    )
    License____OSI_Approved____Jabber_Open_Source_License = (
        "License :: OSI Approved :: Jabber Open Source License"
    )
    License____OSI_Approved____MIT_License = "License :: OSI Approved :: MIT License"
    License____OSI_Approved____MIT_No_Attribution_License_MIT_0 = (
        "License :: OSI Approved :: MIT No Attribution License (MIT-0)"
    )
    License____OSI_Approved____MITRE_Collaborative_Virtual_Workspace_License_CVW = (
        "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)"
    )
    License____OSI_Approved____MirOS_License_MirOS = (
        "License :: OSI Approved :: MirOS License (MirOS)"
    )
    License____OSI_Approved____Motosoto_License = (
        "License :: OSI Approved :: Motosoto License"
    )
    License____OSI_Approved____Mozilla_Public_License_1_0_MPL = (
        "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)"
    )
    License____OSI_Approved____Mozilla_Public_License_1_1_MPL_1_1 = (
        "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)"
    )
    License____OSI_Approved____Mozilla_Public_License_2_0_MPL_2_0 = (
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
    )
    License____OSI_Approved____Mulan_Permissive_Software_License_v2_MulanPSL_2_0 = (
        "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)"
    )
    License____OSI_Approved____Nethack_General_Public_License = (
        "License :: OSI Approved :: Nethack General Public License"
    )
    License____OSI_Approved____Nokia_Open_Source_License = (
        "License :: OSI Approved :: Nokia Open Source License"
    )
    License____OSI_Approved____Open_Group_Test_Suite_License = (
        "License :: OSI Approved :: Open Group Test Suite License"
    )
    License____OSI_Approved____Open_Software_License_3_0_OSL_3_0 = (
        "License :: OSI Approved :: Open Software License 3.0 (OSL-3.0)"
    )
    License____OSI_Approved____PostgreSQL_License = (
        "License :: OSI Approved :: PostgreSQL License"
    )
    License____OSI_Approved____Python_License_CNRI_Python_License = (
        "License :: OSI Approved :: Python License (CNRI Python License)"
    )
    License____OSI_Approved____Python_Software_Foundation_License = (
        "License :: OSI Approved :: Python Software Foundation License"
    )
    License____OSI_Approved____Qt_Public_License_QPL = (
        "License :: OSI Approved :: Qt Public License (QPL)"
    )
    License____OSI_Approved____Ricoh_Source_Code_Public_License = (
        "License :: OSI Approved :: Ricoh Source Code Public License"
    )
    License____OSI_Approved____SIL_Open_Font_License_1_1_OFL_1_1 = (
        "License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)"
    )
    License____OSI_Approved____Sleepycat_License = (
        "License :: OSI Approved :: Sleepycat License"
    )
    License____OSI_Approved____Sun_Industry_Standards_Source_License_SISSL = (
        "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)"
    )
    License____OSI_Approved____Sun_Public_License = (
        "License :: OSI Approved :: Sun Public License"
    )
    License____OSI_Approved____The_Unlicense_Unlicense = (
        "License :: OSI Approved :: The Unlicense (Unlicense)"
    )
    License____OSI_Approved____Universal_Permissive_License_UPL = (
        "License :: OSI Approved :: Universal Permissive License (UPL)"
    )
    License____OSI_Approved____University_of_Illinois_NCSA_Open_Source_License = (
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License"
    )
    License____OSI_Approved____Vovida_Software_License_1_0 = (
        "License :: OSI Approved :: Vovida Software License 1.0"
    )
    License____OSI_Approved____W3C_License = "License :: OSI Approved :: W3C License"
    License____OSI_Approved____X_Net_License = (
        "License :: OSI Approved :: X.Net License"
    )
    License____OSI_Approved____Zope_Public_License = (
        "License :: OSI Approved :: Zope Public License"
    )
    License____OSI_Approved____zlib_libpng_License = (
        "License :: OSI Approved :: zlib/libpng License"
    )
    License____Other_Proprietary_License = "License :: Other/Proprietary License"
    License____Public_Domain = "License :: Public Domain"
    License____Repoze_Public_License = "License :: Repoze Public License"
    Natural_Language____Afrikaans = "Natural Language :: Afrikaans"
    Natural_Language____Arabic = "Natural Language :: Arabic"
    Natural_Language____Basque = "Natural Language :: Basque"
    Natural_Language____Bengali = "Natural Language :: Bengali"
    Natural_Language____Bosnian = "Natural Language :: Bosnian"
    Natural_Language____Bulgarian = "Natural Language :: Bulgarian"
    Natural_Language____Cantonese = "Natural Language :: Cantonese"
    Natural_Language____Catalan = "Natural Language :: Catalan"
    Natural_Language____Chinese_Simplified = "Natural Language :: Chinese (Simplified)"
    Natural_Language____Chinese_Traditional = (
        "Natural Language :: Chinese (Traditional)"
    )
    Natural_Language____Croatian = "Natural Language :: Croatian"
    Natural_Language____Czech = "Natural Language :: Czech"
    Natural_Language____Danish = "Natural Language :: Danish"
    Natural_Language____Dutch = "Natural Language :: Dutch"
    Natural_Language____English = "Natural Language :: English"
    Natural_Language____Esperanto = "Natural Language :: Esperanto"
    Natural_Language____Finnish = "Natural Language :: Finnish"
    Natural_Language____French = "Natural Language :: French"
    Natural_Language____Galician = "Natural Language :: Galician"
    Natural_Language____German = "Natural Language :: German"
    Natural_Language____Greek = "Natural Language :: Greek"
    Natural_Language____Hebrew = "Natural Language :: Hebrew"
    Natural_Language____Hindi = "Natural Language :: Hindi"
    Natural_Language____Hungarian = "Natural Language :: Hungarian"
    Natural_Language____Icelandic = "Natural Language :: Icelandic"
    Natural_Language____Indonesian = "Natural Language :: Indonesian"
    Natural_Language____Irish = "Natural Language :: Irish"
    Natural_Language____Italian = "Natural Language :: Italian"
    Natural_Language____Japanese = "Natural Language :: Japanese"
    Natural_Language____Javanese = "Natural Language :: Javanese"
    Natural_Language____Korean = "Natural Language :: Korean"
    Natural_Language____Latin = "Natural Language :: Latin"
    Natural_Language____Latvian = "Natural Language :: Latvian"
    Natural_Language____Lithuanian = "Natural Language :: Lithuanian"
    Natural_Language____Macedonian = "Natural Language :: Macedonian"
    Natural_Language____Malay = "Natural Language :: Malay"
    Natural_Language____Marathi = "Natural Language :: Marathi"
    Natural_Language____Nepali = "Natural Language :: Nepali"
    Natural_Language____Norwegian = "Natural Language :: Norwegian"
    Natural_Language____Panjabi = "Natural Language :: Panjabi"
    Natural_Language____Persian = "Natural Language :: Persian"
    Natural_Language____Polish = "Natural Language :: Polish"
    Natural_Language____Portuguese = "Natural Language :: Portuguese"
    Natural_Language____Portuguese_Brazilian = (
        "Natural Language :: Portuguese (Brazilian)"
    )
    Natural_Language____Romanian = "Natural Language :: Romanian"
    Natural_Language____Russian = "Natural Language :: Russian"
    Natural_Language____Serbian = "Natural Language :: Serbian"
    Natural_Language____Slovak = "Natural Language :: Slovak"
    Natural_Language____Slovenian = "Natural Language :: Slovenian"
    Natural_Language____Spanish = "Natural Language :: Spanish"
    Natural_Language____Swedish = "Natural Language :: Swedish"
    Natural_Language____Tamil = "Natural Language :: Tamil"
    Natural_Language____Telugu = "Natural Language :: Telugu"
    Natural_Language____Thai = "Natural Language :: Thai"
    Natural_Language____Tibetan = "Natural Language :: Tibetan"
    Natural_Language____Turkish = "Natural Language :: Turkish"
    Natural_Language____Ukrainian = "Natural Language :: Ukrainian"
    Natural_Language____Urdu = "Natural Language :: Urdu"
    Natural_Language____Vietnamese = "Natural Language :: Vietnamese"
    Operating_System____Android = "Operating System :: Android"
    Operating_System____BeOS = "Operating System :: BeOS"
    Operating_System____MacOS = "Operating System :: MacOS"
    Operating_System____MacOS____MacOS_9 = "Operating System :: MacOS :: MacOS 9"
    Operating_System____MacOS____MacOS_X = "Operating System :: MacOS :: MacOS X"
    Operating_System____Microsoft = "Operating System :: Microsoft"
    Operating_System____Microsoft____MS_DOS = "Operating System :: Microsoft :: MS-DOS"
    Operating_System____Microsoft____Windows = (
        "Operating System :: Microsoft :: Windows"
    )
    Operating_System____Microsoft____Windows____Windows_10 = (
        "Operating System :: Microsoft :: Windows :: Windows 10"
    )
    Operating_System____Microsoft____Windows____Windows_11 = (
        "Operating System :: Microsoft :: Windows :: Windows 11"
    )
    Operating_System____Microsoft____Windows____Windows_3_1_or_Earlier = (
        "Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier"
    )
    Operating_System____Microsoft____Windows____Windows_7 = (
        "Operating System :: Microsoft :: Windows :: Windows 7"
    )
    Operating_System____Microsoft____Windows____Windows_8 = (
        "Operating System :: Microsoft :: Windows :: Windows 8"
    )
    Operating_System____Microsoft____Windows____Windows_8_1 = (
        "Operating System :: Microsoft :: Windows :: Windows 8.1"
    )
    Operating_System____Microsoft____Windows____Windows_95_98_2000 = (
        "Operating System :: Microsoft :: Windows :: Windows 95/98/2000"
    )
    Operating_System____Microsoft____Windows____Windows_CE = (
        "Operating System :: Microsoft :: Windows :: Windows CE"
    )
    Operating_System____Microsoft____Windows____Windows_NT_2000 = (
        "Operating System :: Microsoft :: Windows :: Windows NT/2000"
    )
    Operating_System____Microsoft____Windows____Windows_Server_2003 = (
        "Operating System :: Microsoft :: Windows :: Windows Server 2003"
    )
    Operating_System____Microsoft____Windows____Windows_Server_2008 = (
        "Operating System :: Microsoft :: Windows :: Windows Server 2008"
    )
    Operating_System____Microsoft____Windows____Windows_Vista = (
        "Operating System :: Microsoft :: Windows :: Windows Vista"
    )
    Operating_System____Microsoft____Windows____Windows_XP = (
        "Operating System :: Microsoft :: Windows :: Windows XP"
    )
    Operating_System____OS_Independent = "Operating System :: OS Independent"
    Operating_System____OS_2 = "Operating System :: OS/2"
    Operating_System____Other_OS = "Operating System :: Other OS"
    Operating_System____PDA_Systems = "Operating System :: PDA Systems"
    Operating_System____POSIX = "Operating System :: POSIX"
    Operating_System____POSIX____AIX = "Operating System :: POSIX :: AIX"
    Operating_System____POSIX____BSD = "Operating System :: POSIX :: BSD"
    Operating_System____POSIX____BSD____BSD_OS = (
        "Operating System :: POSIX :: BSD :: BSD/OS"
    )
    Operating_System____POSIX____BSD____FreeBSD = (
        "Operating System :: POSIX :: BSD :: FreeBSD"
    )
    Operating_System____POSIX____BSD____NetBSD = (
        "Operating System :: POSIX :: BSD :: NetBSD"
    )
    Operating_System____POSIX____BSD____OpenBSD = (
        "Operating System :: POSIX :: BSD :: OpenBSD"
    )
    Operating_System____POSIX____GNU_Hurd = "Operating System :: POSIX :: GNU Hurd"
    Operating_System____POSIX____HP_UX = "Operating System :: POSIX :: HP-UX"
    Operating_System____POSIX____IRIX = "Operating System :: POSIX :: IRIX"
    Operating_System____POSIX____Linux = "Operating System :: POSIX :: Linux"
    Operating_System____POSIX____Other = "Operating System :: POSIX :: Other"
    Operating_System____POSIX____SCO = "Operating System :: POSIX :: SCO"
    Operating_System____POSIX____SunOS_Solaris = (
        "Operating System :: POSIX :: SunOS/Solaris"
    )
    Operating_System____PalmOS = "Operating System :: PalmOS"
    Operating_System____RISC_OS = "Operating System :: RISC OS"
    Operating_System____Unix = "Operating System :: Unix"
    Operating_System____iOS = "Operating System :: iOS"
    Programming_Language____APL = "Programming Language :: APL"
    Programming_Language____ASP = "Programming Language :: ASP"
    Programming_Language____Ada = "Programming Language :: Ada"
    Programming_Language____Assembly = "Programming Language :: Assembly"
    Programming_Language____Awk = "Programming Language :: Awk"
    Programming_Language____Basic = "Programming Language :: Basic"
    Programming_Language____C = "Programming Language :: C"
    Programming_Language____CSharp = "Programming Language :: C#"
    Programming_Language____CPP = "Programming Language :: C++"
    Programming_Language____Cold_Fusion = "Programming Language :: Cold Fusion"
    Programming_Language____Cython = "Programming Language :: Cython"
    Programming_Language____D = "Programming Language :: D"
    Programming_Language____Delphi_Kylix = "Programming Language :: Delphi/Kylix"
    Programming_Language____Dylan = "Programming Language :: Dylan"
    Programming_Language____Eiffel = "Programming Language :: Eiffel"
    Programming_Language____Emacs_Lisp = "Programming Language :: Emacs-Lisp"
    Programming_Language____Erlang = "Programming Language :: Erlang"
    Programming_Language____Euler = "Programming Language :: Euler"
    Programming_Language____Euphoria = "Programming Language :: Euphoria"
    Programming_Language____FSharp = "Programming Language :: F#"
    Programming_Language____Forth = "Programming Language :: Forth"
    Programming_Language____Fortran = "Programming Language :: Fortran"
    Programming_Language____Haskell = "Programming Language :: Haskell"
    Programming_Language____Java = "Programming Language :: Java"
    Programming_Language____JavaScript = "Programming Language :: JavaScript"
    Programming_Language____Kotlin = "Programming Language :: Kotlin"
    Programming_Language____Lisp = "Programming Language :: Lisp"
    Programming_Language____Logo = "Programming Language :: Logo"
    Programming_Language____ML = "Programming Language :: ML"
    Programming_Language____Modula = "Programming Language :: Modula"
    Programming_Language____OCaml = "Programming Language :: OCaml"
    Programming_Language____Object_Pascal = "Programming Language :: Object Pascal"
    Programming_Language____Objective_C = "Programming Language :: Objective C"
    Programming_Language____Other = "Programming Language :: Other"
    Programming_Language____Other_Scripting_Engines = (
        "Programming Language :: Other Scripting Engines"
    )
    Programming_Language____PHP = "Programming Language :: PHP"
    Programming_Language____PL_SQL = "Programming Language :: PL/SQL"
    Programming_Language____PROGRESS = "Programming Language :: PROGRESS"
    Programming_Language____Pascal = "Programming Language :: Pascal"
    Programming_Language____Perl = "Programming Language :: Perl"
    Programming_Language____Pike = "Programming Language :: Pike"
    Programming_Language____Pliant = "Programming Language :: Pliant"
    Programming_Language____Prolog = "Programming Language :: Prolog"
    Programming_Language____Python = "Programming Language :: Python"
    Programming_Language____Python____2 = "Programming Language :: Python :: 2"
    Programming_Language____Python____2____Only = (
        "Programming Language :: Python :: 2 :: Only"
    )
    Programming_Language____Python____2_3 = "Programming Language :: Python :: 2.3"
    Programming_Language____Python____2_4 = "Programming Language :: Python :: 2.4"
    Programming_Language____Python____2_5 = "Programming Language :: Python :: 2.5"
    Programming_Language____Python____2_6 = "Programming Language :: Python :: 2.6"
    Programming_Language____Python____2_7 = "Programming Language :: Python :: 2.7"
    Programming_Language____Python____3 = "Programming Language :: Python :: 3"
    Programming_Language____Python____3____Only = (
        "Programming Language :: Python :: 3 :: Only"
    )
    Programming_Language____Python____3_0 = "Programming Language :: Python :: 3.0"
    Programming_Language____Python____3_1 = "Programming Language :: Python :: 3.1"
    Programming_Language____Python____3_10 = "Programming Language :: Python :: 3.10"
    Programming_Language____Python____3_11 = "Programming Language :: Python :: 3.11"
    Programming_Language____Python____3_12 = "Programming Language :: Python :: 3.12"
    Programming_Language____Python____3_2 = "Programming Language :: Python :: 3.2"
    Programming_Language____Python____3_3 = "Programming Language :: Python :: 3.3"
    Programming_Language____Python____3_4 = "Programming Language :: Python :: 3.4"
    Programming_Language____Python____3_5 = "Programming Language :: Python :: 3.5"
    Programming_Language____Python____3_6 = "Programming Language :: Python :: 3.6"
    Programming_Language____Python____3_7 = "Programming Language :: Python :: 3.7"
    Programming_Language____Python____3_8 = "Programming Language :: Python :: 3.8"
    Programming_Language____Python____3_9 = "Programming Language :: Python :: 3.9"
    Programming_Language____Python____Implementation = (
        "Programming Language :: Python :: Implementation"
    )
    Programming_Language____Python____Implementation____CPython = (
        "Programming Language :: Python :: Implementation :: CPython"
    )
    Programming_Language____Python____Implementation____IronPython = (
        "Programming Language :: Python :: Implementation :: IronPython"
    )
    Programming_Language____Python____Implementation____Jython = (
        "Programming Language :: Python :: Implementation :: Jython"
    )
    Programming_Language____Python____Implementation____MicroPython = (
        "Programming Language :: Python :: Implementation :: MicroPython"
    )
    Programming_Language____Python____Implementation____PyPy = (
        "Programming Language :: Python :: Implementation :: PyPy"
    )
    Programming_Language____Python____Implementation____Stackless = (
        "Programming Language :: Python :: Implementation :: Stackless"
    )
    Programming_Language____R = "Programming Language :: R"
    Programming_Language____REBOL = "Programming Language :: REBOL"
    Programming_Language____Rexx = "Programming Language :: Rexx"
    Programming_Language____Ruby = "Programming Language :: Ruby"
    Programming_Language____Rust = "Programming Language :: Rust"
    Programming_Language____SQL = "Programming Language :: SQL"
    Programming_Language____Scheme = "Programming Language :: Scheme"
    Programming_Language____Simula = "Programming Language :: Simula"
    Programming_Language____Smalltalk = "Programming Language :: Smalltalk"
    Programming_Language____Tcl = "Programming Language :: Tcl"
    Programming_Language____Unix_Shell = "Programming Language :: Unix Shell"
    Programming_Language____Visual_Basic = "Programming Language :: Visual Basic"
    Programming_Language____XBasic = "Programming Language :: XBasic"
    Programming_Language____YACC = "Programming Language :: YACC"
    Programming_Language____Zope = "Programming Language :: Zope"
    Topic____Adaptive_Technologies = "Topic :: Adaptive Technologies"
    Topic____Artistic_Software = "Topic :: Artistic Software"
    Topic____Communications = "Topic :: Communications"
    Topic____Communications____BBS = "Topic :: Communications :: BBS"
    Topic____Communications____Chat = "Topic :: Communications :: Chat"
    Topic____Communications____Chat____ICQ = "Topic :: Communications :: Chat :: ICQ"
    Topic____Communications____Chat____Internet_Relay_Chat = (
        "Topic :: Communications :: Chat :: Internet Relay Chat"
    )
    Topic____Communications____Chat____Unix_Talk = (
        "Topic :: Communications :: Chat :: Unix Talk"
    )
    Topic____Communications____Conferencing = "Topic :: Communications :: Conferencing"
    Topic____Communications____Email = "Topic :: Communications :: Email"
    Topic____Communications____Email____Address_Book = (
        "Topic :: Communications :: Email :: Address Book"
    )
    Topic____Communications____Email____Email_Clients_MUA = (
        "Topic :: Communications :: Email :: Email Clients (MUA)"
    )
    Topic____Communications____Email____Filters = (
        "Topic :: Communications :: Email :: Filters"
    )
    Topic____Communications____Email____Mail_Transport_Agents = (
        "Topic :: Communications :: Email :: Mail Transport Agents"
    )
    Topic____Communications____Email____Mailing_List_Servers = (
        "Topic :: Communications :: Email :: Mailing List Servers"
    )
    Topic____Communications____Email____Post_Office = (
        "Topic :: Communications :: Email :: Post-Office"
    )
    Topic____Communications____Email____Post_Office____IMAP = (
        "Topic :: Communications :: Email :: Post-Office :: IMAP"
    )
    Topic____Communications____Email____Post_Office____POP3 = (
        "Topic :: Communications :: Email :: Post-Office :: POP3"
    )
    Topic____Communications____FIDO = "Topic :: Communications :: FIDO"
    Topic____Communications____Fax = "Topic :: Communications :: Fax"
    Topic____Communications____File_Sharing = "Topic :: Communications :: File Sharing"
    Topic____Communications____File_Sharing____Gnutella = (
        "Topic :: Communications :: File Sharing :: Gnutella"
    )
    Topic____Communications____File_Sharing____Napster = (
        "Topic :: Communications :: File Sharing :: Napster"
    )
    Topic____Communications____Ham_Radio = "Topic :: Communications :: Ham Radio"
    Topic____Communications____Internet_Phone = (
        "Topic :: Communications :: Internet Phone"
    )
    Topic____Communications____Telephony = "Topic :: Communications :: Telephony"
    Topic____Communications____Usenet_News = "Topic :: Communications :: Usenet News"
    Topic____Database = "Topic :: Database"
    Topic____Database____Database_Engines_Servers = (
        "Topic :: Database :: Database Engines/Servers"
    )
    Topic____Database____Front_Ends = "Topic :: Database :: Front-Ends"
    Topic____Desktop_Environment = "Topic :: Desktop Environment"
    Topic____Desktop_Environment____File_Managers = (
        "Topic :: Desktop Environment :: File Managers"
    )
    Topic____Desktop_Environment____GNUstep = "Topic :: Desktop Environment :: GNUstep"
    Topic____Desktop_Environment____Gnome = "Topic :: Desktop Environment :: Gnome"
    Topic____Desktop_Environment____K_Desktop_Environment_KDE = (
        "Topic :: Desktop Environment :: K Desktop Environment (KDE)"
    )
    Topic____Desktop_Environment____K_Desktop_Environment_KDE____Themes = (
        "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes"
    )
    Topic____Desktop_Environment____PicoGUI = "Topic :: Desktop Environment :: PicoGUI"
    Topic____Desktop_Environment____PicoGUI____Applications = (
        "Topic :: Desktop Environment :: PicoGUI :: Applications"
    )
    Topic____Desktop_Environment____PicoGUI____Themes = (
        "Topic :: Desktop Environment :: PicoGUI :: Themes"
    )
    Topic____Desktop_Environment____Screen_Savers = (
        "Topic :: Desktop Environment :: Screen Savers"
    )
    Topic____Desktop_Environment____Window_Managers = (
        "Topic :: Desktop Environment :: Window Managers"
    )
    Topic____Desktop_Environment____Window_Managers____Afterstep = (
        "Topic :: Desktop Environment :: Window Managers :: Afterstep"
    )
    Topic____Desktop_Environment____Window_Managers____Afterstep____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: Afterstep :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____Applets = (
        "Topic :: Desktop Environment :: Window Managers :: Applets"
    )
    Topic____Desktop_Environment____Window_Managers____Blackbox = (
        "Topic :: Desktop Environment :: Window Managers :: Blackbox"
    )
    Topic____Desktop_Environment____Window_Managers____Blackbox____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: Blackbox :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____CTWM = (
        "Topic :: Desktop Environment :: Window Managers :: CTWM"
    )
    Topic____Desktop_Environment____Window_Managers____CTWM____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: CTWM :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____Enlightenment = (
        "Topic :: Desktop Environment :: Window Managers :: Enlightenment"
    )
    Topic____Desktop_Environment____Window_Managers____Enlightenment____Epplets = (
        "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Epplets"
    )
    Topic____Desktop_Environment____Window_Managers____Enlightenment____Themes_DR15 = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR15"
    Topic____Desktop_Environment____Window_Managers____Enlightenment____Themes_DR16 = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR16"
    Topic____Desktop_Environment____Window_Managers____Enlightenment____Themes_DR17 = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR17"
    Topic____Desktop_Environment____Window_Managers____FVWM = (
        "Topic :: Desktop Environment :: Window Managers :: FVWM"
    )
    Topic____Desktop_Environment____Window_Managers____FVWM____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: FVWM :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____Fluxbox = (
        "Topic :: Desktop Environment :: Window Managers :: Fluxbox"
    )
    Topic____Desktop_Environment____Window_Managers____Fluxbox____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: Fluxbox :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____IceWM = (
        "Topic :: Desktop Environment :: Window Managers :: IceWM"
    )
    Topic____Desktop_Environment____Window_Managers____IceWM____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: IceWM :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____MetaCity = (
        "Topic :: Desktop Environment :: Window Managers :: MetaCity"
    )
    Topic____Desktop_Environment____Window_Managers____MetaCity____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: MetaCity :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____Oroborus = (
        "Topic :: Desktop Environment :: Window Managers :: Oroborus"
    )
    Topic____Desktop_Environment____Window_Managers____Oroborus____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: Oroborus :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____Sawfish = (
        "Topic :: Desktop Environment :: Window Managers :: Sawfish"
    )
    Topic____Desktop_Environment____Window_Managers____Sawfish____Themes_0_30 = (
        "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes 0.30"
    )
    Topic____Desktop_Environment____Window_Managers____Sawfish____Themes_pre_0_30 = (
        "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes pre-0.30"
    )
    Topic____Desktop_Environment____Window_Managers____Waimea = (
        "Topic :: Desktop Environment :: Window Managers :: Waimea"
    )
    Topic____Desktop_Environment____Window_Managers____Waimea____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: Waimea :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____Window_Maker = (
        "Topic :: Desktop Environment :: Window Managers :: Window Maker"
    )
    Topic____Desktop_Environment____Window_Managers____Window_Maker____Applets = (
        "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Applets"
    )
    Topic____Desktop_Environment____Window_Managers____Window_Maker____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Themes"
    )
    Topic____Desktop_Environment____Window_Managers____XFCE = (
        "Topic :: Desktop Environment :: Window Managers :: XFCE"
    )
    Topic____Desktop_Environment____Window_Managers____XFCE____Themes = (
        "Topic :: Desktop Environment :: Window Managers :: XFCE :: Themes"
    )
    Topic____Documentation = "Topic :: Documentation"
    Topic____Documentation____Sphinx = "Topic :: Documentation :: Sphinx"
    Topic____Education = "Topic :: Education"
    Topic____Education____Computer_Aided_Instruction_CAI = (
        "Topic :: Education :: Computer Aided Instruction (CAI)"
    )
    Topic____Education____Testing = "Topic :: Education :: Testing"
    Topic____Games_Entertainment = "Topic :: Games/Entertainment"
    Topic____Games_Entertainment____Arcade = "Topic :: Games/Entertainment :: Arcade"
    Topic____Games_Entertainment____Board_Games = (
        "Topic :: Games/Entertainment :: Board Games"
    )
    Topic____Games_Entertainment____First_Person_Shooters = (
        "Topic :: Games/Entertainment :: First Person Shooters"
    )
    Topic____Games_Entertainment____Fortune_Cookies = (
        "Topic :: Games/Entertainment :: Fortune Cookies"
    )
    Topic____Games_Entertainment____Multi_User_Dungeons_MUD = (
        "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)"
    )
    Topic____Games_Entertainment____Puzzle_Games = (
        "Topic :: Games/Entertainment :: Puzzle Games"
    )
    Topic____Games_Entertainment____Real_Time_Strategy = (
        "Topic :: Games/Entertainment :: Real Time Strategy"
    )
    Topic____Games_Entertainment____Role_Playing = (
        "Topic :: Games/Entertainment :: Role-Playing"
    )
    Topic____Games_Entertainment____Side_Scrolling_Arcade_Games = (
        "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games"
    )
    Topic____Games_Entertainment____Simulation = (
        "Topic :: Games/Entertainment :: Simulation"
    )
    Topic____Games_Entertainment____Turn_Based_Strategy = (
        "Topic :: Games/Entertainment :: Turn Based Strategy"
    )
    Topic____Home_Automation = "Topic :: Home Automation"
    Topic____Internet = "Topic :: Internet"
    Topic____Internet____File_Transfer_Protocol_FTP = (
        "Topic :: Internet :: File Transfer Protocol (FTP)"
    )
    Topic____Internet____Finger = "Topic :: Internet :: Finger"
    Topic____Internet____Log_Analysis = "Topic :: Internet :: Log Analysis"
    Topic____Internet____Name_Service_DNS = "Topic :: Internet :: Name Service (DNS)"
    Topic____Internet____Proxy_Servers = "Topic :: Internet :: Proxy Servers"
    Topic____Internet____WAP = "Topic :: Internet :: WAP"
    Topic____Internet____WWW_HTTP = "Topic :: Internet :: WWW/HTTP"
    Topic____Internet____WWW_HTTP____Browsers = (
        "Topic :: Internet :: WWW/HTTP :: Browsers"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content____CGI_Tools_Libraries = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content____Content_Management_System = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content____Message_Boards = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content____News_Diary = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content____Page_Counters = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters"
    )
    Topic____Internet____WWW_HTTP____Dynamic_Content____Wiki = (
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki"
    )
    Topic____Internet____WWW_HTTP____HTTP_Servers = (
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
    )
    Topic____Internet____WWW_HTTP____Indexing_Search = (
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
    )
    Topic____Internet____WWW_HTTP____Session = (
        "Topic :: Internet :: WWW/HTTP :: Session"
    )
    Topic____Internet____WWW_HTTP____Site_Management = (
        "Topic :: Internet :: WWW/HTTP :: Site Management"
    )
    Topic____Internet____WWW_HTTP____Site_Management____Link_Checking = (
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking"
    )
    Topic____Internet____WWW_HTTP____WSGI = "Topic :: Internet :: WWW/HTTP :: WSGI"
    Topic____Internet____WWW_HTTP____WSGI____Application = (
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    )
    Topic____Internet____WWW_HTTP____WSGI____Middleware = (
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware"
    )
    Topic____Internet____WWW_HTTP____WSGI____Server = (
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server"
    )
    Topic____Internet____XMPP = "Topic :: Internet :: XMPP"
    Topic____Internet____Z39_50 = "Topic :: Internet :: Z39.50"
    Topic____Multimedia = "Topic :: Multimedia"
    Topic____Multimedia____Graphics = "Topic :: Multimedia :: Graphics"
    Topic____Multimedia____Graphics____3D_Modeling = (
        "Topic :: Multimedia :: Graphics :: 3D Modeling"
    )
    Topic____Multimedia____Graphics____3D_Rendering = (
        "Topic :: Multimedia :: Graphics :: 3D Rendering"
    )
    Topic____Multimedia____Graphics____Capture = (
        "Topic :: Multimedia :: Graphics :: Capture"
    )
    Topic____Multimedia____Graphics____Capture____Digital_Camera = (
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera"
    )
    Topic____Multimedia____Graphics____Capture____Scanners = (
        "Topic :: Multimedia :: Graphics :: Capture :: Scanners"
    )
    Topic____Multimedia____Graphics____Capture____Screen_Capture = (
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture"
    )
    Topic____Multimedia____Graphics____Editors = (
        "Topic :: Multimedia :: Graphics :: Editors"
    )
    Topic____Multimedia____Graphics____Editors____Raster_Based = (
        "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based"
    )
    Topic____Multimedia____Graphics____Editors____Vector_Based = (
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based"
    )
    Topic____Multimedia____Graphics____Graphics_Conversion = (
        "Topic :: Multimedia :: Graphics :: Graphics Conversion"
    )
    Topic____Multimedia____Graphics____Presentation = (
        "Topic :: Multimedia :: Graphics :: Presentation"
    )
    Topic____Multimedia____Graphics____Viewers = (
        "Topic :: Multimedia :: Graphics :: Viewers"
    )
    Topic____Multimedia____Sound_Audio = "Topic :: Multimedia :: Sound/Audio"
    Topic____Multimedia____Sound_Audio____Analysis = (
        "Topic :: Multimedia :: Sound/Audio :: Analysis"
    )
    Topic____Multimedia____Sound_Audio____CD_Audio = (
        "Topic :: Multimedia :: Sound/Audio :: CD Audio"
    )
    Topic____Multimedia____Sound_Audio____CD_Audio____CD_Playing = (
        "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing"
    )
    Topic____Multimedia____Sound_Audio____CD_Audio____CD_Ripping = (
        "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping"
    )
    Topic____Multimedia____Sound_Audio____CD_Audio____CD_Writing = (
        "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing"
    )
    Topic____Multimedia____Sound_Audio____Capture_Recording = (
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording"
    )
    Topic____Multimedia____Sound_Audio____Conversion = (
        "Topic :: Multimedia :: Sound/Audio :: Conversion"
    )
    Topic____Multimedia____Sound_Audio____Editors = (
        "Topic :: Multimedia :: Sound/Audio :: Editors"
    )
    Topic____Multimedia____Sound_Audio____MIDI = (
        "Topic :: Multimedia :: Sound/Audio :: MIDI"
    )
    Topic____Multimedia____Sound_Audio____Mixers = (
        "Topic :: Multimedia :: Sound/Audio :: Mixers"
    )
    Topic____Multimedia____Sound_Audio____Players = (
        "Topic :: Multimedia :: Sound/Audio :: Players"
    )
    Topic____Multimedia____Sound_Audio____Players____MP3 = (
        "Topic :: Multimedia :: Sound/Audio :: Players :: MP3"
    )
    Topic____Multimedia____Sound_Audio____Sound_Synthesis = (
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis"
    )
    Topic____Multimedia____Sound_Audio____Speech = (
        "Topic :: Multimedia :: Sound/Audio :: Speech"
    )
    Topic____Multimedia____Video = "Topic :: Multimedia :: Video"
    Topic____Multimedia____Video____Capture = "Topic :: Multimedia :: Video :: Capture"
    Topic____Multimedia____Video____Conversion = (
        "Topic :: Multimedia :: Video :: Conversion"
    )
    Topic____Multimedia____Video____Display = "Topic :: Multimedia :: Video :: Display"
    Topic____Multimedia____Video____Non_Linear_Editor = (
        "Topic :: Multimedia :: Video :: Non-Linear Editor"
    )
    Topic____Office_Business = "Topic :: Office/Business"
    Topic____Office_Business____Financial = "Topic :: Office/Business :: Financial"
    Topic____Office_Business____Financial____Accounting = (
        "Topic :: Office/Business :: Financial :: Accounting"
    )
    Topic____Office_Business____Financial____Investment = (
        "Topic :: Office/Business :: Financial :: Investment"
    )
    Topic____Office_Business____Financial____Point_Of_Sale = (
        "Topic :: Office/Business :: Financial :: Point-Of-Sale"
    )
    Topic____Office_Business____Financial____Spreadsheet = (
        "Topic :: Office/Business :: Financial :: Spreadsheet"
    )
    Topic____Office_Business____Groupware = "Topic :: Office/Business :: Groupware"
    Topic____Office_Business____News_Diary = "Topic :: Office/Business :: News/Diary"
    Topic____Office_Business____Office_Suites = (
        "Topic :: Office/Business :: Office Suites"
    )
    Topic____Office_Business____Scheduling = "Topic :: Office/Business :: Scheduling"
    Topic____Other_Nonlisted_Topic = "Topic :: Other/Nonlisted Topic"
    Topic____Printing = "Topic :: Printing"
    Topic____Religion = "Topic :: Religion"
    Topic____Scientific_Engineering = "Topic :: Scientific/Engineering"
    Topic____Scientific_Engineering____Artificial_Intelligence = (
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    )
    Topic____Scientific_Engineering____Artificial_Life = (
        "Topic :: Scientific/Engineering :: Artificial Life"
    )
    Topic____Scientific_Engineering____Astronomy = (
        "Topic :: Scientific/Engineering :: Astronomy"
    )
    Topic____Scientific_Engineering____Atmospheric_Science = (
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    )
    Topic____Scientific_Engineering____Bio_Informatics = (
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    )
    Topic____Scientific_Engineering____Chemistry = (
        "Topic :: Scientific/Engineering :: Chemistry"
    )
    Topic____Scientific_Engineering____Electronic_Design_Automation_EDA = (
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    )
    Topic____Scientific_Engineering____GIS = "Topic :: Scientific/Engineering :: GIS"
    Topic____Scientific_Engineering____Human_Machine_Interfaces = (
        "Topic :: Scientific/Engineering :: Human Machine Interfaces"
    )
    Topic____Scientific_Engineering____Hydrology = (
        "Topic :: Scientific/Engineering :: Hydrology"
    )
    Topic____Scientific_Engineering____Image_Processing = (
        "Topic :: Scientific/Engineering :: Image Processing"
    )
    Topic____Scientific_Engineering____Image_Recognition = (
        "Topic :: Scientific/Engineering :: Image Recognition"
    )
    Topic____Scientific_Engineering____Information_Analysis = (
        "Topic :: Scientific/Engineering :: Information Analysis"
    )
    Topic____Scientific_Engineering____Interface_Engine_Protocol_Translator = (
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
    )
    Topic____Scientific_Engineering____Mathematics = (
        "Topic :: Scientific/Engineering :: Mathematics"
    )
    Topic____Scientific_Engineering____Medical_Science_Apps_ = (
        "Topic :: Scientific/Engineering :: Medical Science Apps."
    )
    Topic____Scientific_Engineering____Physics = (
        "Topic :: Scientific/Engineering :: Physics"
    )
    Topic____Scientific_Engineering____Visualization = (
        "Topic :: Scientific/Engineering :: Visualization"
    )
    Topic____Security = "Topic :: Security"
    Topic____Security____Cryptography = "Topic :: Security :: Cryptography"
    Topic____Sociology = "Topic :: Sociology"
    Topic____Sociology____Genealogy = "Topic :: Sociology :: Genealogy"
    Topic____Sociology____History = "Topic :: Sociology :: History"
    Topic____Software_Development = "Topic :: Software Development"
    Topic____Software_Development____Assemblers = (
        "Topic :: Software Development :: Assemblers"
    )
    Topic____Software_Development____Bug_Tracking = (
        "Topic :: Software Development :: Bug Tracking"
    )
    Topic____Software_Development____Build_Tools = (
        "Topic :: Software Development :: Build Tools"
    )
    Topic____Software_Development____Code_Generators = (
        "Topic :: Software Development :: Code Generators"
    )
    Topic____Software_Development____Compilers = (
        "Topic :: Software Development :: Compilers"
    )
    Topic____Software_Development____Debuggers = (
        "Topic :: Software Development :: Debuggers"
    )
    Topic____Software_Development____Disassemblers = (
        "Topic :: Software Development :: Disassemblers"
    )
    Topic____Software_Development____Documentation = (
        "Topic :: Software Development :: Documentation"
    )
    Topic____Software_Development____Embedded_Systems = (
        "Topic :: Software Development :: Embedded Systems"
    )
    Topic____Software_Development____Internationalization = (
        "Topic :: Software Development :: Internationalization"
    )
    Topic____Software_Development____Interpreters = (
        "Topic :: Software Development :: Interpreters"
    )
    Topic____Software_Development____Libraries = (
        "Topic :: Software Development :: Libraries"
    )
    Topic____Software_Development____Libraries____Application_Frameworks = (
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    )
    Topic____Software_Development____Libraries____Java_Libraries = (
        "Topic :: Software Development :: Libraries :: Java Libraries"
    )
    Topic____Software_Development____Libraries____PHP_Classes = (
        "Topic :: Software Development :: Libraries :: PHP Classes"
    )
    Topic____Software_Development____Libraries____Perl_Modules = (
        "Topic :: Software Development :: Libraries :: Perl Modules"
    )
    Topic____Software_Development____Libraries____Pike_Modules = (
        "Topic :: Software Development :: Libraries :: Pike Modules"
    )
    Topic____Software_Development____Libraries____Python_Modules = (
        "Topic :: Software Development :: Libraries :: Python Modules"
    )
    Topic____Software_Development____Libraries____Ruby_Modules = (
        "Topic :: Software Development :: Libraries :: Ruby Modules"
    )
    Topic____Software_Development____Libraries____Tcl_Extensions = (
        "Topic :: Software Development :: Libraries :: Tcl Extensions"
    )
    Topic____Software_Development____Libraries____pygame = (
        "Topic :: Software Development :: Libraries :: pygame"
    )
    Topic____Software_Development____Localization = (
        "Topic :: Software Development :: Localization"
    )
    Topic____Software_Development____Object_Brokering = (
        "Topic :: Software Development :: Object Brokering"
    )
    Topic____Software_Development____Object_Brokering____CORBA = (
        "Topic :: Software Development :: Object Brokering :: CORBA"
    )
    Topic____Software_Development____Pre_processors = (
        "Topic :: Software Development :: Pre-processors"
    )
    Topic____Software_Development____Quality_Assurance = (
        "Topic :: Software Development :: Quality Assurance"
    )
    Topic____Software_Development____Testing = (
        "Topic :: Software Development :: Testing"
    )
    Topic____Software_Development____Testing____Acceptance = (
        "Topic :: Software Development :: Testing :: Acceptance"
    )
    Topic____Software_Development____Testing____BDD = (
        "Topic :: Software Development :: Testing :: BDD"
    )
    Topic____Software_Development____Testing____Mocking = (
        "Topic :: Software Development :: Testing :: Mocking"
    )
    Topic____Software_Development____Testing____Traffic_Generation = (
        "Topic :: Software Development :: Testing :: Traffic Generation"
    )
    Topic____Software_Development____Testing____Unit = (
        "Topic :: Software Development :: Testing :: Unit"
    )
    Topic____Software_Development____User_Interfaces = (
        "Topic :: Software Development :: User Interfaces"
    )
    Topic____Software_Development____Version_Control = (
        "Topic :: Software Development :: Version Control"
    )
    Topic____Software_Development____Version_Control____Bazaar = (
        "Topic :: Software Development :: Version Control :: Bazaar"
    )
    Topic____Software_Development____Version_Control____CVS = (
        "Topic :: Software Development :: Version Control :: CVS"
    )
    Topic____Software_Development____Version_Control____Git = (
        "Topic :: Software Development :: Version Control :: Git"
    )
    Topic____Software_Development____Version_Control____Mercurial = (
        "Topic :: Software Development :: Version Control :: Mercurial"
    )
    Topic____Software_Development____Version_Control____RCS = (
        "Topic :: Software Development :: Version Control :: RCS"
    )
    Topic____Software_Development____Version_Control____SCCS = (
        "Topic :: Software Development :: Version Control :: SCCS"
    )
    Topic____Software_Development____Widget_Sets = (
        "Topic :: Software Development :: Widget Sets"
    )
    Topic____System = "Topic :: System"
    Topic____System____Archiving = "Topic :: System :: Archiving"
    Topic____System____Archiving____Backup = "Topic :: System :: Archiving :: Backup"
    Topic____System____Archiving____Compression = (
        "Topic :: System :: Archiving :: Compression"
    )
    Topic____System____Archiving____Mirroring = (
        "Topic :: System :: Archiving :: Mirroring"
    )
    Topic____System____Archiving____Packaging = (
        "Topic :: System :: Archiving :: Packaging"
    )
    Topic____System____Benchmark = "Topic :: System :: Benchmark"
    Topic____System____Boot = "Topic :: System :: Boot"
    Topic____System____Boot____Init = "Topic :: System :: Boot :: Init"
    Topic____System____Clustering = "Topic :: System :: Clustering"
    Topic____System____Console_Fonts = "Topic :: System :: Console Fonts"
    Topic____System____Distributed_Computing = (
        "Topic :: System :: Distributed Computing"
    )
    Topic____System____Emulators = "Topic :: System :: Emulators"
    Topic____System____Filesystems = "Topic :: System :: Filesystems"
    Topic____System____Hardware = "Topic :: System :: Hardware"
    Topic____System____Hardware____Hardware_Drivers = (
        "Topic :: System :: Hardware :: Hardware Drivers"
    )
    Topic____System____Hardware____Mainframes = (
        "Topic :: System :: Hardware :: Mainframes"
    )
    Topic____System____Hardware____Symmetric_Multi_processing = (
        "Topic :: System :: Hardware :: Symmetric Multi-processing"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Audio = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Audio"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Audio_Video_AV = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Audio/Video (AV)"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Communications_Device_Class_CDC = "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Communications Device Class (CDC)"
    Topic____System____Hardware____Universal_Serial_Bus_USB____Diagnostic_Device = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Diagnostic Device"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Hub = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Hub"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Human_Interface_Device_HID = "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Human Interface Device (HID)"
    Topic____System____Hardware____Universal_Serial_Bus_USB____Mass_Storage = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Mass Storage"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Miscellaneous = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Miscellaneous"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Printer = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Printer"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Smart_Card = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Smart Card"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Vendor = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Vendor"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Video_UVC = (
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Video (UVC)"
    )
    Topic____System____Hardware____Universal_Serial_Bus_USB____Wireless_Controller = "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Wireless Controller"
    Topic____System____Installation_Setup = "Topic :: System :: Installation/Setup"
    Topic____System____Logging = "Topic :: System :: Logging"
    Topic____System____Monitoring = "Topic :: System :: Monitoring"
    Topic____System____Networking = "Topic :: System :: Networking"
    Topic____System____Networking____Firewalls = (
        "Topic :: System :: Networking :: Firewalls"
    )
    Topic____System____Networking____Monitoring = (
        "Topic :: System :: Networking :: Monitoring"
    )
    Topic____System____Networking____Monitoring____Hardware_Watchdog = (
        "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog"
    )
    Topic____System____Networking____Time_Synchronization = (
        "Topic :: System :: Networking :: Time Synchronization"
    )
    Topic____System____Operating_System = "Topic :: System :: Operating System"
    Topic____System____Operating_System_Kernels = (
        "Topic :: System :: Operating System Kernels"
    )
    Topic____System____Operating_System_Kernels____BSD = (
        "Topic :: System :: Operating System Kernels :: BSD"
    )
    Topic____System____Operating_System_Kernels____GNU_Hurd = (
        "Topic :: System :: Operating System Kernels :: GNU Hurd"
    )
    Topic____System____Operating_System_Kernels____Linux = (
        "Topic :: System :: Operating System Kernels :: Linux"
    )
    Topic____System____Power_UPS = "Topic :: System :: Power (UPS)"
    Topic____System____Recovery_Tools = "Topic :: System :: Recovery Tools"
    Topic____System____Shells = "Topic :: System :: Shells"
    Topic____System____Software_Distribution = (
        "Topic :: System :: Software Distribution"
    )
    Topic____System____System_Shells = "Topic :: System :: System Shells"
    Topic____System____Systems_Administration = (
        "Topic :: System :: Systems Administration"
    )
    Topic____System____Systems_Administration____Authentication_Directory = (
        "Topic :: System :: Systems Administration :: Authentication/Directory"
    )
    Topic____System____Systems_Administration____Authentication_Directory____LDAP = (
        "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP"
    )
    Topic____System____Systems_Administration____Authentication_Directory____NIS = (
        "Topic :: System :: Systems Administration :: Authentication/Directory :: NIS"
    )
    Topic____Terminals = "Topic :: Terminals"
    Topic____Terminals____Serial = "Topic :: Terminals :: Serial"
    Topic____Terminals____Telnet = "Topic :: Terminals :: Telnet"
    Topic____Terminals____Terminal_Emulators_X_Terminals = (
        "Topic :: Terminals :: Terminal Emulators/X Terminals"
    )
    Topic____Text_Editors = "Topic :: Text Editors"
    Topic____Text_Editors____Documentation = "Topic :: Text Editors :: Documentation"
    Topic____Text_Editors____Emacs = "Topic :: Text Editors :: Emacs"
    Topic____Text_Editors____Integrated_Development_Environments_IDE = (
        "Topic :: Text Editors :: Integrated Development Environments (IDE)"
    )
    Topic____Text_Editors____Text_Processing = (
        "Topic :: Text Editors :: Text Processing"
    )
    Topic____Text_Editors____Word_Processors = (
        "Topic :: Text Editors :: Word Processors"
    )
    Topic____Text_Processing = "Topic :: Text Processing"
    Topic____Text_Processing____Filters = "Topic :: Text Processing :: Filters"
    Topic____Text_Processing____Fonts = "Topic :: Text Processing :: Fonts"
    Topic____Text_Processing____General = "Topic :: Text Processing :: General"
    Topic____Text_Processing____Indexing = "Topic :: Text Processing :: Indexing"
    Topic____Text_Processing____Linguistic = "Topic :: Text Processing :: Linguistic"
    Topic____Text_Processing____Markup = "Topic :: Text Processing :: Markup"
    Topic____Text_Processing____Markup____HTML = (
        "Topic :: Text Processing :: Markup :: HTML"
    )
    Topic____Text_Processing____Markup____LaTeX = (
        "Topic :: Text Processing :: Markup :: LaTeX"
    )
    Topic____Text_Processing____Markup____Markdown = (
        "Topic :: Text Processing :: Markup :: Markdown"
    )
    Topic____Text_Processing____Markup____SGML = (
        "Topic :: Text Processing :: Markup :: SGML"
    )
    Topic____Text_Processing____Markup____VRML = (
        "Topic :: Text Processing :: Markup :: VRML"
    )
    Topic____Text_Processing____Markup____XML = (
        "Topic :: Text Processing :: Markup :: XML"
    )
    Topic____Text_Processing____Markup____reStructuredText = (
        "Topic :: Text Processing :: Markup :: reStructuredText"
    )
    Topic____Utilities = "Topic :: Utilities"
    Typing____Stubs_Only = "Typing :: Stubs Only"
    Typing____Typed = "Typing :: Typed"
