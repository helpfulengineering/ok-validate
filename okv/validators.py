from yamale.validators import DefaultValidators, Validator
from yamale.util import get_subclasses
from yaml import dump, error
from yamale import make_schema, make_data, schema, validate

class License(Validator):
    """ Custom License validator """
    tag = 'license'
    required_key_present = False

    # TODO: convert this to a map/dict and add a script generate that from the SPDX website
    # for faster comparisons and richer metadata
    def _valid_licenses(self):
        return [
            'Apache-2.0','Abstyles','Adobe-2006','Adobe-Glyph','CERN-OHL-1.2','ADSL','AFL-1.1','AFL-1.2',
            'AFL-2.1','0BSD','AFL-2.0','AFL-3.0','Afmparse','AGPL-1.0-only','AAL','AGPL-3.0-only',
            'AGPL-1.0-or-later','AGPL-3.0-or-later','Aladdin','AMDPLPA','AML','AMPAS','ANTLR-PD',
            'ANTLR-PD-fallback','Apache-1.0','Apache-1.1','APAFML','APL-1.0','APSL-1.0','APSL-1.1',
            'APSL-1.2','APSL-2.0','Artistic-1.0','Artistic-1.0-c18','Artistic-1.0-Perl','Artistic-2.0',
            'Bahyph','Barr','Beerware','BitTorrent-1.0','BitTorrent-1.1','blessing','BlueOak-1.0.0',
            'Borceux','BSD-1-Clause','BSD-2-Clause','BSD-2-Clause-Patent','BSD-2-Clause-Views',
            'BSD-3-Clause','BSD-3-Clause-Attribution','BSD-3-Clause-Clear','BSD-3-Clause-LBNL',
            'BSD-3-Clause-No-Nuclear-License','BSD-3-Clause-No-Nuclear-License-2014',
            'BSD-3-Clause-No-Nuclear-Warranty','BSD-3-Clause-Open-MPI','BSD-4-Clause','BSD-4-Clause-UC',
            'BSD-Protection','BSD-Source-Code','BSL-1.0','BUSL-1.1','bzip2-1.0.5','bzip2-1.0.6','CAL-1.0',
            'CAL-1.0-Combined-Work-Exception','Caldera','CATOSL-1.1','CC-BY-1.0',"CC-BY-2.0",'CC-BY-2.5',
            'CC-BY-3.0','CC-BY-4.0','CC-BY-3.0-AT','CC-BY-3.0-US','CC-BY-NC-1.0',"CC-BY-NC-2.0",
            'CC-BY-NC-2.5','CC-BY-NC-3.0','CC-BY-NC-4.0','CC-BY-NC-ND-1.0',"CC-BY-NC-ND-2.0",
            'CC-BY-NC-ND-2.5','CC-BY-NC-ND-3.0','CC-BY-NC-ND-4.0','CC-BY-NC-ND-3.0-IGO','CC-BY-NC-SA-1.0',
            "CC-BY-NC-SA-2.0",'CC-BY-NC-SA-2.5','CC-BY-NC-SA-3.0','CC-BY-NC-SA-4.0','CC-BY-ND-1.0',
            "CC-BY-ND-2.0",'CC-BY-ND-2.5','CC-BY-ND-3.0','CC-BY-ND-4.0','CC-BY-SA-1.0',"CC-BY-SA-2.0",
            'CC-BY-SA-2.5','CC-BY-SA-3.0','CC-BY-SA-4.0','CC-BY-SA-2.0-UK','CC-BY-SA-3.0-AT','CC-PDDC',
            'CC0-1.0','CDDL-1.0','CDDL-1.1','CDLA-Permissive-1.0','CDLA-Sharing-1.0','CECILL-1.0',
            'CECILL-1.1','CECILL-2.0','CECILL-2.1','CECILL-B','CECILL-C','CERN-OHL-1.1','CERN-OHL-P-2.0',
            'CERN-OHL-S-2.0','CERN-OHL-W-2.0','ClArtistic','CNRI-Jython','CNRI-Python',
            'CNRI-Python-GPL-Compatible','Condor-1.1','copyleft-next-0.3.0','copyleft-next-0.3.1',
            'CPAL-1.0','CPL-1.0','CPOL-1.02','Crossword','CrystalStacker','CUA-OPL-1.0','Cube','curl',
            'D-FSL-1.0','diffmark','DOC','dvipdfm','DSDP','Dotseqn','ECL-1.0','ECL-2.0','EFL-1.0',
            'EFL-2.0','eGenix','Entessa','EPICS','EPL-1.0','EPL-2.0','ErlPL-1.1','etalab-2.0',
            'EUDatagrid','EUPL-1.0','EUPL-1.1','EUPL-1.2','Eurosym','Fair','Frameworx-1.0','FreeImage',
            'FSFAP','FSFUL','FSFULLR','FTL','GFDL-1.1-invariants-only','GFDL-1.1-invariants-or-later',
            'GFDL-1.1-no-invariants-only','GFDL-1.1-no-invariants-or-later','GFDL-1.1-only',
            'GFDL-1.1-or-later','GFDL-1.2-invariants-only','GFDL-1.2-invariants-or-later',
            'GFDL-1.2-no-invariants-only','GFDL-1.2-no-invariants-or-later','GFDL-1.2-only',
            'GFDL-1.2-or-later','GFDL-1.3-invariants-only','GFDL-1.3-invariants-or-later',
            'GFDL-1.3-no-invariants-only','GFDL-1.3-no-invariants-or-later','GFDL-1.3-only',
            'GFDL-1.3-or-later','Glide','Glulxe','Giftware','GL2PS','GLWTPL','gnuplot','GPL-1.0-only',
            'GPL-1.0-or-later','GPL-2.0-only','GPL-2.0-or-later','GPL-3.0-only','GPL-3.0-or-later',
            'gSOAP-1.3b','HaskellReport','Hippocratic-2.1','HPND','HPND-sell-variant','HTMLTIDY',
            'IBM-pibs','ICU','IJG','ImageMagick','iMatix','Info-ZIP','Imlib2','Intel','Intel-ACPI',
            'Interbase-1.0','IPA','IPL-1.0','ISC','JasPer-2.0','JPNIC','JSON','LAL-1.2','LAL-1.3',
            'Latex2e','Leptonica','LGPL-2.0-only','LGPL-2.0-or-later','LGPL-2.1-only','LGPL-2.1-or-later',
            'LGPL-3.0-only','LGPL-3.0-or-later','LGPLLR','Libpng','libpng-2.0','libselinux-1.0','libtiff',
            'LiLiQ-P-1.1','LiLiQ-R-1.1','LiLiQ-Rplus-1.1','Linux-OpenIB','LPL-1.02','LPPL-1.0','LPPL-1.1',
            'LPPL-1.2','LPPL-1.3a','LPPL-1.3c','MakeIndex','MirOS','MIT','MITNFA','MIT-0',
            'MIT-advertising','MIT-CMU','MIT-enna','MIT-feh','MIT-open-group','Motosoto','mpich2',
            'MPL-1.0','MPL-1.1','MPL-2.0','MPL-2.0-no-copyleft-exception','MS-PL','MS-RL','MTLL',
            'MulanPSL-1.0','MulanPSL-2.0','Multics','Mup','NASA-1.3','Naumen','NBPL-1.0','NCGL-UK-2.0',
            'NCSA','Net-SNMP','NetCDF','Newsletr','NGPL','NIST-PD','NIST-PD-fallback','NLOD-1.0','NLPL',
            'Nokia','Noweb','NOSL','NPL-1.0','NPL-1.1','NPOSL-3.0','NRL','NTP','NTP-0','O-UDA-1.0',
            'OCCT-PL','OCLC-2.0','ODbL-1.0','ODC-By-1.0','OFL-1.0','OFL-1.0-RFN','OFL-1.0-no-RFN',
            'OFL-1.1','OFL-1.1-RFN','OFL-1.1-no-RFN','OGC-1.0','OGL-Canada-2.0','OGL-UK-1.0','OGL-UK-2.0',
            'OGL-UK-3.0','OGTSL','OLDAP-1.1','OLDAP-1.2','OLDAP-1.3','OLDAP-1.4','OLDAP-2.0','OLDAP-2.0.1',
            'OLDAP-2.1','OLDAP-2.2','OLDAP-2.2.1','OLDAP-2.2.2','OLDAP-2.3','OLDAP-2.4','OLDAP-2.5',
            'OLDAP-2.6','OLDAP-2.7','OLDAP-2.8','OML','OpenSSL','OPL-1.0','OSET-PL-2.1','OSL-1.0',
            'OSL-1.1','OSL-2.0','OSL-3.0','OSL-2.1','Parity-6.0.0','Parity-7.0.0','PDDL-1.0','PHP-3.0',
            'PHP-3.01','Plexus','PolyForm-Noncommercial-1.0.0','PolyForm-Small-Business-1.0.0',
            'PostgreSQL','PSF-2.0','psfrag','psutils','Python-2.0','Qhull','QPL-1.0','Rdisc','RHeCos-1.1',
            'RPL-1.1','RPL-1.5','RPSL-1.0','RSA-MD','RSCPL','Ruby','SAX-PD','Saxpath','SCEA','Sendmail',
            'Sendmail-8.23','SGI-B-1.0','SGI-B-1.1','SGI-B-2.0','SGI-B-1.0','SHL-0.51','SHL-0.51','SISSL',
            'SISSL-1.2','Sleepycat','SMLNJ','SMPPL','SNIA','Spencer-86','Spencer-94','Spencer-99',
            'SPL-1.0','SSH-OpenSSH','SSH-short','SSPL-1.0','SugarCRM-1.1.3','SWL','TAPR-OHL-1.0','TCL',
            'TCP-wrappers','TMate','TORQUE-1.1','TOSL','TU-Berlin-1.0','TU-Berlin-2.0','UCL-1.0',
            'Unicode-DFS-2015','Unicode-DFS-2016','Unicode-TOU','Unlicense','UPL-1.0','Vim','VOSTROM',
            'VSL-1.0','W3C','W3C-19980720','W3C-20150513','Watcom-1.0','Wsuipa','WTFPL','X11','Xerox',
            'XFree86-1.1','xinetd','Xnet','xpp','XSkat','YPL-1.0','YPL-1.1','Zed','Zend-2.0','Zimbra-1.3',
            'Zimbra-1.4','Zlib','zlib-acknowledgement','ZPL-1.1','ZPL-2.1','ZPL-2.0'      
        ]

    def _valid_keys(self):
            return ['hardware', 'documentation', 'software']

    def _is_valid(self, value):
        # If there are no keys declared for hardware, documentation, software
        # then this will evaluate to false
        self.license_error = ''
        validity = True
        if not bool(value):
            return False
        valid_licenses = self._valid_licenses()
        keys_to_check = self._valid_keys()
        for key in keys_to_check:
            if key in value:
                self.required_key_present = True
                provided_license = value[key]
                if provided_license not in valid_licenses:
                    if provided_license is None:
                        return False
                    if validity:
                        self.license_error = "\'" + provided_license + "\'"
                    else:
                        self.license_error = self.license_error+", \'" + provided_license + "\'"
                    validity = False
        if not self.required_key_present:
            return False
        return validity

    def fail(self, value):
        """Override to define a custom fail message"""
        if value is None:
            return 'There must be at least one license specified for \'hardware\', \'documentation\', or \'software\''
        elif not self.required_key_present:
            return 'There must be at least one license specified for \'hardware\', \'documentation\', or \'software\''
        elif len(self.license_error)<1:
            return 'At least one license field has been left blank. Please revise and provide valid SPDX license(s) or delete the field if you already have valid license(s).'
        else:
            return 'Invalid SPDX license(s) found: %s. Should be a valid identifier from https://spdx.org/licenses/' % (self.license_error)

class Key(Validator):
    """ Custom Key validator """
    tag = 'key'

    def __init__(self, *args, **kwargs):
        super(Key, self).__init__(*args, **kwargs)
        self.key_name = args[0]

    def _is_valid(self, value):
        if self.key_name in value:
            return True
        return False
    
    def fail(self, value):
        """Override to define a custom fail message"""
        return '\'%s\' is missing from the map.' % (self.key_name)

class RootValidation(object):
    key = '__root_validator__'
    # Appeasing pylint
    schema = None
    data = []
    validators = None
    args = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def validate(self):
        """ Used for applying validation at the root level of the schema """
        # This is an experimental process
        schema = self.schema
        res_arr=[]
        for item in schema.includes.items():
            if item[0] == self.key:
                root_level = self.data[0][0]
                root_level_dict = {"%s" % (self.key): root_level}
                yaml_dump = str(dump(root_level_dict))
                root_data = make_data(content=str(yaml_dump))
                root_schema_string = '%s: %s' % (self.key, item[1].dict)
                root_schema = make_schema(path=None, validators=self.validators, content=root_schema_string)
                raw_results = validate(root_schema, root_data, strict=(not self.args.no_strict), _raise_error=True)
                results=list(raw_results)
                for i in results:
                    res_arr.append(str(i))
                return res_arr  # return results and work from there??

DefaultValidators = {}

for v in get_subclasses(Validator):
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[v.tag] = v
    DefaultValidators[v.__name__] = v