import urllib2
from HTMLParser import HTMLParser

class SegmentHTMLParser(HTMLParser):
    heading=['name','length','Data type','optional','repeat','table','desc']
    numberOfTables = 0
    addCell = False;
    rows=[];
    currentRow=[]
    def handle_starttag(self, tag, attrs):
        if (tag=='table'):
            self.numberOfTables = self.numberOfTables + 1
        if (tag=='td'):
            self.addCell = True

    def handle_endtag(self, tag):
        if (tag=='tr'):
            self.rows.append(self.currentRow)
            self.currentRow = []
        if (tag=='td'):
            self.addCell=False

    def handle_data(self, data):
        if (self.addCell):
            self.currentRow.append(data)

    def get_rows(self):
        return self.rows

    def init(self):
        self.numberOfTables=0
        self.addCell=False
        self.rows=[]
        self.currentRow=[]

def buildJSON(componentsArray):
    import json
    jsonMap = {}
    for componentDetailArray in componentsArray:
        if len(componentDetailArray)!=0:
            key = componentDetailArray[0].replace('.','-')
            jsonMap[key]=componentDetailArray

    return json.dumps(jsonMap, indent=2)

def writeToFile(file, segmentName, json):
    file.write("var " + segmentName + " = " + json + ";")
    file.write("\n")
    file.write("DB['" + segmentName + "'] = " + segmentName + ";")
    file.write("\n\n")


urlbase='http://hl7-definition.caristix.com:9010/Default.aspx?version=HL7%20v2.4&segment='
segments = [
'ABS',
'ACC',
'ADD',
'AFF',
'AIG',
'AIL',
'AIP',
'AIS',
'AL1',
'APR',
'ARQ',
'AUT',
'BLC',
'BLG',
'CDM',
'CM0',
'CM1',
'CM2',
'CNS',
'CSP',
'CSR',
'CSS',
'CTD',
'CTI',
'DB1',
'DG1',
'DRG',
'DSC',
'DSP',
'ECD',
'ECR',
'EDU',
'EQL',
'EQP',
'EQU',
'ERQ',
'ERR',
'EVN',
'FAC',
'FT1',
'GOL',
'GP1',
'GP2',
'GT1',
'IAM',
'IN1',
'IN2',
'IN3',
'INV',
'ISD',
'LAN',
'LCC',
'LCH',
'LDP',
'LOC',
'LRL',
'MFA',
'MFE',
'MFI',
'MRG',
'MSA',
'MSH',
'NCK',
'NDS',
'NK1',
'NPU',
'NSC',
'NST',
'NTE',
'OBR',
'OBX',
'ODS',
'ODT',
'OM1',
'OM2',
'OM3',
'OM4',
'OM5',
'OM6',
'OM7',
'ORC',
'ORG',
'PCR',
'PD1',
'PDA',
'PDC',
'PEO',
'PES',
'PID',
'PR1',
'PRA',
'PRB',
'PRC',
'PRD',
'PSH',
'PTH',
'PV1',
'PV2',
'QAK',
'QID',
'QPD',
'QRD',
'QRF',
'QRI',
'RCP',
'RDF',
'RDT',
'RF1',
'RGS',
'RMI',
'ROL',
'RQ1',
'RQD',
'RXA',
'RXC',
'RXD',
'RXE',
'RXG',
'RXO',
'RXR',
'SAC',
'SCH',
'SID',
'SPR',
'STF',
'TCC',
'TCD',
'TXA',
'UB1',
'UB2',
'URD',
'URS',
'VAR',
'VTQ'];

#segments = ['AL1', 'PV1']
parser = SegmentHTMLParser()
f = open('DB.js', 'w')
f.write("var DB = {};\n")

for segment in segments:
    url = urlbase + segment
    print segment + ","
    response = urllib2.urlopen(url)
    html = response.read()
    parser.init();
    parser.feed(html)
    json = buildJSON(parser.get_rows())
    writeToFile(f, segment, json)

f.close()
