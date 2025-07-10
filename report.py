#/usr/bin/python
import os
from stopwatch import  *
from dbmanager import *
from html import escape
from random import *
import string
import math

class Report():

    def __init__(self):
        self.watch = StopWatch()

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.report = ""

        self.header = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html  xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>digikamstat</title>
<style>
 body
 {
     background-color:#ffffff;
     font-family: 'Open Sans', sans-serif;
     font-size:12pt;
 }
 
h1
{
        width:100%;
        margin-bottom:1.5em;
        border-bottom:1px solid black;
}

h1, h2, h3
{
    text-weight:bold;
}

.warning
{
    color:#dd7777;
}

h2, h3
{
        text-align:center;
}

#contents
{
width: 25%;
background-color:#f0f0f0;
padding:0.5em;
border:1px solid silver;
}

img.logo
{
        float:right;
        margin-top:-6em;
}

div.svgcontainer
{
    margin:0.5em auto;
    width:800px;
}

table.default
{
    width: 85%;
    margin:auto;
}


/* from YAML */
table { width: auto; border-collapse:collapse; margin-bottom: 0.5em; border-top: 2px #666 solid; border-bottom: 2px #666 solid; }

table.full { width: 100%; }
table.fixed { table-layout:fixed; }

th, td { padding: 0.5em; }
tbody th { background: #e3e3e3;}

tbody th { border-bottom: 1px solid #bbb; text-align: left; }
tbody td { border-bottom: 1px solid #bbb; }

tbody tr:hover td { background: #e3e3e3; }

tr:nth-child(even) {background: #fff}
tr:nth-child(odd) {background: #f0f0f0}


/* TABS */

.tabs {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons that are used to open the tab content */
.tabs button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
}

/* Change background color of buttons on hover */
.tabs button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tabs button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
  animation: fadeEffect 1s; /* Fading effect takes 1 second */
}

/* Go from zero to full opacity */
@keyframes fadeEffect {
  from {opacity: 0;}
  to {opacity: 1;}
}

@media print {

    body {
        margin: 1em;
        color: #000;
        background-color: #fff;
        zoom: 70%;
      }
    
    .tabs
    {
        display: none !important; 
    }
    
    .tabcontent {
      display: block !important; 
      padding: 6px 12px;
      border: none;
    }
}
</style>
</head>
<body>
<a name="top"></a>"""

        self.script ="""
<script  type="text/javascript">
// <![CDATA[
function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  
  tabcontent = document.getElementsByClassName("tabcontent");
  
  //hide all tabs
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  
  //activate the current button
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  
  //show the activated tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

// activate the first tab and the first button
document.getElementsByClassName("tabcontent")[0].style.display = "block"
document.getElementsByClassName("tablinks")[0].className += " active";
// ]]>
</script>
"""

        self.header += """<h1>DigikamSTAT</h1>\n<img class='logo' src='%s/data/digikam-logo.png' />\n""" % (self.current_dir)

        self.contents = []
        self.tabs = []
        self.tab_open = 0
        self.footer = "</body></html>"

        self.color = 0

    def update_image(self, Image):
        print("updateImage")

    def get_report(self):
        
        contents_html = ''
        
        if(len(self.contents) > 0):
            contents_html = "<div class=\"tabs\">\n"
            
            for i in self.contents:
                #contents_html +="""<li><a href=\"#%s\">%s</a></li>\n"""  % (i[0], i[1])
                contents_html +="""<button class="tablinks" onclick="openTab(event, '%s')">%s</button>\n"""  % (i[0], i[1])
                 
            contents_html += "</div>\n"

        if(self.tab_open == 1):
            self.report += "</div>"
            
        report = self.header + contents_html + self.report + self.script + self.footer
        
        self.debug_html(report)
        
        return (report)

    def debug_html(self,  data):

        self.watch.start("debug HTML")

        output = open("report.xhtml", "w")
        output. write(data)
        output.close()

        self.watch.stop("debug HTML")

    def clear_all(self):
        self.contents = []
        self.report = ""
        self.tab_open = 0;

    def add_table(self, data,  css='default'):

        self.report += """<table class="%s">
        <tbody>
        <tr>
        """ % css

        header = data.pop(0)

        for cell in header:
           self.report += """<th>%s</th>\n""" % cell

        self.report += "</tr>"

        for row in data:
            self.report += "<tr>\n"

            for cell in row:
                self.report += """<td>%s</td>\n""" % cell

            self.report += "</tr>\n"

        self.report += "</tbody>\n</table>\n"

    def add_text(self, text):
        self.report += text
        
    def add_headline(self, text,  anchor = 'none',  anchorTitle = 'none'):
        if anchor != 'none':
            self.report += """<a name=\"%s\"></a>"""  % (anchor)
            self.contents.append([anchor,  anchorTitle])
            
        self.report += text
        
    def add_tab(self, headline,  tab_id,  tab_title):
        
        self.contents.append([tab_id,  tab_title])
        
        #check if a tab is open, close it before open a new
        if(self.tab_open == 1):
            self.report += "</div>"
            
        self.report += "<div id=\"%s\" class=\"tabcontent\">" % (tab_id)
        self.tab_open = 1
        self.report += "<h2>%s</h2>" % (headline)
        
    def add_toplink(self):
        self.report += "<p><a href=\"#top\">&#8673; Go to top</a></p>";
        
    def add_hor_graph(self, title,  data,  sum,  text_width = 48):

        self.watch.start("add Horizontal Graph")

        width = 800
        #text_width = 48
        border_left = 2
        border_right = 10
        border_top = 25
        border_bottom = 25
        axis_overpaint = 5
        bar_height = 10
        bar_margin = 8
        num_sections = 4
        
        if (sum > 0):
            numer_count = int(math.log10(sum))
            power = 10 ** numer_count
            sum -= sum % (power * -1)
        else:
            sum = 10
            
        height = border_top + border_bottom + len(data) * (bar_height + bar_margin)

        self.report += """<div class="svgcontainer"><svg xmlns="http://www.w3.org/2000/svg" width="100%%" height="100%%"  viewBox="0 0 %s %s">
        <rect x="0" y="0" width="%s" height="%s" stroke="#666666" stroke-width="1" fill="#eaeaea" />""" % (
                width,  height,
                width,  height, )

        self.report += """<text x="%s" y="%s" font-family="Verdana" font-size="12" fill="black" text-anchor="middle">%s</text>""" % (width / 2, border_top - axis_overpaint - 5 , title)

        color = ['#ffffff', '#f0f0f0', '#ffffff', '#f0f0f0']

        for i in  range(num_sections):
            percent = float(width - border_left - border_right - text_width)  /  num_sections
            start = border_left + text_width + (percent *  i)
            self.report += """<rect x="%s" y="%s" width="%s" height="%s" stroke="%s" stroke-width="0" fill="%s" />""" % (
            start,  border_top - axis_overpaint,  percent ,  height - border_top - border_bottom + axis_overpaint,
            color[i],  color[i] )

            self.report += """<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1" stroke="#444444" stroke-linecap="round" />""" % (
            start + percent,  border_top - axis_overpaint,  start + percent,   height - border_bottom)
            
            self.report += """<text x="%s" y="%s" font-family="Verdana" font-size="10" fill="black"   text-anchor="middle">%s</text>""" % (start, height - border_bottom + 14 ,  round(sum / num_sections * i))
        
        #last text in horizontal axis
        start = border_left + text_width + (percent *  num_sections)
        self.report += """<text x="%s" y="%s" font-family="Verdana" font-size="10" fill="black"   text-anchor="end">%s</text>""" % (start, height - border_bottom + 14 ,  sum)


        self.report += """<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1" stroke="#000000" stroke-linecap="round" />
        <line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1" stroke="#000000" stroke-linecap="round" />
        """ % (border_left + text_width,  border_top - axis_overpaint,  border_left + text_width,  height - border_bottom + axis_overpaint,
               border_left + text_width - axis_overpaint,  height - border_bottom, width - border_right,  height - border_bottom)

        for i in range(len(data)):
            y = i * (bar_height + bar_margin) + border_top
            barwidth = float(data[i][1]) / float(sum) * (width - border_left  - text_width - border_right)

            self.report += """<text x="%s" y="%s" font-family="Verdana" font-size="10" fill="black"   text-anchor="end">
            %s
            </text>""" % (text_width,  y + bar_height - 2,  data[i][0])

            self.report += """<rect x="%s" y="%s" width="%s" height="10" stroke="#000000" stroke-width="1" fill="%s" />""" % (text_width + border_left, y, barwidth, self.get_svg_color())

        self.report += """</svg></div>"""

        self.watch.stop("add Horizontal Graph")

    def escape_html(self, text):
        text = escape(text)
        filtered_text = ''.join(filter(lambda x: x in string.printable, text))
        return filtered_text

    def get_svg_color(self):

        self.color += 10

        if(self.color > 359):
            self.color = 0

        (r, g, b) = self.hsv_to_rgb(self.color)

        return "#%02X%02X%02X" % (int(round(r * 255, 0)),  int(round(g * 255, 0)), int(round(b * 255, 0)))


    def hsv_to_rgb(self, h,  s = 1,  v = 1):

        r = 0
        g = 0
        b = 0

        if(s == 0):
            r = v
            g = v
            b = v

        h /= float(60)
        i = int(h // 1)
        f = h - i
        p = v * ( 1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * ( 1 - f ))


        if(i == 0):
            r = v
            g = t
            b = p

        elif(i == 1):
            r = q
            g = v
            b = p

        elif(i == 2):
            r = p
            g = v
            b = t

        elif(i == 3):
            r = p
            g = q
            b = v

        elif(i == 4):
            r = t
            g =p
            b = v

        else:
            r = v
            g = p
            b = q

        return r, g, b
