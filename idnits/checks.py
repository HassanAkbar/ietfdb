# Copyright 2018-2019 IETF Trust, All Rights Reserved
# -*- coding: utf-8 indent-with-tabs: 0 -*-

from __future__ import unicode_literals, print_function, division

import io
import lxml
import re
import requests
import six
import sys
import xml2rfc

from collections import namedtuple
from idnits import default_options
from idnits.utils import normalize_paragraph
from xml2rfc.boilerplate_tlp import boilerplate_tlp
from xml2rfc.writers.base import deprecated_element_tags
from xml2rfc.writers.preptool import PrepToolWriter

if six.PY2:
    from urlparse import urlsplit, urlunsplit
    from urllib import urlopen
elif six.PY3:
    from urllib.parse import urlsplit, urlunsplit
    from urllib.request import urlopen

try:
    import debug
    debug.debug = True
except ImportError:
    debug = None
    pass


Check = namedtuple('Check', [ 'fmt', 'type', 'norm', 'easy', 'subm', 'func', ])
Nit   = namedtuple('Nit',   [ 'num', 'msg', ])

tlp_keys = [ (float(k), k) for k in boilerplate_tlp.keys() ]
tlp_keys.sort()
latest = tlp_keys[-1][1]
tlp = boilerplate_tlp[latest]

bplist = [ tlp[i][p] for i in tlp for p in range(len(tlp[i])) ]
bpkeys = set()

for i in range(len(bplist)):
    para = bplist[i]
    para = normalize_paragraph(para)
    key  = para[:14]
    para = re.sub(r'([(|).*+])', r'\\\1', para)
    para = para.format(
            year='(19\d\d|20\d\d)',
            scheme='(http|https)',
            )
    bplist[i] = para
    bpkeys.add(key)

def plurals(l):
    n = len(l)
    if n == 1:
        d = dict(n=n, s='', a='a', an='an', this='this')
    else:
        d = dict(n=n, s='s', a='', an='', this='these')
    return d

def enit(nits, e, s):
    nits.append(Nit(e.sourceline, s))

def lnit(nits, l, s):
    nits.append(Nit(l, s))


class Checker(PrepToolWriter):
    # We subclass PrepToolWriter in order to use the checks it provides.  Have to override
    # .warn(), .err() and .die().

    def __init__(self, doc, options=default_options):
        if hasattr(doc, 'xmlrfc'):
            super(Checker, self).__init__(doc.xmlrfc)
        self.doc = doc
        self.options = options
        self.nits = dict(err=[], warn=[], comm=[])
        self.tmpnits = []
        #

    def get_checks(self):
        checks = self.checks
        fmt = 'xml' if self.doc.type in ['application/xml', 'text/xml', ] else 'txt' if self.doc.type in ['text/plain', ] else None
        if fmt is None:
            self.nits['err'].append(([Nit(None,"Found input type %s" % self.doc.type)], "Input type text or xml is required"))
            return []
        checks = [ c for c in checks if c.fmt in ['any', fmt] ]
        type = 'rfc' if self.doc.name.startswith('rfc') or self.doc.root != None and self.doc.root.get('number') != None else 'ids'
        checks = [ c for c in checks if c.type in ['any', type] ]
        if   self.options.mode == 'normal':
            checks = [ c for c in checks if c.norm != 'none' ]
        elif self.options.mode == 'lenient':
            checks = [ c for c in checks if c.easy != 'none' ]
        elif self.options.mode == 'submission':
            checks = [ c for c in checks if c.subm != 'none' ]
        else:
            raise RuntimeError("Internal error: Unexpected mode: %s" % self.options.mode)
        return checks

    def warn(self, e, text):
        self.tmpnits.append(Nit(e.sourceline, text))
    err = warn
    die = warn

    def check(self):
        mode = self.options.mode
        checks = self.get_checks()
        blank  = 0
        done   = 0

        if any([ c.fmt == 'xml' for c in checks]) and self.doc.root != None:
            ver = self.doc.root.get('version')
            if ver != '3':
                self.nits['err'].append(([Nit(self.doc.root.sourceline, 'Expected <rfc ... version="3" ...>, found %s'%ver),], "For xml checks, version 3 is required"))
                self.doc.root = None

        for check in checks:
            severity = check.norm if mode == 'normal' else check.easy if mode == 'lenient' else check.subm
            if check.fmt == 'xml' and not self.doc.root != None:
                continue
            res = check.func(self)
            if res is None:
                blank += 1
            else:
                done  += 1
                assert len(res) == 2
                nits, msg = res
                if nits:
                    msg = msg.format(**plurals(nits)).replace('  ', ' ')
                    self.nits[severity].append((nits, msg))

        if blank and self.options.debug:
            sys.stdout.write("Checks: ran %d, %d unimplemented\n" % (done, blank))
        return self.nits


    def any_text_has_control_char(self):
        "Control characters other than CR, NL, or FF appear (0x01-0x09,0x0b,0x0e-0x1f)"
        nits = []
        for l in self.doc.lines:
            match = re.search(r'[\x01-\x09\x0b\x0e-\x1f]', l.txt)
            if match:
                lnit(nits, l.num, "Found control character 0x%02x in column %d" % (ord(match.group()), match.start(), ))
        return nits, "Found {n} line{s} with control characters"
        
    def any_text_has_invalid_utf8(self):
        "Byte sequences that are not valid UTF-8 appear"
        nits = []
        if not self.doc.encoding in ['ascii', 'us-ascii', 'utf-8', ]:
            for num, txt in enumerate(self.doc.raw.splitlines()):
                try:
                    txt.decode('utf-8')
                except UnicodeDecodeError as e:
                    code = ord(e.args[1][e.start])
                    lnit(nits, num, "Invalid UTF-8 characters starting in column %d: 0x%x" % (e.start, code))
        return nits, "File encoding is not utf-8 (seems to be %s)" % self.doc.encoding

    def any_text_has_nonascii_char(self):
        "Non-ASCII UTF-8 appear (comment will point to guidance in draft-iab-rfc-nonascii or its successor)"
        nits = []
        if not self.doc.encoding in ['ascii', 'us-ascii', ]:
            if self.doc.encoding in ['utf-8', ]:
                for num, txt in enumerate(self.doc.raw.splitlines()):
                    try:
                        txt.decode('ascii')
                    except UnicodeDecodeError as e:
                        code = ord(e.args[1][e.start])
                        lnit(nits, num, "Non-ASCII characters starting in column %d: 0x%x" % (e.start, code))
        return nits, "Found {n} line{s} with non-ASCII characters"

    def any_abstract_missing(self):
        "Missing Abstract section"

    def any_introduction_missing(self):
        "Missing Introduction section"

    def any_security_considerations_missing(self):
        "Missing Security Considerations section"

    def any_author_address_missing(self):
        "Missing Author Address section"

    def any_references_no_category(self):
        "References (if any present) are not categorized as Normative or Informative"

    def any_abstract_with_reference(self):
        "Abstract contains references"

    def any_fqdn_not_example(self):
        "FQDN appears (other than www.ietf.org) not meeting RFC2606/RFC6761 recommendations"

    def any_ipv4_private_not_example(self):
        "Private IPv4 address appears that doesn't meet RFC5735 recommendations"

    def any_ipv4_multicast_not_example(self):
        "Multicast IPv4 address appears that doesn't meet RFC5771/RFC6676 recommendations"

    def any_ipv4_generic_not_example(self):
        "Other IPv4 address appears that doesn't meet RFC5735 recommendations"

    def any_ipv6_local_not_example(self):
        "Unique Local IPv6 address appears that doesn't meet RFC3849/RFC4291 recommendations"

    def any_ipv6_link_not_example(self):
        "Link Local IPv6 address appears that doesn't meet RFC3849/RFC4291 recommendations"

    def any_ipv6_generic_not_example(self):
        "Other IPv6 address appears that doesn't meet RFC3849/RFC4291 recommendations"

    def any_text_code_comment(self):
        "A possible code comment is detected outside of a marked code block"

    def any_rfc2119_info_missing(self):
        "2119 keywords occur, but neither the matching boilerplate nor a reference to 2119 is missing"

    def any_rfc2119_boilerplate_missing(self):
        "2119 keywords occur, a reference to 2119 exists, but matching boilerplate is missing"

    def any_rfc2119_boilerplate_extra(self):
        "2119 boilerplate is present, but document doesn't use 2119 keywords"

    def any_rfc2119_bad_keyword_combo(self):
        "Badly formed combination of 2119 words occurs (MUST not, SHALL not, SHOULD not, not RECOMMENDED, MAY NOT, NOT REQUIRED, NOT OPTIONAL)"

    def any_rfc2119_boilerplate_lookalike(self):
        "Text similar to 2119 boilerplate occurs, but doesn't reference 2119"

    def any_rfc2119_keyword_lookalike(self):
        "NOT RECOMMENDED appears, but is not included in 2119-like boilerplate"

    def any_abstract_update_info_missing(self):
        "Abstract doesn't directly state it updates or obsoletes each document so affected (Additional comment if Abstract mentions the document some other way)"

    def any_abstract_update_info_extra(self):
        "Abstract states it updates or obsoletes a document not declared in the relevant field previously"

    def any_authors_addresss_grammar(self):
        "Author's address section title misuses possessive mark or uses a character other than a single quote"

    def any_reference_not_used(self):
        "A reference is declared, but not used in the document"

    def any_reference_is_downref(self):
        "A reference appears to be a downref (noting if reference appears in the downref registry)"

    def any_reference_status_unknown(self):
        "A normative reference to an document of unknown status appears (possible downref)"

    def any_reference_is_obsolete_norm(self):
        "A normative or unclassified reference is to an obsolete document"

    def any_reference_is_obsolete_info(self):
        "An informative reference is to an obsolete document"

    def any_reference_is_draft_rfc(self):
        "A reference is to a draft that has already been published as an rfc"

    def any_sourcecode_no_license(self):
        "A code-block is detected, but the block does not contain a license declaration"

    def any_filename_base_bad_characters(self):
        "Filename's base name contains characters other than digits, lowercase alpha, and dash"

    def any_filename_ext_mismatch(self):
        "Filename's extension doesn't match format type (.txt, .xml)"

    def any_filename_base_not_docname_(self):
        "Filename's base name doesn't match the name declared in the document"

    def any_filename_too_long(self):
        "Filename (including extension) is more than 50 characters"

    def any_obsoletes_obsolete_rfc(self):
        "Document claims to obsolete an RFC that is already obsolete"

    def any_updates_obsolete_rfc(self):
        "Document claims to update an RFC that is obsolete"

    def any_doc_status_info_bad(self):
        "Document's status or intended status is not found or not recognized"

    def any_doc_date_bad(self):
        "Document's date can't be determined or is too far in the past or the future (see existing implementation for 'too far')"

    def any_section_iana_missing(self):
        "Missing IANA considerations section"

    def any_docname_malformed(self):
        "Filename's base name doesn't begin with 'draft', contains two consecutive hyphens, or doesn't have enough structure to contain the individual or stream, potentially a wg name, and a distinguishing name. (draft-example-00 is an error, but draft-example-filename is acceptable)"

    def any_section_iana_missing(self):
        "Missing IANA considerations section"

    def any_doc_rev_unexpected(self):
        "Version of document is unexpected (already exists, or leaves a gap)"

    def xml_element_deprecated(self):
        "Any deprecated elements or attributes appear"
        nits = []
        for e in self.doc.root.iter(*list(deprecated_element_tags)):
            enit(nits, e, "Deprecated element: %s" % e.tag)
        return nits, "Found {n} deprecated xml element{s}"

    def xml_stream_contradiction(self):
        "Metadata and document's 'submissionType' attribute state different streams"
        self.tmpnits = []
        self.check_series_and_submission_type(self.doc.root, None)
        return self.tmpnits, "Found inconsistent stream settings"

    def xml_source_code_in_sourcecode(self):
        "The text inside a <sourcecode> tag contains the string '<CODE BEGINS>' (Warn that the string is unnecessary and may duplicate what a presentation format converter will produce.)"
        nits = []
        for e in self.doc.root.iter('sourcecode'):
            if e.text and ('<CODE BEGINS>' in e.text) and (e.get('markers')=='true'):
                enit(nits, e, 'Found "<SOURCE BEGINS>" in <sourcecode> element with markers="true"')
        return nits, "Found {n} instance{s} of '<SOURCE BEGINS>' in <sourcecode> that will cause duplicate markers in the output"

    def xml_source_code_in_text(self):
        "The text inside any other tag contains the string '<CODE BEGINS>' (Warn that if the text is a code block, it should appear in a <sourcecode> element)"
        nits = []
        for e in self.doc.root.iter('t'):
            text = ' '.join(e.itertext())
            if text and ('<CODE BEGINS>' in text):
                enit(nits, e, 'Found "<SOURCE BEGINS>" in text')
        return nits, 'Found {n} instance{s} of "<SOURCE BEGINS>" in text.  If this is the start of a code block, it should be put in a <sourcecode> element'

    def xml_text_looks_like_ref(self):
        "Text occurs that looks like a text-document reference (e.g. [1], or [RFC...])  (if the text was really a reference it should be in an <xref> tag)"
        nits = []
        ref_format = r"\[(([0-9A-Z]|I-?D.)[0-9A-Za-z-]*( [0-9A-Z-]+)?|(IEEE|ieee)[A-Za-z0-9.-]+|(ITU ?|ITU-T ?|G\\.)[A-Za-z0-9.-]+)\]"
        tags = list(self.text_tags - set(['sourcecode', 'artwork', ]))
        for e in self.doc.root.iter(tags):
            text = ' '.join([ t for t in [e.text, e.tail] if t and t.strip() ])
            match = re.search(ref_format, text)
            if match:
                enit(nits, e, "Found text that looks like a citation: %s" % match.group(0))
        return nits, "Found {n} instance{s} of text that looks like a citation, and maybe should use <xref> instead"

    def xml_ipr_attrib_missing(self):
        "The <rfc> ipr attribute is missing or not recognized"
        nits = []
        ipr = self.doc.root.get('ipr')
        if ipr is None:
            enit(nits, self.doc.root, "Expected an ipr attribute on <rfc>, but found none")
        return nits, "Found no ipr attribute on <rfc>"

    def xml_ipr_attrib_unknown(self):
        "The ipr attribute is not one of 'trust200902', 'noModificationTrust200902', 'noDerivativesTrust200902', or 'pre5378Trust200902'"
        nits = []
        supported_ipr = [
            'trust200902',
            'noModificationTrust200902',
            'noDerivativesTrust200902',
            'pre5378Trust200902',
        ]
        ipr = self.doc.root.get('ipr')
        if not ipr in supported_ipr:
            enit(nits, self.doc.root, "Found an unrecognized ipr attribute on <rfc>: %s" % ipr)
        return nits, "Found an unrecognized ipr attribute: %s" % ipr

    def xml_ipr_attrib_disallowed(self):
        "Document is ietf stream and ipr attribute is one of 'noModificationTrust200902' or 'noDerivativesTrust200902'"
        nits = []
        disallowed_ipr = [
            'noModificationTrust200902',
            'noDerivativesTrust200902',
        ]
        ipr = self.doc.root.get('ipr')
        stream = self.doc.root.get('submissionType', 'IETF')
        if stream=='IETF' and ipr in disallowed_ipr:
            enit(nits, self.doc.root, 'Found a disallowed ipr attribute: %s' % ipr)
        return nits, "Found a disallowed ipr attribute for stream IETF: %s" % ipr

    def xml_workgroup_not_group(self):
        "The <workgroup> content doesn't end with 'Group'"
        nits = []
        e = self.doc.root.find('./front/workgroup')
        wg = ''
        if e != None:
            wg = e.text.strip()
            if not wg.endswith('Group'):
                enit(nits, e, "Expected a <workgroup> entry ending in 'Group', but found '%s'" % wg)
        return nits, "Found a bad <workgroup> value: %s" % wg

    def xml_update_info_bad(self):
        "The 'obsoletes' or 'updates' attribute values of the <rfc> element are not comma separated strings of digits"
        nits = []
        for a in 'obsoletes', 'updates':
            l = self.doc.root.get(a)
            if l and l.strip():
                nums = [ n.strip() for n in l.split(',') ]
                for num in nums:
                    if not n.strip().isdigit():
                        enit(nits, self.doc.root, "Expected an RFC number in '%s', but found %s" % (a, num))
        return nits, "Found malformed updates / obsoletes information"

    def xml_update_info_noref(self):
        "The rfcs indicated by the 'obsoletes' and 'updates' attribute values of the <rfc> element are not included in the references section"
        nits = []
        for a in 'obsoletes', 'updates':
            l = self.doc.root.get(a)
            if l and l.strip():
                nums = [ n.strip() for n in l.split(',') if n.strip().isdigit() ]
                for num in nums:
                    ref = self.doc.root.find('./back/references//reference/seriesInfo[@name="RFC"][@value="%s"]' % num)
                    debug.show('ref')
                    if ref is None:
                        nits.append(Nit(self.doc.root.sourceline,
                            "Did not find RFC %s, listed in '%s', in the references" %(num, a)))
        return nits, "Found updates / obsoletes RFC numbers not included in a References section"

    def xml_xref_target_missing(self):
        "An <xref> has no target attribute"
        nits = []
        for e in self.doc.root.xpath('.//xref'):
            if not e.get('target'):
                enit(nits, e, "Found <xref> without a target attribute: %s" % lxml.etree.tostring(e))
        return nits, "Found {n} instance{s} of {an} <xref> element{s} without a target"

    def xml_xref_target_not_anchor(self):
        "Any <xref> target attribute does not appear as an anchor of another element"
        nits = []
        for e in self.doc.root.xpath('.//xref[@target]'):
            target = e.get('target')
            t = self.doc.root.find('.//*[@anchor="%s"]' % target)
            if t is None:
                t = self.doc.root.find('.//*[@pn="%s"]' % target)
                if t is None:
                    t = self.doc.root.find('.//*[@slugifiedName="%s"]' % target)
            if t is None:
                enit(nits, e, "Found <xref> with a target without matching anchor: %s" % lxml.etree.tostring(e))
        return nits, "Found {n} instance{s} of {an} <xref> element{s} with unmatched target"


    def xml_relref_target_missing(self):
        "A <relref> has no target attribute"
        nits = []
        for e in self.doc.root.xpath('.//relref'):
            if not e.get('target'):
                enit(nits, e, "Found <relref> without a target attribute: %s" % lxml.etree.tostring(e))
        return nits, "Found {n} instance{s} of {a} <relref> element{s} without a target"

    def xml_relref_target_not_anchor(self):
        "Any <relref> target attribute does not appear as an anchor of a <reference> element"
        nits = []
        for e in self.doc.root.xpath('.//relref[@target]'):
            target = e.get('target')
            t = self.doc.root.find('./back//reference[@anchor="%s"]' % target)
            if t is None:
                enit(nits, e, "Found <relref> with a target that is not a <reference>: %s" % lxml.etree.tostring(e))
        return nits, "Found {n} instance{s} of {a} bad <relref> target{s}"

    def xml_relref_target_no_target(self):
        "A <reference> element pointed to by a <relref> target attribute does not itself have a target attribute"
        nits = []
        for e in self.doc.root.xpath('.//relref[@target]'):
            target = e.get('target')
            t = self.doc.root.find('./back//reference[@anchor="%s"]' % target)
            if t != None:
                ttarget = t.get('target')
                if not (ttarget and ttarget.strip()):
                    enit(nits, e, 
                        'Found a <relref> target without its own target attribute: <reference anchor="%s"...>' % target)
        return nits, "Found {n} instance{s} of {a} <relref> target{s} without a target attribute in the <reference>"

    def xml_artwork_multiple_content(self):
        "An element (particularly <artwork> or <sourcecode>) contains both a src attribute, and content"

        # Note: The specifications RFCs had selfcontradictory text regarding this, for
        # <artwork>.  After discussion, this is not a nit for <artwork>, as any content is
        # text-mode fallback for SVG artwork.

    def xml_element_src_bad_schema(self):
        "The src attribute of an element contains a URI scheme other than data:, file:, http:, or https:"
        nits = []
        for e in self.doc.root.xpath('.//*[@src]'):
            valid_schemes = ['data', 'file', 'http', 'https', ]
            src = e.get('src', '')
            parts = urlsplit(src)
            if not parts.scheme in valid_schemes:
                enit(nits, e, 'Expected the src scheme to be one of %s; but found "%s" in "%s ..."' % (','.join(valid_schemes), parts.scheme, src[:16]))
        return nits, "Found {n} instance{s} of {a} 'src' attribute{s} with disallowed URL scheme"
            

    def xml_ids_link_has_bad_content(self):
        "A <link> exists with DOI or RFC-series ISDN for this document when the document is an Internet-Draft"
        nits = []
        for e in self.doc.root.xpath('./link'):
            href = e.get('href')
            if href == 'urn:issn:2070-1721':
                enit(nits, e, "Found a <link> with an RFC ISSN URN in a draft: %s" % href)
            scheme, rest = href.split(':', 1)
            if rest.startswith('//dx.doi.org/10.17487/rfc'):
                enit(nits, e, "Found a <link> with an RFC DOI in a draft: %s" % href)
        return nits, "Found {n} instance{s} of {a} <link> element{s} with incorrect content for an Internet-Draft"

    def xml_section_bad_numbered_false(self):
        "A <section> with a numbered attribute of 'false' is not a child of <boilerplate>, <middle>, or <back>, or has a subsequent <section> sibling with a numbered attribute of 'true'"
        nits = []
        valid_parents = ['boilerplate', 'middle', 'back']
        for e in self.doc.root.xpath('.//section[@numbered="false"]'):
            if not e.getparent().tag in valid_parents:
                enit(nits, e, 'Found a section with numbered="false" which is not a top-level section')
            for c in e.xpath('.//section[@numbered="true"]'):
                enit(nits, c, 'Found a section with numbered="true" which is a child of an unnumbered section')
        return nits, "Found {n} instance{s} of {a} <section> element{s} with an incorrect 'numbered' attribute"

    def xml_xref_counter_bad_target(self):
        "An <xref> element with no content and a 'format' attribute of 'counter' has a 'target' attribute whose value is not a section, figure, table or ordered list number"
        nits = []
        valid_targets = [ 'section', 'figure', 'table', 'ol', ]
        for e in self.doc.root.xpath('.//xref[@format="counter"]'):
            if e.text and e.text.strip():
                target = e.get('target')
                t = self.doc.root.find('.//*[@anchor="%s"]'%target)
                if t is None:
                    enit(nits, e, 'Found an <xref> with format="counter" without a matching anchor: %s' % lxml.etree.tostring(e))
                elif t.tag not in valid_targets:
                    enit(nits, e, 'Found an <xref> with format="counter" referring to a <%s> element' % t.tag)
        return nits, "Found {n} instance{s} of {an} <xref> element{s} with format=\"counter\" having a bad target"


    def xml_relref_target_missing_anchor(self):
        "A <relref> element whose 'target' attribute points to a document in xml2rfcv3 format, and whose 'relative' attribute value (or the derived value from a 'section' attribute) does not appear as an anchor in that document"
        nits = []
        for tag in ['relref', 'xref', ]:
            for e in self.doc.root.xpath('.//%s[@target]'%tag):
                target = e.get('target')
                section = e.get('section')
                relative = e.get('relative')
                if relative is None and section is None:
                    continue
                t = self.doc.root.find('./back//reference[@anchor="%s"]' % target)
                if t != None:
                    ttarget = t.get('target')
                    ttparts = urlsplit(ttarget)
                    if (   re.search('/rfc\d+.xml$', ttparts.path)
                        or re.search('/draft-.*.xml$', ttparts.path)):
                        sys.stdout.write("Checking %s ...\n" % ttarget)
                        r = requests.get(ttarget, timeout=2.0)
                        debug.show('r.status_code')
                        if r.status_code != 200:
                            raise RuntimeError("Could not fetch <relref> target's external URL: %s" % ttarget)
                        else:
                            if relative is None:
                                relative = 'section-%s' % section
                            try:
                                parser = xml2rfc.XmlRfcParser(None, quiet=True)
                                parser.text = r.text.encode('utf-8')
                                parser.source = ttarget
                                refdoc = parser.parse()
                                f = refdoc.tree.find('//*[@anchor="%s"]'%relative)
                                if f is None:
                                    enit(nits, e,
                                        'The external URL %s for <%s> with target="%s" does not have an anchor matching "%s"' % (ttarget, tag, target, relative))
                            except lxml.etree.XMLSyntaxError:
                                pass
        return nits, "Found {n} instance{s} of {a} <relref> / <xref> element{s} with a relative identifier that does not exist in the target document"

    def xml_artwork_svg_wrong_media_type(self):
        "An <artwork> element with type 'svg' has a 'src' attribute with URI scheme 'data:' and the mediatype of the data: URI is not 'image/svg+xml'"
        nits = []
        for e in self.doc.root.xpath('.//artwork[@type="svg"]'):
            src = e.get('src')
            if src and src.startswith('data:'):
                f = urlopen(src)
                if six.PY2:
                    mediatype = f.info().gettype()
                else:
                    mediatype = f.info().get_content_type()
                if mediatype != 'image/svg+xml':
                    enit(nits, e, 'Found <artwork> with type="svg" but an unexpected media type: %s' % mediatype)
        return nits, "Found {n} instance{s} of {an} <artwork> element{s} with bad media type"
                    

    def xml_sourcecode_multiple_content(self):
        "A <sourcecode> element has both a 'src' attribute and non-empty content"
        nits = []
        for e in self.doc.root.xpath('.//sourcecode[@src]'):
            debug.show('e')
            if e.text and e.text.strip():
                enit(nits, e,
                    'Found a <sourcecode> element with both a src attribute and text content')
        return nits, "Found {n} instance{s} of {a} <sourcecode> element{s} with both a 'src' attribute and text content"


    def xml_rfc_note_remove_true(self):
        "A <note> element has a 'removeInRFC' attribute with a value of 'true'"

    def xml_rfc_artwork_wrong_type(self):
        "An <artwork> element has type other than 'ascii-art','call-flow','hex-dump', or 'svg'"

    def xml_text_has_boilerplate(self):
        "The text inside any tag sufficiently matches any of the boilerplate in the IETF-TLP-4 section 6a-6d (such text should probably be removed and the ipr attribute of the rfc tag should be verified)"
        nits = []
        for t in self.doc.root.xpath('./middle//section//t'):
            text = normalize_paragraph(' '.join(t.itertext()))
            key = text[:14]
            if key in bpkeys:
                for regex in bplist:
                    if re.match(regex, text):
                        enit(nits, t, 
                            "Found what looks like a boilerplate paragraph in xml text: %s..." % text[:20])
        return nits, "Found {n} case{s} of what looks like boilerplate in xml <t> element{s}; {this} should be removed"

    def xml_boilerplate_mismatch(self):
        "The value of the <boilerplate> element, if non-empty, does not match what the ipr, category, submission, and consensus <rfc> attributes would cause to be generated"

    def xml_rfc_generated_attrib_wrong(self):
        "The value of any present pn or slugifiedName attributes do not match what would be regenerated"

    def txt_text_added_whitespace(self):
        "Document does not appear to be ragged-right (more than 50 lines of intra-line extra spacing)"

    def txt_text_lines_too_long(self):
        "Document contains over-long lines (cut-off is 72 characters. Report longest line, and count of long lines)"

    def txt_text_line_break_hyphens(self):
        "Document has hyphenated line-breaks"

    def txt_text_hyphen_space(self):
        "Document has a hyphen followed immediately by a space within a line"

    def txt_update_info_extra_text(self):
        "Updates or Obsoletes line on first page has more than just numbers of RFCs (such as the character sequence 'RFC')"

    def txt_update_info_not_in_order(self):
        "Updates or Obsoletes numbers do not appear in ascending order"

    def txt_doc_bad_magic(self):
        "Document starts with PK or BM"

    def txt_reference_style_mixed(self):
        "Document appears to use numeric references, but contains something that looks like a text-style reference (or vice-versa)"

    def txt_text_ref_unused_(self):
        "A string that looks like a reference appears but does not occur in any reference section"

    def txt_abstract_numbered(self):
        "Abstract section is numbered"

    def txt_status_of_memo_numbered(self):
        "'Status of this memo' section is numbered"

    def txt_copyright_notice_numbered(self):
        "Copyright Notice section is numbered"

    def txt_boilerplate_copyright_missing(self):
        "TLP-4 6.b.i copyright line is not present"

    def txt_boilerplate_copyright_year_wrong(self):
        "TLP-4 6.b.i copyright date is not this (or command-line specified) year"

    def txt_boilerplate_licence_missing(self):
        "TLP-4 6.b.i or b.ii license notice is not present, or doesn't match stream"

    def txt_boilerplate_restrictions_found(self):
        "IETF stream document sufficiently matches TLP-4 6.c.i or 6.c.ii text (restrictions on publication or derivative works)"

    def txt_boilerplate_copyright_duplicate(self):
        "More than one instance of text sufficiently matching the TLP-4 6.b.i copyright line occurs"

    def txt_boilerplate_licence_duplicate(self):
        "More than one instance of text sufficiently matching either the TLP4 6.b.i or 6.b.ii license notice occurs"

    def txt_boilerplate_pre5378_missing_upd(self):
        "Document obsoletes or updates any pre-5378 document, and doesn't contain the pre-5378 material of TLP4 6.c.iii"

    def txt_boilerplate_pre5378_missing_prev(self):
        "Any prior version of the document might be pre-5378 and the document doesn't contain the pre-5378 material of TLP4 6.c.iii"

    def txt_pages_too_long(self):
        "Contains over-long pages (report count of pages with more than 58 lines)"

    def txt_head_label_missing(self):
        "Doesn't say INTERNET DRAFT in the upper left of the first page"

    def txt_head_expiration_missing(self):
        "Doesn't have expiration date on first and last page"

    def txt_boilerplate_working_doc_missing(self):
        "Doesn't have an acceptable paragraph noting that IDs are working documents"

    def txt_boilerplate_6month_missing(self):
        "Doesn't have an acceptable paragraph calling out 6 month validity"

    def txt_boilerplate_current_ids_missing(self):
        "Doesn't have an acceptable paragraph pointing to the list of current ids"

    def txt_boilerplate_current_ids_duplicate(self):
        "Has multiple occurrences of current id text"

    def txt_head_docname_missing(self):
        "Document name doesn't appear on first page"

    def txt_table_of_contents_missing(self):
        "Has no Table of Contents"

    def txt_boilerplate_ipr_missing(self):
        "Ipr disclosure text (TLP 4.0 6.a) does not appear"

    def txt_boilerplate_ipr_not_first_page(self):
        "Ipr disclosure text (TLP 4.0 6.a) appears after first page"

    def txt_pages_missing_formfeed(self):
        "Pages are not separated by formfeeds"


    def txt_pages_formfeed_misplaced(self):
        "'FORMFEED' and '[Page...]' occur on a line, possibly separated by spaces (indicates 'NROFF post-processing wasn't successful)"

    def txt_text_bad_section_indentation(self):
        "A section title occurs at an unexpected indentation"

    checks = [

    #3.1 Conditions to check for any input type
    #--------------------------------------

        # fmt    type   norm    easy    subm
        # xml    rfc
        # txt    ids
        Check('any', 'any', 'err',  'warn', 'none', any_text_has_control_char), # Control characters other than CR, NL, or FF appear (0x01-0x09,0x0b,0x0e-0x1f) 
        Check('any', 'any', 'err',  'warn', 'none', any_text_has_invalid_utf8), # Byte sequences that are not valid UTF-8 appear 
        Check('any', 'any', 'comm', 'comm', 'none', any_text_has_nonascii_char), # Non-ASCII UTF-8 appear (comment will point to guidance in draft-iab-rfc-nonascii or its successor) 
        Check('any', 'any', 'err',  'err',  'err',  any_abstract_missing), # Missing Abstract section 
        Check('any', 'any', 'err',  'warn', 'none', any_introduction_missing), # Missing Introduction section 
        Check('any', 'any', 'err',  'warn', 'none', any_security_considerations_missing), # Missing Security Considerations section 
        Check('any', 'any', 'err',  'warn', 'none', any_author_address_missing), # Missing Author Address section 
        Check('any', 'any', 'err',  'warn', 'none', any_references_no_category), # References (if any present) are not categorized as Normative or Informative 
        Check('any', 'any', 'err',  'warn', 'none', any_abstract_with_reference), # Abstract contains references 
        Check('any', 'any', 'warn', 'warn', 'none', any_fqdn_not_example), # FQDN appears (other than www.ietf.org) not meeting RFC2606/RFC6761 recommendations 
        Check('any', 'any', 'warn', 'warn', 'none', any_ipv4_private_not_example), # Private IPv4 address appears that doesn't meet RFC5735 recommendations 
        Check('any', 'any', 'warn', 'warn', 'none', any_ipv4_multicast_not_example), # Multicast IPv4 address appears that doesn't meet RFC5771/RFC6676 recommendations 
        Check('any', 'any', 'warn', 'warn', 'none', any_ipv4_generic_not_example), # Other IPv4 address appears that doesn't meet RFC5735 recommendations 
        Check('any', 'any', 'warn', 'warn', 'none', any_ipv6_local_not_example), # Unique Local IPv6 address appears that doesn't meet RFC3849/RFC4291 recommendations 
        Check('any', 'any', 'warn', 'warn', 'none', any_ipv6_link_not_example), # Link Local IPv6 address appears that doesn't meet RFC3849/RFC4291 recommendations 
        Check('any', 'any', 'warn', 'warn', 'none', any_ipv6_generic_not_example), # Other IPv6 address appears that doesn't meet RFC3849/RFC4291 recommendations 
        Check('any', 'any', 'warn', 'warn', 'warn', any_text_code_comment), # A possible code comment is detected outside of a marked code block 
        Check('any', 'any', 'err',  'warn', 'none', any_rfc2119_info_missing), # 2119 keywords occur, but neither the matching boilerplate nor a reference to 2119 is missing 
        Check('any', 'any', 'warn', 'warn', 'none', any_rfc2119_boilerplate_missing), # 2119 keywords occur, a reference to 2119 exists, but matching boilerplate is missing 
        Check('any', 'any', 'warn', 'warn', 'none', any_rfc2119_boilerplate_extra), # 2119 boilerplate is present, but document doesn't use 2119 keywords 
        Check('any', 'any', 'comm', 'comm', 'none', any_rfc2119_bad_keyword_combo), # badly formed combination of 2119 words occurs (MUST not, SHALL not, SHOULD not, not RECOMMENDED, MAY NOT, NOT REQUIRED, NOT OPTIONAL) 
        Check('any', 'any', 'err',  'err',  'none', any_rfc2119_boilerplate_lookalike), # text similar to 2119 boilerplate occurs, but doesn't reference 2119 
        Check('any', 'any', 'warn', 'warn', 'none', any_rfc2119_keyword_lookalike), # NOT RECOMMENDED appears, but is not included in 2119-like boilerplate 
        Check('any', 'any', 'comm', 'comm', 'none', any_abstract_update_info_missing), # Abstract doesn't directly state it updates or obsoletes each document so affected (Additional comment if Abstract mentions the document some other way) 
        Check('any', 'any', 'comm', 'comm', 'none', any_abstract_update_info_extra), # Abstract states it updates or obsoletes a document not declared in the relevant field previously 
        Check('any', 'any', 'warn', 'warn', 'none', any_authors_addresss_grammar), # Author's address section title misuses possessive mark or uses a character other than a single quote 
        Check('any', 'any', 'warn', 'warn', 'warn', any_reference_not_used), # a reference is declared, but not used in the document 
        Check('any', 'any', 'err',  'warn', 'none', any_reference_is_downref), # a reference appears to be a downref (noting if reference appears in the downref registry) 
        Check('any', 'any', 'comm', 'comm', 'none', any_reference_status_unknown), # a normative reference to an document of unknown status appears (possible downref) 
        Check('any', 'any', 'err',  'warn', 'none', any_reference_is_obsolete_norm), # a normative or unclassified reference is to an obsolete  document 
        Check('any', 'any', 'comm', 'comm', 'none', any_reference_is_obsolete_info), # an informative reference is to an obsolete document 
        Check('any', 'any', 'warn', 'warn', 'none', any_reference_is_draft_rfc), # a reference is to a draft that has already been published as an rfc 
        Check('any', 'any', 'warn', 'warn', 'none', any_sourcecode_no_license), # A code-block is detected, but the block does not contain a license declaration 

    #3.1.1 Filename Checks
    #---------------------

        Check('any', 'any', 'err',  'err',  'err',  any_filename_base_bad_characters), # filename's base name contains characters other than digits, lowercase alpha, and dash 
        Check('any', 'any', 'err',  'err',  'err',  any_filename_ext_mismatch), # filename's extension doesn't match format type (.txt, .xml) 
        Check('any', 'any', 'err',  'err',  'err',  any_filename_base_not_docname_), # filename's base name doesn't match the name declared in the document 
        Check('any', 'any', 'err',  'err',  'err',  any_filename_too_long), # filename (including extension) is more than 50 characters 

    #3.1.2 Metadata checks
    #---------------------

        Check('any', 'any', 'warn', 'warn', 'none', any_obsoletes_obsolete_rfc), # Document claims to obsolete an RFC that is already obsolete 
        Check('any', 'any', 'warn', 'warn', 'none', any_updates_obsolete_rfc), # Document claims to update an RFC that is obsolete 
        Check('any', 'any', 'warn', 'warn', 'warn', any_doc_status_info_bad), # Document's status or intended status is not found or not recognized 
        Check('any', 'any', 'warn', 'warn', 'warn', any_doc_date_bad), # Document's date can't be determined or is too far in the past or the future (see existing implementation for "too far") 

    #3.1.3 If the document is an RFC
    #-------------------------------

        Check('any', 'rfc', 'comm', 'comm', 'none', any_section_iana_missing),  # Missing IANA considerations section 

    #3.1.4 If the document is an Internet-Draft (that is, not an RFC)
    #----------------------------------------------------------------

        Check('any', 'ids', 'err',  'err',  'err',  any_docname_malformed), # filename's base name  doesn't begin with 'draft', contains two consecutive hyphens, or doesn't have enough structure to contain the individual or stream, potentially a wg name, and a distinguishing name. (draft-example-00 is an error, but draft-example-filename is acceptable) 
        Check('any', 'ids', 'err',  'warn', 'none', any_section_iana_missing), # Missing IANA considerations section 

    #3.1.4.1 Additional metadata check
    #---------------------------------

        Check('any', 'ids', 'warn', 'warn', 'warn', any_doc_rev_unexpected), # version of document is unexpected (already exists, or leaves a gap) 

    #3.2 XML Input Specific Conditions
    #---------------------------------

        Check('xml', 'any', 'warn', 'warn', 'warn', xml_element_deprecated), # any deprecated elements or attributes appear 
        Check('xml', 'any', 'err',  'err',  'err',  xml_stream_contradiction), # metadata and document's 'submissionType' attribute state different streams 
        Check('xml', 'any', 'warn', 'warn', 'none', xml_source_code_in_sourcecode), # The text inside a <sourcecode> tag contains the string '<CODE BEGINS>' (Warn that the string is unnecessary and may duplicate what a presentation format converter will produce.) 
        Check('xml', 'any', 'warn', 'warn', 'none', xml_source_code_in_text), # The text inside any other tag contains the string '<CODE BEGINS>' (Warn that if the text is a code block, it should appear in a <sourcecode> element) 
        Check('xml', 'any', 'warn', 'warn', 'none', xml_text_looks_like_ref), # text occurs that looks like a text-document reference (e.g. [1], or [RFC...])  (if the text was really a reference it should be in an <xref> tag) 
        Check('xml', 'any', 'err',  'err',  'err',  xml_ipr_attrib_missing), # <rfc> ipr attribute is missing or not recognized 
        Check('xml', 'any', 'warn', 'warn', 'warn', xml_ipr_attrib_unknown), # ipr attribute is not one of "trust200902", "noModificationTrust200902", "noDerivativesTrust200902", or "pre5378Trust200902" 
        Check('xml', 'any', 'err',  'err',  'err',  xml_ipr_attrib_disallowed), # document is ietf stream and ipr attribute is one of "noModificationTrust200902" or "noDerivativesTrust200902" 
        Check('xml', 'any', 'warn', 'warn', 'warn', xml_workgroup_not_group), # <workgroup> content doesn't end with "Group" 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_update_info_bad),  # The "obsoletes" or "updates" attribute values of the <rfc> element are not comma separated strings of digits 
        Check('xml', 'any', 'err',  'err',  'err',  xml_update_info_noref), # The rfcs indicated by the "obsoletes" and "updates" attribute values of the <rfc> element are not included in the references section 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_xref_target_missing), # <xref> has no target attribute 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_xref_target_not_anchor), # <xref> target attribute does not appear as an anchor of another element 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_relref_target_missing), # <relref> has no target attribute 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_relref_target_not_anchor), # <relref> target attribute does not appear as an anchor of a <reference> element 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_relref_target_no_target), # A <reference> element pointed to by a <relref> target attribute does not itself have a target attribute 
#        Check('xml', 'any', 'warn', 'warn', 'warn', xml_artwork_multiple_content), # An element (particularly <artwork> or <sourcecode>) contains both a src attribute, and content 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_element_src_bad_schema), # The src attribute of an element contains a URI scheme other than data:, file:, http:, or https: 
        Check('xml', 'ids', 'warn', 'warn', 'warn', xml_ids_link_has_bad_content), # <link> exists with DOI or RFC-series ISDN for this document when the document is an Internet-Draft 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_section_bad_numbered_false), # <section> with a numbered attribute of 'false' is not a child of <boilerplate>, <middle>, or <back>, or has a subsequent <section> sibling with a numbered attribute of 'true' 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_xref_counter_bad_target), # An <xref> element with no content and a 'format' attribute of 'counter' has a 'target' attribute whose value is not a section, figure, table or ordered list number 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_relref_target_missing_anchor), # A <relref> element whose 'target' attribute points to a document in xml2rfcv3 format, and whose 'relative' attribute value (or the derived value from a 'section' attribute) does not appear as an anchor in that document 
        Check('xml', 'any', 'err',  'warn', 'err',  xml_artwork_svg_wrong_media_type), # An <artwork> element with type 'svg' has a 'src' attribute with URI scheme 'data:' and the mediatype of the data: URI is not 'image/svg+xml' 
        Check('xml', 'any', 'err',  'err',  'err',  xml_sourcecode_multiple_content), # A <sourcecode> element has both a 'src' attribute and non-empty content 
    #    Check('xml', 'any', 'err',  'err',  'err',  xml_artwork_binary_notempty), # An <artwork> element has type 'binary-art' and non-empty content 

    #3.2.1 If the document is an RFC
    #-------------------------------

        Check('xml', 'rfc', 'err',  'err',  'err',  xml_rfc_note_remove_true), # A <note> element has a 'removeInRFC' attribute with a value of 'true' 
        Check('xml', 'rfc', 'err',  'warn', 'err',  xml_rfc_artwork_wrong_type), # An <artwork> element has type other than 'ascii-art','call-flow','hex-dump', or 'svg' 

    #3.2.2 Boilerplate checks
    #------------------------

        Check('xml', 'any', 'warn', 'warn', 'warn', xml_text_has_boilerplate), # The text inside any tag sufficiently matches any of the boilerplate in the IETF-TLP-4 section 6a-6d  (such text should probably be removed and the ipr attribute of the rfc tag should be verified) 
        Check('xml', 'any', 'warn', 'warn', 'err',  xml_boilerplate_mismatch), # The value of the <boilerplate> element, if non-empty, does not match what the ipr, category, submission, and consensus <rfc> attributes would cause to be generated 

    #3.2.3 Autogenerated identifier checks
    #-------------------------------------

        Check('xml', 'rfc', 'warn', 'comm', 'warn', xml_rfc_generated_attrib_wrong), # The value of any present pn or slugifiedName attributes do not match what would be regenerated 

    #3.3 Text Input Specific Conditions
    #----------------------------------

        Check('txt', 'any', 'err',  'warn', 'none', txt_text_added_whitespace), # document does not appear to be ragged-right (more than 50 lines of intra-line extra spacing) 
        Check('txt', 'any', 'err',  'warn', 'warn', txt_text_lines_too_long), # document contains over-long lines (cut-off is 72 characters. Report longest line, and count of long lines) 
        Check('txt', 'any', 'warn', 'warn', 'none', txt_text_line_break_hyphens), # document has hyphenated line-breaks 
        Check('txt', 'any', 'warn', 'warn', 'none', txt_text_hyphen_space), # document has a hyphen followed immediately by a space within a line 
        Check('txt', 'any', 'warn', 'warn', 'none', txt_update_info_extra_text), # Updates or Obsoletes line on first page has more than just numbers of RFCs (such as the character sequence 'RFC') 
        Check('txt', 'any', 'warn', 'warn', 'none', txt_update_info_not_in_order), # Updates or Obsoletes numbers do not appear in ascending order 
        Check('txt', 'any', 'comm', 'comm', 'none', txt_doc_bad_magic), # document starts with PK or BM 
        Check('txt', 'any', 'comm', 'comm', 'none', txt_reference_style_mixed), # document appears to use numeric references, but contains something that looks like a text-style reference (or vice-versa) 
        Check('txt', 'any', 'warn', 'warn', 'warn', txt_text_ref_unused_), # a string that looks like a reference appears but does not occur in any reference section 
        Check('txt', 'any', 'err',  'err',  'err',  txt_abstract_numbered), # Abstract section is numbered 
        Check('txt', 'any', 'err',  'err',  'err',  txt_status_of_memo_numbered), # 'Status of this memo' section is numbered 
        Check('txt', 'any', 'err',  'err',  'err',  txt_copyright_notice_numbered), # Copyright Notice section is numbered 

    # 3.3.1 Boilerplate checks
    # ------------------------

        Check('txt', 'any', 'err',  'err',  'err',  txt_boilerplate_copyright_missing), # TLP-4 6.b.i copyright line is not present 
        Check('txt', 'any', 'warn', 'warn', 'warn', txt_boilerplate_copyright_year_wrong), # TLP-4 6.b.i copyright date is not this (or command-line specified) year 
        Check('txt', 'any', 'err',  'err',  'err',  txt_boilerplate_licence_missing), # TLP-4 6.b.i  or b.ii license notice is not present, or doesn't match stream 
        Check('txt', 'any', 'err',  'err',  'err',  txt_boilerplate_restrictions_found), # IETF stream document sufficiently matches TLP-4 6.c.i or 6.c.ii text (restrictions on publication or derivative works) 
        Check('txt', 'any', 'warn', 'warn', 'warn', txt_boilerplate_copyright_duplicate), # More than one instance of text sufficiently matching the TLP-4 6.b.i copyright line occurs 
        Check('txt', 'any', 'warn', 'warn', 'warn', txt_boilerplate_licence_duplicate), # More than one instance of text sufficiently matching either the TLP4 6.b.i or 6.b.ii license notice occurs 
        Check('txt', 'any', 'warn', 'warn', 'warn', txt_boilerplate_pre5378_missing_upd), # Document obsoletes or updates any pre-5378 document, and doesn't contain the pre-5378 material of TLP4 6.c.iii 
        Check('txt', 'any', 'warn', 'warn', 'warn', txt_boilerplate_pre5378_missing_prev), # Any prior version of the document might be pre-5378 and the document doesn't contain the pre-5378 material of TLP4 6.c.iii 

    #3.3.2 If the document is an Internet-Draft (i.e not an RFC)
    #-----------------------------------------------------------

        Check('txt', 'ids', 'warn', 'warn', 'none', txt_pages_too_long), # contains over-long pages (report count of pages with more than 58 lines)
        Check('txt', 'ids', 'err',  'err',  'err',  txt_head_label_missing), # doesn't say INTERNET DRAFT in the upper left of the first page 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_head_expiration_missing), # doesn't have expiration date on first and last page 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_boilerplate_working_doc_missing), # doesn't have an acceptable paragraph noting that IDs are working documents 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_boilerplate_6month_missing), # doesn't have an acceptable paragraph calling out 6 month validity 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_boilerplate_current_ids_missing), # doesn't have an acceptable paragraph pointing to the list of current ids 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_boilerplate_current_ids_duplicate), # has multiple occurrences of current id text 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_head_docname_missing), # document name doesn't appear on first page 
        Check('txt', 'ids', 'err',  'err',  'warn', txt_table_of_contents_missing), # has no Table of Contents 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_boilerplate_ipr_missing), # IPR disclosure text (TLP 4.0 6.a) does not appear 
        Check('txt', 'ids', 'err',  'err',  'err',  txt_boilerplate_ipr_not_first_page), # IPR disclosure text (TLP 4.0 6.a) appears after first page 
        Check('txt', 'ids', 'warn', 'warn', 'none', txt_pages_missing_formfeed), # pages are not separated by formfeeds 
        Check('txt', 'ids', 'comm', 'comm', 'comm', txt_pages_formfeed_misplaced), # 'FORMFEED' and '[Page...]' occur on a line, possibly separated by spaces (indicates NROFF post-processing wasn't successful) 
        Check('txt', 'ids', 'warn', 'warn', 'none', txt_text_bad_section_indentation), # section title occurs at an unexpected indentation 

    ]
