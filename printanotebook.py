#**PRINTING TIPS ON LASER PRINTER** In my case, using a Brother HL-L5200DW
#printer, the best printing results were obtained at the highest resolution
#(HQ1200 dpi), with the "text" mode selected (and not the "graphics" mode).

import glob
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re
import sys
from datetime import date
import math

cwd = os.getcwd()

#The "problem" variable is initialized to "False"
#and will be set to "True" should the code encounter
#any problems, in order to give the user relevant error
#messages along the  way.
problem = False

#The title passed in after the "title:"
#argument will be checked to see if it
#has instances of two spaces ("  "). 
#If so, the version with the extra
#spaces will be stored in "title_with_spaces"
#and the version with at most one space
#in-between words will be stored in the
#"title" variable.
title = None
title_with_spaces = None
#If there were instances of two spaces
#(" ") in the title or if the title
#was too long to fit on the title
#page, the title will be split
#by the code so that it can
#span multiple lines. The longest
#line will be stored in the variable
#"longest_title_line" so that the
#font size may be automatically
#asjusted to fit within the 
#available space on the page.
longest_title_line = None
#The user has the option to go with the automatic
#splitting of the title or author, or manually indicate where the
#line breaks should be by placing at least two successive
#space in-between words that are to be split onto different lines.
custom_title_line_breaks = False
custom_author_line_breaks = False
author = None
author_with_spaces = None
longest_author_line = None

#If the title needs to be split
#in order to fit in the title page,
#the value of "asjusted_title_rtf"
#will be set to the string containing
#a "\line" linebreak RTF command and
#will be updated in text[title_index].
#A similar approach is taken for the
#title and author name on the cover.
adjusted_title_cover = None
adjusted_author_cover = None
#"spine_text" is initialized as "None",
#and a value can be supplied by the user
#should they want to use different text
#than the abbreviated author name, followed
#by a hyphen and the book title.
spine_text = None
#The users may choose to perforate their notebook
#pages and covers to bind them using standard
#ring binders or a discbound option. If so,
#the value of "perforated_cover" will be set to "True".
perforated_cover = False
#Should the cover title need to be split,
#the default line spacing in-between title lines
#is initialized at 40 pixels, and may be altered
#by the user by specifying the number of pixels
#after the "cover_title_line_spacing:" argument
#when running the code. The same can be done for
#the author text ("cover_author_line_spacing:"),
#with a default spacing of 30 px (40 px * 0.75 = 30 px)
cover_title_line_spacing = 40
cover_author_line_spacing = 30
cover_box_color = None
cover_text_color = None
cover_trim_width = 0.25
#The "cover_line" variable determines whether
#a dark border will be present on the cover,
#before the white trim. The default setting
#includes such a border, but as the users
#may wish to trim their pages using a stack
#page guillotine cutter, and the presence of
#a dark line would likely leave behind some
#uneven line after cutting, they may wish to remove
#such a line by passing the argument "no_cover_line"
#when running the Python code.
cover_line = True
#An extra 20 pixels are added to the cover width,
#to account for binding irregularities and the
#thickness of the glue:
cover_extra_pixels = 20
#The "pixels_from_bottom_cover_spine" variable
#determines how many pixels are added to the
#starting "y" coordinate (in the rotated image)
#from the bottom of the spine box to reach the
#point where the spine text will start to be written.
#Negative values will bring the text down.
pixels_from_bottom_cover_spine = 0
#A similar approach is taken with the variable
#"pixels_from_left_cover_spine" to determine how
#many pixels are added to the starting "x" coordinate
#(in the rotated image) from the left edge of the
#spine box to reach the point where the spine
#text will start to be written. Negative values
#will bring the text left.
pixels_from_left_cover_spine = 0
#The "pixels_from_top_cover_title_box" variable
#determines how many pixels are added to the
#starting "y" coordinate (in the unrotated image)
#from the top of the cover title box to reach the
#point where the cover title text will start to be
#written. Negative values will bring the text up.
pixels_from_top_cover_title_box = 0
#A similar approach is taken with the variable
#"pixels_from_left_cover_title_box" to determine how
#many pixels are added to the starting "x" coordinate
#(in the unrotated image) from the left edge of the
#cover title box to reach the point where the cover
#title text will start to be written. Negative
#values will bring the text left.
pixels_from_left_cover_title_box = 0

number_of_pages = 192
inches_per_ream_500_pages = None
cm_per_ream_500_pages = None

grayscale = False

#The "cover_title_font_size" is initialized
#at 125 pixels and the code will determine the largest
#font size that fits within the front cover box.
#The user can specify another starting value for
#"cover_title_font_size".
cover_title_font_size = 125
#The spacing on the cover in-between
#the title and the author name will be
#a certain proportion of the cover title
#height and is set to 20% by default.
cover_spacing_title_height_ratio = 0.20
#The "max_author_title_font_ratio" variables
#determines the max ratio between the title
#headings font size and that of the author name,
#to provide a starting font size while automatically
#adjusting the font size to the available space.
max_author_title_font_ratio = 0.75
#The "cover_author_font_size" is initialized
#at 94 pixels and the code will determine the largest
#font size that fits within the front cover box.
#The user can specify another starting
#value for "cover_author_font_size"
cover_author_font_size = 94
#Similarly, the "spine_font_size"
#default value is set at 100 pixels,
#and the code will determine the largest
#font size that fits within the spine.
#The user can specify another starting
#value for "spine_font_size".
spine_font_size = 100


no_merging = False
list_of_page_images = []
#The "heading_text_left" and "heading_text_right" variables
#are initialized to "None" and will be set to the user's
#input text. These two variables may have the same value,
#if the user input the titles with "heading_text:Title".
#The default font sizes for the header is set at 75 px
#and that of the footer containing the page numbers is
#initialized at 60 px. The user can change these values,
#along with the text color "heading_text_color" and
#"page_numbers_text_color".
heading_text_left = None
heading_text_right = None
heading_font_size = 75
heading_text_color = "LightSlateGrey"
page_numbers_font_size = 60
page_numbers_text_color = "LightSteelBlue"

#The headers can either be located in the outer corners
#of the pages "heading_corner", or centerd (default setting).
heading_corner = False
#All of the pages included in the table of contents
#are listed in "TOC_pages_list", with a default of
#eight pages. It is important that the number of pages
#for the table of contents be an even number, so that
#the first of the numbered notebook pages lands on
#a right-hand page. For this reason, when the user
#inputs an odd-numbered value for "TOC_pages", it
#will automatically be incremented by one page count.
TOC_pages = 8
TOC_pages_list = list(range(1,9))
#The font size for the "Subject" heading in the table of contents
#("TOC_subject_text") is set to sixty pixels by default and the color
#is set to "LightSlateGrey", both of which may be changed by the user.
#The same goes for the "Pages" heading. The user can also change the
#text of these headings, as well as that of the "Contents" heading.
TOC_subject_font_size = 60
TOC_subject_text = "Subject"
TOC_subject_text_color = "LightSlateGrey"
TOC_pages_font_size = 60
TOC_pages_text = "Page"
TOC_pages_text_color = "LightSlateGrey"
TOC_line_spacing = None
TOC_heading_font_size = 75
TOC_heading_text = "Contents"
TOC_heading_text_color = "LightSlateGrey"
dot_y_coordinates = None
line_y_coordinates = None
line_y_coordinates_TOC = None
line_y_coordinates_graph = None
#The "page_numbers" variable is set to "None", and will
#be initialized at 1 and incremented by 1 every time a
#page number is written in the footer, should the user
#add the page numbering arguments. The "page_numbers_left",
#would only add page numbering on the left pages, and vice
#versa for "page_numbers_right". The starting page number
#is set to 1.
page_numbers = None
page_number = 1
page_numbers_left = None
page_numbers_right = None

#The "heading_top_margin_y_pixel" maps to the "y"
#pixel where the heading text is written.

heading_top_margin_y_pixel = 0.60*300

#Similarly, "page_numbers_bottom_margin_y_pixel" maps to the
#"y" pixel where the page numbers are written.

#The variable "page_numbers_bottom_margin_y_pixel" designates
#the "y" coordinate mapping to the vertical middle point of the
#page numbers. By default, this variable is set as "None", and the
#user can either set it manually, or the code will determine whether there
#is sufficient space to vertically center the page numbers in the space
#in-between the last horizontal line and the bottom of the page. Should
#there be less than 75 pixels below the page number for it to be
#vertically centered, the code will automatically bring the text up,
#such that the lowest "y" pixel of the page number is above 75 pixels
#from the bottom of the page, thereby respecting the default 0.25 inch
#non-printable area for most printers.
page_numbers_bottom_margin_y_pixel = None

#The "top_margin_y_pixel" maps to the "y" pixel
#where the lines or dots start being drawin on
#the pages.
top_margin_y_pixel = 0.95*300
#Similarly, the "bottom_margin_y_pixel" maps to
#the "y" pixel where the lines and dots end.
bottom_margin_y_pixel = 2550-(0.60*300)
user_provided_bottom_margin_y_pixel = False
#The variables "left_margin_x_pixel"  and
#"right_margin_x_pixel" map to the "x"
#pixels where the lines and dots start and
#stop being drawn on the pages, respectively.
#An extra pixel is added to the "left_margin_x_pixel"
#and subtracted from "right_margin_x_pixel" in order
#to allow for a full 0.25 inch margin.
left_margin_x_pixel = 0.25*300 + 1
right_margin_x_pixel = 3300-(0.25*300) - 1
user_provided_right_margin = False
#The "gutter_margin_width_pixels" designates the
#width (in pixels) of the gutter margins of the
#notebook. They are set to the pixel equivalent
#of an eighth of an inch, so they won't be noticeable
#when opening a bound book.
gutter_margin_width_pixels = 0.125*300
user_provided_gutter_margin = False
#The various page formattings (lines,
#graph paper, dots) are initialized as
#False, so that the notebook would have
#blank page by default, unless the user
#specifies a certing formatting element.
#Of note, the formatting elements can be
#applied only to odd (right) pages, only
#to even (left) pages, or to both pages
#(variables without mention of right or left).
college_ruled = False
college_ruled_left = False
college_ruled_right = False
wide_ruled = False
wide_ruled_left = False
wide_ruled_right = False
custom_ruled = False
custom_ruled_left = False
custom_ruled_right = False
custom_line_distance_inches = None
graph_paper = False
graph_paper_left = False
graph_paper_right = False
dot_grid = False
dot_grid_left = False
dot_grid_right = False
#ScriptReader is another github repo that
#enables the user to train a OCR convoluted
#neural network model on their handwriting,
#using customized dot grid sheets generated
#with PrintANotebook. If the user enters the
#appropriate parameters, "scriptreader" will
#be set to "True".
scriptreader_left = False
scriptreader_right = False
scriptreader = False
#The "scriptreader_acetate" option will generate
#notebook pages with dot grids for printing on
#acetates (preferably on a laser printer), such
#that the pages may be written on with an erasable
#marker, submitted to OCR and erased afterwards.
#The user would need to print the pages up to the halfway
#point on the acetates, then flip the stack of acetates
#and print the remaining pages on the other side, thus
#allowing to generate two right hand pages with the same
#gutter margin from a single acetate sheet. A vertical
#dotted line will indicate where the user should cut the acetate,
#in order to later perforate the half-letter acetate sheets
#and use them in a binder.
scriptreader_acetate = False
#The variable "pixels_above_black_squares" stores the number
#of pixels above the black squares on the ScriptReader pages.
pixels_above_black_squares = 0.25*300
#The list of line indices where characters will be segmented
#if the ScriptReader option is selected ("text_line_numbers")
#will be initialized including the zero index if the "scriptreader"
#mode is selected, as the first line of text needs to be on the first 
#line, and then at a regular interval thereafter after that. There is 
#a default of three empty lines in-between every line of text, to minimize
#the overlapping of ascenders and descenders of adjacent text lines.
text_line_numbers = None
#The user can choose to add a design to one or
#both pages by adding the JPEG image to the
#working folder, of which the file name starts
#with "page", so that the code might distinguish
#it from the cover image (of which the file name
#begins with "cover"). The user would then pass in
#"custom_template_both_pages", "custom_template_left_page"
#or "custom_template_right_page" when running the code.
custom_template_left_page = False
custom_template_right_page = False
#The line and graph lines colors are
#set to "Gainsboro" by default and
#may be changed by the user.
line_color = "Gainsboro"
TOC_line_color = "Gainsboro"
graph_line_color = "Gainsboro"
#If the user defines the dot fill color
#as white, the outline color can be some
#other color
dot_fill_color = "LightSlateGrey"
dot_outline_color = "LightSlateGrey"
#The diameter of the dots (in pixels)
#is defined by the variable
#"dot_diameter_pixels".
dot_diameter_pixels = 5
#If the user defines the dot fill color
#as white, the outline color can be some
#other color, and the "dot_line_width"
#will determine the boldness of that
#outline.
dot_line_width = 1
#The spacing in-between dots is
#set to a fifth of an inch by
#default and may be changed by
#the user.
inches_between_dots = 0.20
#The line width of ruled lines
#and graph lines are set to 5
#pixels by default an may be
#changed by the user.
line_width = 5
TOC_line_width = 5
graph_line_width = 5
#The number of squares per inch
#("squares_per_inch") is set to
#"None" by default and the user
#must specify this value when
#selecting the graph paper
#formatting. For example, for
#four squares per inch, with a
#bold line every four squares and
#with a bold line thickness 1.75 times
#that of the default 5 pixels, the
#user would enter "graph_paper:4:4:1.75",
#where the first number is "squares_per_inch",
#the second digit is "bold_line_every_n_squares",
#and the final number is "line_boldness_factor"
squares_per_inch = None
line_boldness_factor = 1
bold_line_every_n_squares = 5


#The default left and right
#margins on the cover page are set to 0.75 inches
#from the edges of the half-letter page (5.5 inches wide).
#These margins correspond to the space in-between the
#left-hand side of the white rectangle on the cover and 
#the start of the spine dark rectangle (left margin) or the 
#right-hand side of the white rectangle on the cover and
#the beginning of the 1/4 inch white trim around the book
#cover (right margin). The trim width will be factored
#in later in the code when drawing the dark and light
#rounded rectangle and the title and author on the cover
#("cover_trim_width").

#The left margin can be determined by subtracting the space
#in-between the margins (4.75 inches) from the right edge
#pixel count: (4200 - 4.75*300) = 2775 px, with 300 being the
#resolution (300 pixels per inch).
left_margin_cover_textbox = 2775

#The right margin can simply be calculated given the pixel
#width of the canvas: 4220-(0.75*300) = 3995 px, with 300 being the
#resolution (300 pixels per inch).
right_margin_cover_textbox = 3995

#The top margin of the text box on the cover page can
#be determined by adding a 25% of the vertical
#pixels to the starting y corrdinate of 0. (0+(2550/4)).
top_margin_cover_textbox = 640

#A recycling symbol will be added to the back cover
#of the notebook, if the code could locate the 
#image in the "Recycling Symbol" subfolder in the 
#working folder.
recycling_symbol = None

#The notebooks can be printed in A4 format
#The user then needs to pass in the "A4" argument
#when running the code, before specifying any margins
#on the notebook pages, so that the code could apply
#the right margin settings to the A4 pages.
A4 = False


if len(sys.argv) > 1:
    #The "try/except" statement will
    #intercept any "ValueErrors" and
    #ask the users to correctly enter
    #the desired values for the variables
    #directly after the colon separating
    #the variable name from the value.
    try:
        for i in range(1, len(sys.argv)):
            sys_argv_i_lower_strip = sys.argv[i].lower().strip()
            length_sys_argv_i_lower_strip = len(sys_argv_i_lower_strip)
            if sys_argv_i_lower_strip[:6] == "title:":
                title = sys.argv[i].strip()[6:].strip()
                #The title passed in after the "title:"
                #argument will be checked to see if it
                #has instances of two spaces ("  "). 
                #If so, the version with the extra
                #spaces will be stored in "title_with_spaces"
                #and the version with at most one space
                #in-between words will be stored in the
                #"title" variable.
                if "  " in title:
                    title_with_spaces = title
                    title = re.sub(r"[ ]{2,}", " ", title)
            elif sys_argv_i_lower_strip[:7] == "author:":
                author = sys.argv[i].strip()[7:].strip()
                author_names = re.split(r"( )", author)
                for j in range(len(author_names)):
                    author_names[j] = author_names[j].capitalize()
                author = "".join(author_names)
                if "  " in author:
                    author_with_spaces = author
                    author = re.sub(r"[ ]{2,}", " ", author)
            elif sys_argv_i_lower_strip[:16] == "number_of_pages:":
                number_of_pages = int(sys_argv_i_lower_strip[16:].strip())
            elif sys_argv_i_lower_strip[:26] == "inches_per_ream_500_pages:":
                make_cover = True
                inches_per_ream_500_pages = float(sys_argv_i_lower_strip[26:].strip())
            elif sys_argv_i_lower_strip[:22] == "cm_per_ream_500_pages:":
                make_cover = True
                cm_per_ream_500_pages = float(sys_argv_i_lower_strip[22:].strip())
                inches_per_ream_500_pages = cm_per_ream_500_pages/2.54
            elif sys_argv_i_lower_strip in ["grayscale", "greyscale"]:
                grayscale = True
            elif sys_argv_i_lower_strip[:16] == "cover_box_color:":
                cover_box_color = sys_argv_i_lower_strip[16:].strip()
                cover_box_rbg = re.findall(r"(\d+)", cover_box_color)
                #If an RGB value has been provided for "cover_box_color",
                #then the recycling symbol on the back cover will be filled
                #with the same color.
                if cover_box_rbg != [] and len(cover_box_rbg) == 3:
                    recycling_symbol_color = (int(cover_box_rbg[0]), int(cover_box_rbg[1]), int(cover_box_rbg[2]), 255)
                #If a color name (ex: "Green") has been provided,
                #then the recycling symbol at the back of the book
                #will be filled in white and its outline will be
                #dark gray.
                else:
                    recycling_symbol_color = (255,255,255,255)
                    recycling_symbol_outline_color = (105,105,105,255)     
            elif sys_argv_i_lower_strip[:17] == "cover_text_color:":
                cover_text_color =  sys_argv_i_lower_strip[17:].strip()
                cover_text_rbg = re.findall(r"(\d+)", cover_text_color)
                #If an RGB value has been provided for "cover_text_color",
                #then the recycling symbol on the back cover will be outlined
                #with the same color.
                if cover_text_rbg != [] and len(cover_text_rbg) == 3:
                    recycling_symbol_outline_color = (int(cover_text_rbg[0]), int(cover_text_rbg[1]), int(cover_text_rbg[2]), 255)
                #If a color name (ex: "Green") has been provided,
                #then the recycling symbol at the back of the book
                #will be outlined in dark gray.
                else:
                    recycling_symbol_outline_color = (105,105,105,255)
            elif sys_argv_i_lower_strip[:22] == "cover_title_font_size:":
                cover_title_font_size = round(int(sys_argv_i_lower_strip[22:].strip()))
            elif sys_argv_i_lower_strip[:25] == "cover_title_line_spacing:":
                cover_title_line_spacing = round(int(sys_argv_i_lower_strip[25:].strip()))
            elif sys_argv_i_lower_strip[:23] == "cover_author_font_size:":
                cover_author_font_size = round(int(sys_argv_i_lower_strip[23:].strip()))
            elif sys_argv_i_lower_strip[:26] == "cover_author_line_spacing:":
                cover_author_line_spacing = round(int(sys_argv_i_lower_strip[26:].strip()))
            elif sys_argv_i_lower_strip[:16] == "spine_font_size:":
                spine_font_size = round(int(sys_argv_i_lower_strip[16:].strip()))
            elif sys_argv_i_lower_strip[:33] == "cover_spacing_title_height_ratio:":
                cover_spacing_title_height_ratio = float(sys_argv_i_lower_strip[33:].strip())
            elif sys_argv_i_lower_strip[:17] == "cover_trim_width:":
                cover_trim_width = float(sys_argv_i_lower_strip[17:].strip())
            elif sys_argv_i_lower_strip[:20] == "cover_trim_width_cm:":
                cover_trim_width = float(sys_argv_i_lower_strip[20:].strip())/2.54
            elif sys_argv_i_lower_strip[:13] == "no_cover_line":
                cover_line = False
            elif sys_argv_i_lower_strip[:19] == "cover_extra_inches:":
                inches = float(sys_argv_i_lower_strip[19:].strip())
                cover_extra_pixels = round(inches*300)
            elif sys_argv_i_lower_strip[:15] == "cover_extra_cm:":
                cm = float(sys_argv_i_lower_strip[15:].strip())
                cover_extra_pixels = round(cm/2.54*300)
            elif sys_argv_i_lower_strip[:31] == "pixels_from_bottom_cover_spine:":
                pixels_from_bottom_cover_spine = int(sys_argv_i_lower_strip[31:].strip())
            elif sys_argv_i_lower_strip[:29] == "pixels_from_left_cover_spine:":
                pixels_from_left_cover_spine = int(sys_argv_i_lower_strip[29:].strip())
            elif sys_argv_i_lower_strip[:32] == "pixels_from_top_cover_title_box:":
                pixels_from_top_cover_title_box = int(sys_argv_i_lower_strip[32:].strip())
            elif sys_argv_i_lower_strip[:33] == "pixels_from_left_cover_title_box:":
                pixels_from_left_cover_title_box = int(sys_argv_i_lower_strip[33:].strip())
            elif sys_argv_i_lower_strip[:11] == "spine_text:":
                spine_text = sys.argv[i].strip()[11:].strip()
            #The elif statements below are specific to PrintANotebook
            elif sys_argv_i_lower_strip[:12] == "left_margin:":
                inches = float(sys_argv_i_lower_strip[12:].strip())
                #An extra pixel is added in order to allow for
                #a full "inches" margin and to start drawing 
                #one pixel after that.
                left_margin_x_pixel = round(inches*300) + 1
                user_provided_left_margin = True
            elif sys_argv_i_lower_strip[:15] == "left_margin_cm:":
                cm = float(sys_argv_i_lower_strip[15:].strip())
                inches = cm/2.54
                left_margin_x_pixel = round(inches*300) + 1
                user_provided_left_margin = True
            elif sys_argv_i_lower_strip[:13] == "right_margin:":
                inches = float(sys_argv_i_lower_strip[13:].strip())
                if A4:
                    #An extra pixel is subtracted in order to
                    #allow for a full "inches" margin and to
                    #start drawing one pixel before that.
                    right_margin_x_pixel = 3508-round(inches*300)-1
                else:
                    right_margin_x_pixel = 3300-round(inches*300)-1
                user_provided_right_margin = True
            elif sys_argv_i_lower_strip[:16] == "right_margin_cm:":
                cm = float(sys_argv_i_lower_strip[16:].strip())
                inches = cm/2.54
                if A4:
                    right_margin_x_pixel = 3508-round(inches*300)-1
                else:
                    right_margin_x_pixel = 3300-round(inches*300)-1
                user_provided_right_margin = True
            elif sys_argv_i_lower_strip[:11] == "top_margin:":
                inches = float(sys_argv_i_lower_strip[11:].strip())
                top_margin_y_pixel = round(inches*300)
            elif sys_argv_i_lower_strip[:14] == "top_margin_cm:":
                cm = float(sys_argv_i_lower_strip[14:].strip())
                inches = cm/2.54
                top_margin_y_pixel = round(inches*300)
            elif sys_argv_i_lower_strip[:14] == "bottom_margin:":
                inches = float(sys_argv_i_lower_strip[14:].strip())
                if A4:
                    bottom_margin_y_pixel = 2480-round(inches*300)
                else:
                    bottom_margin_y_pixel = 2550-round(inches*300)
                user_provided_bottom_margin_y_pixel = True
            elif sys_argv_i_lower_strip[:17] == "bottom_margin_cm:":
                cm = float(sys_argv_i_lower_strip[17:].strip())
                inches = cm/2.54
                if A4:
                    bottom_margin_y_pixel = 2480-round(inches*300)
                else:
                    bottom_margin_y_pixel = 2550-round(inches*300)
                user_provided_bottom_margin_y_pixel = True
            elif sys_argv_i_lower_strip[:14] == "gutter_margin:":
                inches = float(sys_argv_i_lower_strip[14:].strip())
                gutter_margin_width_pixels = round(inches*300)
                user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:17] == "gutter_margin_cm:":
                cm = float(sys_argv_i_lower_strip[17:].strip())
                inches = cm/2.54
                gutter_margin_width_pixels = round(inches*300)
                user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:19] == "heading_top_margin:":
                inches = float(sys_argv_i_lower_strip[19:].strip())
                heading_top_margin_y_pixel = round(inches*300)
            elif sys_argv_i_lower_strip[:22] == "heading_top_margin_cm:":
                cm = float(sys_argv_i_lower_strip[22:].strip())
                inches = cm/2.54
                heading_top_margin_y_pixel = round(inches*300)
            elif sys_argv_i_lower_strip[:27] == "page_numbers_bottom_margin:":
                inches = float(sys_argv_i_lower_strip[27:].strip())
                if A4:
                    page_numbers_bottom_margin_y_pixel = 2480-round(inches*300)
                else:
                    page_numbers_bottom_margin_y_pixel = 2550-round(inches*300)
            elif sys_argv_i_lower_strip[:30] == "page_numbers_bottom_margin_cm:":
                cm = float(sys_argv_i_lower_strip[30:].strip())
                inches = cm/2.54
                if A4:
                    page_numbers_bottom_margin_y_pixel = 2480-round(inches*300)
                else:
                    page_numbers_bottom_margin_y_pixel = 2550-round(inches*300)
            elif sys_argv_i_lower_strip[:18] == "heading_text_left:":
                #Here the left strip method ("lstrip()") is used to remove
                #any leading spaces before the character after the colon,
                #so that the argument text lines up with that of 
                #"sys_argv_i_lower_strip" when slicing the string.
                #We want to allow for leading or trailing spaces 
                #in the text of "heading_text_left" in case the 
                #user wants to line up the heading differently
                #through the inclusion of spaces.  
                heading_text_left = sys.argv[i].lstrip()[18:]
            elif sys_argv_i_lower_strip[:19] == "heading_text_right:":
                heading_text_right = sys.argv[i].lstrip()[19:]
            elif sys_argv_i_lower_strip[:13] == "heading_text:":
                heading_text_left = sys.argv[i].lstrip()[13:]
                heading_text_right = heading_text_left
            elif sys_argv_i_lower_strip[:19] == "heading_text_color:":
                heading_text_color =  sys_argv_i_lower_strip[19:].strip()
                if heading_text_color[0] == "(":
                    heading_text_color = "rgb" + heading_text_color
            elif sys_argv_i_lower_strip[:14] == "heading_corner":
                heading_corner = True
            elif sys_argv_i_lower_strip[:22] == "toc_heading_font_size:":
                TOC_heading_font_size = int(sys_argv_i_lower_strip[22:].strip())
            elif sys_argv_i_lower_strip[:17] == "toc_heading_text:":
                TOC_heading_text = sys.argv[i].lstrip()[17:]
            elif sys_argv_i_lower_strip[:23] == "toc_heading_text_color:":
                TOC_heading_text_color =  sys_argv_i_lower_strip[23:].strip()
                if TOC_heading_text_color[0] == "(":
                    TOC_heading_text_color = "rgb" + TOC_heading_text_color
            elif sys_argv_i_lower_strip[:18] == "heading_font_size:":
                heading_font_size = int(sys_argv_i_lower_strip[18:].strip())
            elif sys_argv_i_lower_strip[:18] == "heading_left_pages":
                heading_left_pages = True
            elif sys_argv_i_lower_strip[:19] == "heading_right_pages":
                heading_right_pages = True
            elif sys_argv_i_lower_strip[:24] == "page_numbers_text_color:":
                page_numbers_text_color =  sys_argv_i_lower_strip[24:].strip()
                if page_numbers_text_color[0] == "(":
                    page_numbers_text_color = "rgb" + page_numbers_text_color
            elif sys_argv_i_lower_strip[:23] == "page_numbers_font_size:":
                page_numbers_font_size = int(sys_argv_i_lower_strip[23:].strip())
            elif sys_argv_i_lower_strip[:17] == "page_numbers_left":
                page_numbers_left = True
            elif sys_argv_i_lower_strip[:18] == "page_numbers_right":
                page_numbers_right = True
            elif sys_argv_i_lower_strip[:12] == "page_numbers":
                page_numbers = True
            elif sys_argv_i_lower_strip[:18] == "college_ruled_left":
                college_ruled_left = True
            elif sys_argv_i_lower_strip[:19] == "college_ruled_right":
                college_ruled_right = True
            elif sys_argv_i_lower_strip[:13] == "college_ruled":
                college_ruled = True
            elif sys_argv_i_lower_strip[:15] == "wide_ruled_left":
                wide_ruled_left = True
            elif sys_argv_i_lower_strip[:16] == "wide_ruled_right":
                wide_ruled_right = True
            elif sys_argv_i_lower_strip[:10] == "wide_ruled":
                wide_ruled = True
            elif sys_argv_i_lower_strip[:18] == "custom_ruled_left:":
                custom_line_distance_inches = float(sys_argv_i_lower_strip[18:].strip())
                custom_ruled_left = True
            elif sys_argv_i_lower_strip[:19] == "custom_ruled_right:":
                custom_line_distance_inches = float(sys_argv_i_lower_strip[19:].strip())
                custom_ruled_right = True
            elif sys_argv_i_lower_strip[:13] == "custom_ruled:":
                custom_line_distance_inches = float(sys_argv_i_lower_strip[13:].strip())
                custom_ruled = True 
            elif sys_argv_i_lower_strip[:21] == "custom_ruled_left_mm:":
                mm = float(sys_argv_i_lower_strip[21:].strip())
                custom_line_distance_inches = mm/25.4
                custom_ruled_left = True
            elif sys_argv_i_lower_strip[:22] == "custom_ruled_right_mm:":
                mm = float(sys_argv_i_lower_strip[22:].strip())
                custom_line_distance_inches = mm/25.4
                custom_ruled_right = True
            elif sys_argv_i_lower_strip[:16] == "custom_ruled_mm:":
                mm = float(sys_argv_i_lower_strip[16:].strip())
                custom_line_distance_inches = mm/25.4
                custom_ruled = True
            elif sys_argv_i_lower_strip[:17] == "graph_paper_left:":
                graph_paper_left = True
                arguments = sys_argv_i_lower_strip[17:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            squares_per_inch = int(arguments[j])
                        elif j == 1:
                            bold_line_every_n_squares = int(arguments[j])
                        elif j == 2:
                            line_boldness_factor = float(arguments[j])
            elif sys_argv_i_lower_strip[:18] == "graph_paper_right:":
                graph_paper_right = True
                arguments = sys_argv_i_lower_strip[18:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            squares_per_inch = int(arguments[j])
                        elif j == 1:
                            bold_line_every_n_squares = int(arguments[j])
                        elif j == 2:
                            line_boldness_factor = float(arguments[j])
            elif sys_argv_i_lower_strip[:12] == "graph_paper:":
                graph_paper = True
                arguments = sys_argv_i_lower_strip[12:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            squares_per_inch = int(arguments[j])
                        elif j == 1:
                            bold_line_every_n_squares = int(arguments[j])
                        elif j == 2:
                            line_boldness_factor = float(arguments[j])
            #Here it is important to include the "mm" versions of 
            #"dot_grid", as otherwise the result without the colon would
            #also match (ex: 'sys_argv_i_lower_strip[:8] == "dot_grid"')
            #is true for both "dot_grid" and "dot_grid_mm".
            elif (sys_argv_i_lower_strip[:17] == "dot_grid_left_mm:" or
            sys_argv_i_lower_strip[:16] == "dot_grid_left_mm"):
                dot_grid_left = True
                if length_sys_argv_i_lower_strip > 16:
                    arguments = sys_argv_i_lower_strip[17:].replace(" ", "").split(":")
                    if arguments != [""]:
                        for j in range(len(arguments)):
                            if j == 0:
                                mm = float(arguments[j])
                                inches_between_dots = mm/25.4
                            elif j == 1:
                                dot_diameter_pixels = int(arguments[j])
                            elif j == 2:
                                dot_line_width = int(arguments[j])
                #If the user didn't specify a value for
                #the number of millimiters in-between dots,
                #it is assumed that they want 5 mm dot spacing.
                else:
                    inches_between_dots = 5/25.4
            elif (sys_argv_i_lower_strip[:18] == "dot_grid_right_mm:" or
            sys_argv_i_lower_strip[:17] == "dot_grid_right_mm"):
                dot_grid_right = True
                if length_sys_argv_i_lower_strip > 17:
                    arguments = sys_argv_i_lower_strip[18:].replace(" ", "").split(":")
                    if arguments != [""]:
                        for j in range(len(arguments)):
                            if j == 0:
                                mm = float(arguments[j])
                                inches_between_dots = mm/25.4
                            elif j == 1:
                                dot_diameter_pixels = int(arguments[j])
                            elif j == 2:
                                dot_line_width = int(arguments[j])
                else:
                    inches_between_dots = 5/25.4
            elif (sys_argv_i_lower_strip[:12] == "dot_grid_mm:" or
            sys_argv_i_lower_strip[:11] == "dot_grid_mm"):
                dot_grid = True
                if length_sys_argv_i_lower_strip > 11:
                    arguments = sys_argv_i_lower_strip[12:].replace(" ", "").split(":")
                    if arguments != [""]:
                        for j in range(len(arguments)):
                            if j == 0:
                                mm = float(arguments[j])
                                inches_between_dots = mm/25.4
                            elif j == 1:
                                dot_diameter_pixels = int(arguments[j])
                            elif j == 2:
                                dot_line_width = int(arguments[j])
                else:
                    inches_between_dots = 5/25.4 
            elif (sys_argv_i_lower_strip[:14] == "dot_grid_left:" or
            sys_argv_i_lower_strip[:13] == "dot_grid_left"):
                dot_grid_left = True
                if length_sys_argv_i_lower_strip > 13:
                    arguments = sys_argv_i_lower_strip[14:].replace(" ", "").split(":")
                    if arguments != [""]:
                        for j in range(len(arguments)):
                            if j == 0:
                                inches_between_dots = float(arguments[j])
                            elif j == 1:
                                dot_diameter_pixels = int(arguments[j])
                            elif j == 2:
                                dot_line_width = int(arguments[j])
            elif (sys_argv_i_lower_strip[:15] == "dot_grid_right:" or
            sys_argv_i_lower_strip[:14] == "dot_grid_right"):
                dot_grid_right = True
                if length_sys_argv_i_lower_strip > 14:
                    arguments = sys_argv_i_lower_strip[15:].replace(" ", "").split(":")
                    if arguments != [""]:
                        for j in range(len(arguments)):
                            if j == 0:
                                inches_between_dots = float(arguments[j])
                            elif j == 1:
                                dot_diameter_pixels = int(arguments[j])
                            elif j == 2:
                                dot_line_width = int(arguments[j])
            elif (sys_argv_i_lower_strip[:9] == "dot_grid:" or
            sys_argv_i_lower_strip[:8] == "dot_grid"):
                dot_grid = True
                if length_sys_argv_i_lower_strip > 8:
                    arguments = sys_argv_i_lower_strip[9:].replace(" ", "").split(":")
                    if arguments != [""]:
                        for j in range(len(arguments)):
                            if j == 0:
                                inches_between_dots = float(arguments[j])
                            elif j == 1:
                                dot_diameter_pixels = int(arguments[j])
                            elif j == 2:
                                dot_line_width = int(arguments[j])
            elif sys_argv_i_lower_strip[:24] == "scriptreader_acetate_mm:":
                perforated_cover = True
                scriptreader_right = True
                scriptreader_acetate = True
                #The counter "current_acetate_page_number" will keep track
                #of the acetate sheet number (two pages per acetate sheet),
                #in order to only draw a vertical line on one side of the acetate
                #sheet (as an indicator of where to cut the acetate in half).
                #Otherwise, if the lines were drawn on both sides of the
                #acetate, it would end up looking messy, as they would likely
                #not line up.
                current_acetate_page_number = 0
                #If the user has selected to print some custom
                #dot grid pages for use in the handwriting OCR
                #application ScriptReader, they will likely want
                #to perforate the pages for binding, and so a wider
                #gutter margins of 0.75 inch is included by default,
                #which may be overriden if the user has specified
                #a different gutter margin as the fifth argument.
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[24:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            mm = float(arguments[j])
                            inches_between_dots = mm/25.4
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:21] == "scriptreader_acetate:":
                perforated_cover = True
                scriptreader_right = True
                scriptreader_acetate = True
                current_acetate_page_number = 0
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[21:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:21] == "scriptreader_left_mm:":
                perforated_cover = True
                scriptreader_left = True
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[21:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            mm = float(arguments[j])
                            inches_between_dots = mm/25.4
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:22] == "scriptreader_right_mm:":
                perforated_cover = True
                scriptreader_right = True
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[22:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            mm = float(arguments[j])
                            inches_between_dots = mm/25.4
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:16] == "scriptreader_mm:":
                perforated_cover = True
                scriptreader = True
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[16:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            mm = float(arguments[j])
                            inches_between_dots = mm/25.4
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:18] == "scriptreader_left:":
                perforated_cover = True
                scriptreader_left = True
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[18:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:19] == "scriptreader_right:":
                perforated_cover = True
                scriptreader_right = True
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[19:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:13] == "scriptreader:":
                perforated_cover = True
                scriptreader = True
                gutter_margin_width_pixels = 0.75*300
                arguments = sys_argv_i_lower_strip[13:].replace(" ", "").split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
                        elif j == 3:
                            lines_between_text = int(arguments[j])
                        elif j == 4:
                            gutter_margin_width_pixels = round(float(arguments[j])*300)
                            user_provided_gutter_margin = True
            elif sys_argv_i_lower_strip[:19] == "lines_between_text:":
                lines_between_text = int(sys_argv_i_lower_strip[19:].strip())
            elif sys_argv_i_lower_strip[:25] == "custom_template_left_page":
                custom_template_left_page = True
            elif sys_argv_i_lower_strip[:26] == "custom_template_right_page":
                custom_template_right_page = True
            elif sys_argv_i_lower_strip[:26] == "custom_template_both_pages":
                custom_template_left_page = True
                custom_template_right_page = True
            elif sys_argv_i_lower_strip[:15] == "dot_fill_color:":
                dot_fill_color = sys_argv_i_lower_strip[15:].strip()
                if dot_fill_color[0] == "(":
                    dot_fill_color = "rgb" + dot_fill_color
            elif sys_argv_i_lower_strip[:18] == "dot_outline_color:":
                dot_outline_color = sys_argv_i_lower_strip[18:].strip()
                if dot_outline_color[0] == "(":
                    dot_outline_color = "rgb" + dot_outline_color
            elif sys_argv_i_lower_strip[:17] == "graph_line_color:":
                graph_line_color = sys_argv_i_lower_strip[17:].strip()
                if graph_line_color[0] == "(":
                    graph_line_color = "rgb" + graph_line_color
            elif sys_argv_i_lower_strip[:17] == "graph_line_width:":
                graph_line_width = int(sys_argv_i_lower_strip[17:].strip())
            elif sys_argv_i_lower_strip[:15] == "toc_line_color:":
                TOC_line_color = sys_argv_i_lower_strip[15:].strip()
                if TOC_line_color[0] == "(":
                    TOC_line_color = "rgb" + TOC_line_color
            elif sys_argv_i_lower_strip[:11] == "line_color:":
                line_color = sys_argv_i_lower_strip[11:].strip()
                if line_color[0] == "(":
                    line_color = "rgb" + line_color
            elif sys_argv_i_lower_strip[:15] == "toc_line_width:":
                TOC_line_width = int(sys_argv_i_lower_strip[15:].strip())
            elif sys_argv_i_lower_strip[:11] == "line_width:":
                line_width = int(sys_argv_i_lower_strip[11:].strip())
            elif sys_argv_i_lower_strip[:18] == "toc_pages_spacing:":
                arguments = sys_argv_i_lower_strip[18:].replace(" ", "").split(":")
                if len(arguments) > 0:
                    for j in range(len(arguments)):
                        if j == 0:
                            TOC_pages = int(arguments[j])
                            if TOC_pages == 0:
                                TOC_pages_list = []
                                break
                            #The number of TOC pages needs to be
                            #even in order for the first numbered
                            #page to land on a right-hand page.
                            #Therefore, if "TOC_pages" is odd_numbered,
                            #it will be incremented by one page count.
                            elif TOC_pages%2 != 0:
                                TOC_pages+=1
                            TOC_pages_list = list(range(1, TOC_pages+1))
                        elif j == 1:
                            TOC_line_spacing = float(arguments[j])
            elif sys_argv_i_lower_strip[:10] == "no_merging":
                no_merging = True
            elif sys_argv_i_lower_strip[:22] == "toc_subject_font_size:":
                TOC_subject_font_size = int(sys_argv_i_lower_strip[22:].strip())
            elif sys_argv_i_lower_strip[:23] == "toc_subject_text_color:":
                TOC_subject_text_color = sys_argv_i_lower_strip[23:].strip()
                if TOC_subject_text_color[0] == "(":
                    TOC_subject_text_color = "rgb" + TOC_subject_text_color
            elif sys_argv_i_lower_strip[:17] == "toc_subject_text:":
                TOC_subject_text = sys.argv[i].lstrip()[17:]
            elif sys_argv_i_lower_strip[:20] == "toc_pages_font_size:":
                TOC_pages_font_size = int(sys_argv_i_lower_strip[20:].strip())
            elif sys_argv_i_lower_strip[:21] == "toc_pages_text_color:":
                TOC_pages_text_color = sys_argv_i_lower_strip[21:].strip()
                if TOC_pages_text_color[0] == "(":
                    TOC_pages_text_color = "rgb" + TOC_pages_text_color
            elif sys_argv_i_lower_strip[:15] == "toc_pages_text:":
                TOC_pages_text = sys.argv[i].lstrip()[15:]
            elif sys_argv_i_lower_strip[:2] == "a4":
                A4 = True

    except Exception as e:
        print(e)
        problem = True
        print("\nPlease enter the name of the parameter you wish to alter, followed " +
        "by a colon, and the desired setting directly after the colon. For example, " +
        'to set the font size of the heading text to 100 pixels, you would enter: "heading_font_size:100.\n')

#The user can select their own background image as well and the text box fill color on the cover page will
#be determined from the complementary color to one of the darkest pixels in the image. The text color on
#the cover page will be taken from the lightest pixel on the canvas. Moreover, the user can choose to add
#a design to one or both pages by adding the JPEG image to the working folder, of which the file name starts
#with "page", so that the code might distinguish it from the cover image (of which the file name begins with
#"cover").
path_jpeg = os.path.join(cwd, "*.jpg")
jpeg_files = glob.glob(path_jpeg)
jpeg_problem_string = ('\nPlease include a JPEG file containing the image that you ' +
    'wish to use as a background for the book cover in the working folder. Also, please ' +
    'make sure that the provided background image is in JPEG format, ' +
    "with a resolution of 300 ppi and a canvas size of US Legal dimensions in " +
    'landscape mode (width of 4200 pixels and height of 2550 pixels) and that the ' +
    'file name starts with "cover". Alternatively, for a perforated cover used in ' +
    'binders, you would need to provide a background image with a resolution of 300 ppi and ' +
    'a canvas size of either US Letter (width of 3300 pixels and height of 2550 pixels) or A4 ' + 
    'dimensions (width of 3508 pixels and height of 2480 pixels) in landscape mode, ' +
    'with a file name starting with "perforated cover".\n\n' +
    "Moreover, if you wish to add an image template to your notebook, the image " +
    "needs to have a resolution of 300 ppi and a canvas size of either US Letter or A4 dimensions in " +
    "landscape mode, with margins according to the specifications (default left and margins 1/4 inch, " + 
    'top margin 1 inch and bottom margin 3/4 inch). Also, make sure to add the prefix "left page" or ' +
    '"right page" to the jpeg file name.')
if jpeg_files == []:
    print(jpeg_problem_string)
    problem = True
else:
    cover_background_img = None
    page_background_img = None
    for i in range(len(jpeg_files)):
        if os.path.split(jpeg_files[i])[-1][:16].lower() in ["perforated cover", "perforated_cover"]:
            cover_background_img = jpeg_files[i]
            perforated_cover = True
            #As the notebook pages are perforated,
            #the gutter margins will be extended to
            #0.75 inch, unless the user has provided
            #their own value for "gutter_margin".
            if user_provided_gutter_margin == False:
                gutter_margin_width_pixels = 0.75*300
        elif os.path.split(jpeg_files[i])[-1][:5].lower() == "cover":
            cover_background_img = jpeg_files[i]
        elif os.path.split(jpeg_files[i])[-1][:9].lower() in ["left page", "left_page"]:
            left_page_background_img = jpeg_files[i]
        elif os.path.split(jpeg_files[i])[-1][:10].lower() in ["right page", "right_page"]:
            right_page_background_img = jpeg_files[i]
    if (cover_background_img == None or (len(jpeg_files) > 1 and
    left_page_background_img == None and right_page_background_img == None)):
        print(jpeg_problem_string)
        problem = True

#The cover True Type Font file (".ttf") is automatically retrieved
#within the "Cover font TTF file" folder.
path_ttf = os.path.join(cwd, "Cover font TTF file", "*.ttf")
ttf_files = glob.glob(path_ttf)
if ttf_files == []:
    print("\nPlease include a True Type Font (.ttf) file containing " +
    'the font you wish to use on the cover page in the folder "Cover font TTF file"')
    problem = True
elif len(ttf_files) > 1:
    print("\nPlease include only one True Type Font (.ttf) file containing " +
    'the font you wish to use on the cover page in the folder "Cover font TTF file".')
    problem = True
else:
    cover_font = ttf_files[0]

#The header and footer True Type Font file (".ttf") is automatically retrieved
#within the "Header and footer font TTF file" folder.
path_ttf = os.path.join(cwd, "Header and footer font TTF file", "*.ttf")
ttf_files = glob.glob(path_ttf)
if ttf_files == []:
    print("\nPlease include a True Type Font (.ttf) file containing " +
    'the font you wish to use on the cover page in the folder "Header and footer font TTF file"')
    problem = True
elif len(ttf_files) > 1:
    print("\nPlease include only one True Type Font (.ttf) file containing " +
    'the font you wish to use on the cover page in the folder "Header and footer font TTF file".')
    problem = True
else:
    heading_font = ImageFont.truetype(ttf_files[0], heading_font_size)
    page_numbers_font = ImageFont.truetype(ttf_files[0], page_numbers_font_size)
    TOC_heading_font = ImageFont.truetype(ttf_files[0], TOC_heading_font_size)
    TOC_pages_font = ImageFont.truetype(ttf_files[0], TOC_pages_font_size)
    TOC_subject_font = ImageFont.truetype(ttf_files[0], TOC_subject_font_size)

if (problem == False and title != None and number_of_pages
not in [0, None] and (inches_per_ream_500_pages not in [0, None]
or perforated_cover == True)):

    if A4:
        #The width of an A4 page corresponds to: round(210 mm/25.4 mm/inch * 300 pixels/inch) = 2480 px
        paper_width = 2480
        #The length of the book cover using A4 paper corresponds to:
        #round(297 mm/25.4 mm/inch * 300 pixels/inch) = 3508 px
        paper_height = 3508
    else:
        #The width of a US Letter page corresponds to 8.5 inch * 300 pixels/inch = 2550 px
        paper_width = 2550
        #The length of the book cover using US Letter paper corresponds to:
        #11 inch * 300 pixels/inch = 3300 px
        paper_height = 3300
 
    #In order for the booklet numbering to allow for duplex printing,
    #the sum of the TOC pages and the notebook pages needs to be
    #dividable by four (as one sheet of paper contains two pages on
    #each side). If this is not the case, the "number_of_pages" will
    #be incremented by one page until this criterion is met.
    #This is only done if "scriptreader_acetate == False", as the
    #page numbering proceeds differently in this case.
    if (number_of_pages + TOC_pages)%4 != 0 and scriptreader_acetate == False:
        while (number_of_pages + TOC_pages)%4 != 0:
            number_of_pages += 1

    elif scriptreader_acetate == True:
        if heading_text_right == None:
            heading_text_right = "Write on this side"
        if page_numbers_text_color == "LightSteelBlue":
            page_numbers_text_color = "LightSlateGrey"
        if dot_fill_color == "LightSlateGrey":
            dot_fill_color = "DimGrey"
        if dot_outline_color == "LightSlateGrey":
            dot_outline_color = "DimGrey"

        #As the pages will only be printed on the left-hand pages, the
        #total number of TOC pages "TOC_pages" and notebook pages "number_of_pages"
        #both need to be multiplied by two to reflect what the user actually wants.
        #The code will actually generate the pages on the right-hand pages, but
        #flip each image so that they are printed on the left-hand pages. This way,
        #the user can write with erasable ink on the side that was not printed, with
        #the text displayed in the right order.
        TOC_pages = 2* TOC_pages
        TOC_pages_list = list(range(1,TOC_pages+1))
        number_of_pages = 2*number_of_pages

    #The "total_number_of_pages" will be useful in determining
    #the thickness of the spine later on in the code.
    total_number_of_pages = number_of_pages + TOC_pages

    #If only the "TOC_line_width" was specified by the user,
    #the code will apply that value to "line_width" as well,
    #so that any other ruled lines may line up with the TOC.
    if TOC_line_width != 5 and line_width == 5:
        line_width = TOC_line_width
    #Similarly, if the user has only specified a "line_width"
    #different than the default value of 5 pixels, then the
    #"TOC_line_width" will be set to the same value for the
    #same reason.
    elif line_width != 5 and TOC_line_width == 5:
        TOC_line_width = line_width
    #The line spacing for the table of contents is harmonized with
    #other line spacings, if ruled lines or dot grids were selected
    #within the notebook, with preference being biven to ruled lines.
    #This will enable users to use the "high five" notebook organizing
    #system (see https://www.highfivehq.com/ for more information).
    if (TOC_line_spacing == None and (college_ruled == True or
    college_ruled_left == True or college_ruled_right == True)):
        TOC_line_spacing = 9/32
    elif (TOC_line_spacing == None and (wide_ruled == True or
    wide_ruled_left == True or wide_ruled_right == True)):
        TOC_line_spacing = 11/32
    elif (TOC_line_spacing == None and (custom_ruled == True or
    custom_ruled_left == True or custom_ruled_right == True)):
        TOC_line_spacing = custom_line_distance_inches
    elif TOC_line_spacing == None and (dot_grid == True or
    dot_grid_left == True or dot_grid_right == True):
        TOC_line_spacing = inches_between_dots
    elif TOC_line_spacing == None:
        if A4 == True:
            TOC_line_spacing = 8/25.4
        else:
            TOC_line_spacing = 9/32
    
    #The variable "page_numbers_bottom_margin_y_pixel" designates
    #the "y" coordinate mapping to the vertical middle point of the
    #page numbers. By default, this variable is set as "None", and the
    #user can either set it manually, or the code will determine whether there
    #is sufficient space to vertically center the page numbers in the space
    #in-between the last horizontal line and the bottom of the page. Should
    #there be less than 75 pixels below the page number for it to be
    #vertically centered, the code will automatically bring the text up,
    #such that the lowest "y" pixel of the page number is above 75 pixels
    #from the bottom of the page, thereby respecting the default 0.25 inch
    #non-printable area for most printers.

    #If the user didn't provide manually the vertical distance from the
    #bottom of the page at which the page numbers will be written, then
    #"page_numbers_bottom_margin_y_pixel" will still be "None". This
    #variable is then set such as the bottom "y" coordinate of the text
    #will be 75 pixels (or 0.25 inches) from the bottom of the page.
    #The variable "page_numbers_bottom_margin_y_pixel" will be reevaluated
    #later on in the code to automatically center the page numbers vertically,
    #if applicable.
    
    #The page numbers are written with left or right middle text anchoring 
    #("lm" or "rm", respectively), in order to simplify the automatic vertical
    #centering of the page numbers in the available space in-between the last horizontal
    #line and the bottom of the page.
    
    #When determining the value of the "y" coordinate of the middle point of the page numbers
    #("page_numbers_bottom_margin_y_pixel"), we must take into account the middle text anchoring 
    #by subtracting half the "page_number_font_size". The variable "default_page_numbers_bottom_margin_y_pixel",
    #initialized to "False", will only be turned to "True" if the user didn't specify any value
    #for "page_numbers_bottom_margin:" or "page_numbers_bottom_margin_cm:". The page numbers will
    #automatically be centered vertically along the empty space at the bottom of the notebook
    #pages if the users didn't provide values for these variables 
    #(if "default_page_numbers_bottom_margin_y_pixel == True").
    default_page_numbers_bottom_margin_y_pixel = False
    if page_numbers_bottom_margin_y_pixel == None:
        page_numbers_bottom_margin_y_pixel = paper_width - (75 + page_numbers_font_size/2)
        default_page_numbers_bottom_margin_y_pixel = True
    
    if A4:
        #The "bottom_margin_y_pixel" maps to
        #the "y" pixel where the lines and dots end.
        #If the user didn't specify a value for this
        #variable, it needs to be adjusted to the width of an
        #A4 page (2480 px - 0.60 inch*300 px/inch = 2300 px).
        if user_provided_bottom_margin_y_pixel == False:
            bottom_margin_y_pixel = 2300
        if user_provided_right_margin == False:
            #The variable "right_margin_x_pixel" maps to 
            #the "x" pixel where the lines and dots start 
            #being drawn on the right-hand pages. If the user didn't 
            #specify a value for this variable, it needs 
            #to be adjusted to the length of an A4 page 
            #(3508 px - 0.25 inch*300 px/inch - 1 px = 3432 px)
            #One extra pixel is subtracted to allow a full 75 px
            #margin and to start drawing 1 pixel before that.
            right_margin_x_pixel = 3432
    
    #Here, 105 pixels are added so that the bottom margin
    #for the TOC pages is 0.25 inch instead of 0.6 inch
    #(0.6*300 - 0.25*300 = 105 px), as there is no need
    #to accomodate the page numbers on TOC pages.
    bottom_margin_y_pixel_TOC = bottom_margin_y_pixel + 105
    

    font_title = ImageFont.truetype(cover_font, cover_title_font_size)
    #As the author name font size should be at most 75% of that of the title
    #(or whatever the value of "max_author_title_font_ratio" is), the initial 
    #font size is set to 75% of "cover_title_font_size".
    cover_author_font_size = round(max_author_title_font_ratio*cover_title_font_size)
    font_author = ImageFont.truetype(cover_font, cover_author_font_size)
    image = Image.open(cover_background_img)

    if perforated_cover == False:
        
        if A4:
            #The left margin can be determined by subtracting the space
            #in-between the margins (297/25.4/2-0.75 = 5.10 inches) from the right edge
            #pixel count: (4200 - (297/25.4/2-0.75)*300) = 2671 px, with 300 being the
            #resolution (300 pixels per inch).

            #The right margin remains the same with the A4 format, as it can 
            #simply be calculated given the pixel width of the canvas: 
            #4220-(0.75*300) = 3995 px, with 300 being the resolution (300 pixels per inch).

            #Also, as there is roughly 1/4 inch difference in width between 
            #the US letter page (8.5 inches) and the A4 page (8.27 inches),
            #there will simply be a larger white trim at the bottom of the 
            #legal page, and the "top_margin_cover_textbox" will stay the 
            #same at a default of 640 px
            left_margin_cover_textbox = 2671
        
        #Some extra pixels are subtracted from "left_margin_cover_textbox",
        #(35 pixels by default), as there seems to be 3 mm missing on both
        #sides of the cover due to binding irregularities and the thickness of
        #the glue: (3 mm * inch/25.4 mm * 4200 pixels/14 inch = 35 pixels).
        #By subtracting some pixels, the cover title box is shifted towards
        #the left.
        left_margin_cover_textbox -= cover_extra_pixels

        #The same applies to the "right_margin_cover_textbox"
        right_margin_cover_textbox -= cover_extra_pixels

        #The space between the left edge of the textbox
        #and the start of the text on the x axis is set to 100 pixels,
        #so the text will start drawing at "left_margin_cover_textbox + 100" pixels
        left_margin_cover_text = left_margin_cover_textbox + 100

        #The space between the right edge of the textbox
        #and the end of the text on the x axis is set to 100 pixels,
        #so the text will start drawing at "right_margin_cover_textbox - 100" pixels
        right_margin_cover_text = right_margin_cover_textbox - 100

        #The space between the top margin of the textbox
        #and where the top edge of the text on the y axis
        #is set to 50 pixels: "top_margin_cover_textbox+100"
        vertical_margin_cover_text = top_margin_cover_textbox + 100


    elif perforated_cover == True:

        if A4:
            #The left margin can be determined by subtracting the space
            #in-between the margins (297/25.4/2-0.75 = 5.10 inches) from the right edge
            #pixel count: (3508 - (297/25.4/2-0.75)*300) = 1979 px, with 300 being the
            #resolution (300 pixels per inch).
            left_margin_cover_textbox = 1979

            #The right margin in A4 format can 
            #simply be calculated given the pixel width of the canvas: 
            #3508-(0.75*300) = 3283 px, with 300 being the resolution (300 pixels per inch).
            right_margin_cover_textbox = 3283
        else:
            #Similarly, for the perforated cover in letter format,
            #the left margin would be calculated from the width of
            #the page in landscape format at 300 ppi resolution,
            #(3300 - 4.75*3300/11 = 1875 px)
            left_margin_cover_textbox = 1875

            #A similar calculation takes place for the perforated
            #cover in letter format for the right margin 
            #(3300-0.75*3300/11 = 3075 px)
            right_margin_cover_textbox = 3075

        #The space between the left edge of the textbox
        #and the start of the text on the x axis is set to 100 pixels,
        #so the text will start drawing at "left_margin_cover_textbox + 100" pixels
        left_margin_cover_text = left_margin_cover_textbox + 100

        #The space between the right edge of the textbox
        #and the end of the text on the x axis is set to 100 pixels,
        #so the text will start drawing at "right_margin_cover_textbox - 100" pixels
        right_margin_cover_text = right_margin_cover_textbox - 100

        #The space between the top margin of the textbox
        #and where the top edge of the text on the y axis
        #is set to 50 pixels: "top_margin_cover_textbox+100"
        vertical_margin_cover_text = top_margin_cover_textbox + 100
    
    #If the user hasn't provided a color for the cover text box
    #nor for the cover text, the colors will be assigned automatically
    #based on the darkest and lightest pixels on the canvas. In order to
    #facilitate this process, the image the image is first converted to
    #grayscale in order to be able to extract the darkest and lightest
    #pixels from the background.

    #If the user hasn't povided a color for the cover text box
    #nor for the cover text, then the code needs to check if
    #the submitted image is grayscale or not, in the case that
    #the "grayscale" argument wasn't passed in when running the code.
    #If the submitted image turns out to already be in grayscale format,
    #then the default color for the cover boxes is set to "Black" and
    #the color of the cover text is set to "LightGrey", as these give more
    #esthetically pleasing results in terms of contrast with the
    #background.
    #The first pixel "x,y" coordinate at index "[0][0]" in the numpy
    #array "image_array" (before the image is converted to "RGB" mode)
    #will be checked to see if it is of type "np.ndarray", indicating that
    #it has RGB channels, instead of being an integer as in a
    #grayscale image. If the "isinstance()" method is "False",
    #then it means that the image is grayscale.
    if cover_box_color == None and cover_text_color == None:
        image_array = np.array(image)
        if isinstance(image_array[0][0], np.ndarray) == False or grayscale == True:
            cover_box_color = "Black"
            #The recycling symbol on the back cover
            #will be filled in black when the "grayscale"
            #option is selected
            recycling_symbol_color = (0,0,0,255)
            cover_text_color = "LightGrey"
            #The outline of the recycling symbol on the back
            #cover will be set to the RGB equivalent of 
            #"LightGrey" if the "grayscale" option is selected.
            recycling_symbol_outline_color = (211,211,211,255)
            #If the provided image was in grayscale format to start with,
            #or if the user has passed in the "grayscale" argument when
            #running the code, then the "image" instance is overwritten with
            #its grayscale version and the "grayscale" variable is set to "True",
            #in order to avoid creating another grayscale image in the "elif"
            #statement below: "cover_box_color == None and cover_text_color ==
            #None and grayscale == False".
            image = ImageOps.grayscale(image)
            grayscale = True

    #If the provided image isn't in grayscale format, then the colors for the
    #cover text box fill and text need to be determined. The value of the variable
    #"grayscale" will determine if the original image will be overwritten with its
    #grayscale version or if a new instance of the "ImageOps" class will be created,
    #in order to preserve the color information from the original "image".

    #If the "grayscale" variable is set to "True", it means that the user
    #wants to output the cover in grayscale format, and the original image
    #is overwritten with the grayscale image ("image = ImageOps.grayscale(image)").
    if cover_box_color == None and cover_text_color == None and grayscale == True:
        image_array = np.array(image)
        #The "x,y" coordinates for the lightest pixels (having the highest grayscale
        #value, as white is 255) are found using the np.where() method, where the
        #pixels's grayscale value is equal to the maximal grayscale value
        #(np.max(image_array)).
        max_pixels = np.where(image_array == np.max(image_array))
        #One of the pixel "x,y" coordinates matching the highest grayscale value will
        #be selected and stored in "max_pixel". If there were more than one pixel with
        #that grayscale value ("len(max_pixels) > 1"), then the first one is selected.
        if len(max_pixels) > 1:
            max_pixel = [max_pixels[0][0], max_pixels[1][0]]
        #If there is only one pixel with that grayscale value, then its coordinates
        #are stored in "max_pixel".
        else:
            max_pixel = [max_pixels[0], max_pixels[1]]
        #A similar approach is taken for the darkest pixels, which have the lowest
        #grayscale value (black being 0).
        min_pixels = np.where(image_array == np.min(image_array))
        if len(min_pixels) > 1:
            min_pixel = [min_pixels[0][0], min_pixels[1][0]]
        else:
            min_pixel = [min_pixels[0], min_pixels[1]]
    #If the user didn't pass in "grayscale" as an additional argument,
    #then the grayscale image is stored in "image_grayscale", to preserve
    #the color information of the original "image".
    elif cover_box_color == None and cover_text_color == None and grayscale == False:
        image_grayscale = ImageOps.grayscale(image)
        image_array_grayscale = np.array(image_grayscale)

        #The "x,y" coordinates for the lightest pixels (having the highest grayscale
        #value, as white is 255) are found using the np.where() method, where the
        #pixels's grayscale value is equal to the maximal grayscale value
        #(np.max(image_array_grayscale)).
        max_pixels = np.where(image_array_grayscale == np.max(image_array_grayscale))
        #One of the pixel "x,y" coordinates matching the highest grayscale value will
        #be selected and stored in "max_pixel". If there were more than one pixel with
        #that grayscale value ("len(max_pixels) > 1"), then the first one is selected.
        if len(max_pixels) > 1:
            max_pixel = [max_pixels[0][0], max_pixels[1][0]]
        #If there is only one pixel with that grayscale value, then its coordinates
        #are stored in "max_pixel".
        else:
            max_pixel = [max_pixels[0], max_pixels[1]]
        #A similar approach is taken for the darkest pixels, which have the lowest
        #grayscale value (black being 0).
        min_pixels = np.where(image_array_grayscale == np.min(image_array_grayscale))
        if len(min_pixels) > 1:
            min_pixel = [min_pixels[0][0], min_pixels[1][0]]
        else:
            min_pixel = [min_pixels[0], min_pixels[1]]

    #The "image" is then converted to "RGB" mode in case
    #the user has specified some colors to use in "RGB" mode.
    #The "image_array" is overwritten with the multi-channel
    #"RGB" numpy array.
    image = image.convert("RGB")
    image_array = np.array(image)
    #The "image_editable" instantiation of the "Draw" class will allow
    #to modify the background image by overlaying it with the text boxes.)
    image_editable = ImageDraw.Draw(image)

    #If no colors have been specified by the user for the boxes and text containing
    #the title and author name, then the code will automatically extract the darkest
    #color from the image, which it will apply to the filled-out boxes on the cover and spine,
    #and the lightest color on the canvas, which it will assign to the text and light rectangles.
    #It will also apply lightness corrections to these colors if needed in order for the text to
    #be readily legible.
    if cover_box_color == None and cover_text_color == None:
        #Knowing the pixel "x,y" coordinates for the pixel with the lowest
        #grayscale value ("min_pixel"), it is possible to find it within the
        #colored image, by indexing the "image_array" numpy array derived from it.
        dark_color = (image_array[min_pixel[0], min_pixel[1]]).tolist()

        #The complementary color is determined by subtracting the RGB
        #values from those of white (255,255,255). This tends to give
        #more interesting color combinations for the boxes.
        for i in range(3):
            dark_color[i] = 255 - dark_color[i]

        #In order to compare the darkness of different colors quantitatively, the colors are
        #converted into their grayscale equivalents by doing the average of the three RGB values.
        dark_color_grayscale = round(dark_color[0]/3 + dark_color[1]/3 + dark_color[2]/3)
        #The same process as above is repeated for the lightest color on the background image,
        #except that its complementary color is not determined.
        light_color = (image_array[max_pixel[0], max_pixel[1]]).tolist()

        light_color_grayscale = round(light_color[0]/3 + light_color[1]/3 + light_color[2]/3)

        #The "too_high" variable initialized as "False" and will be set to "True" if
        #a R, G or B value exceeding 255 is obtained when correcting the lightness of
        #"light_color". A normalization will then take place to bring the highest channel
        #value to 250, while keeping the relative proportion between channel values.
        too_high = False
        #If the "light_color" is either white (255,255,255) or the grayscale
        #equivalence of the RGB for "light_color" is very pale ("light_color_grayscale">250),
        #or if "light_color_grayscale" is too dark ("light_color_grayscale" < 225) and
        #the "dark_color_grayscale" is dark enough ("dark_color_grayscale < 125"), then
        #every channel of "light_color" will be set to the corresponding channel of
        #"dark_color" multiplied by two. If the highest channel of the resulting
        #"light_color" is over 255, it will be normalized so that it equals 250, and
        #the other channels will be decreased proportionally.
        if ((light_color == [255,255,255] or light_color_grayscale > 250 or
        light_color_grayscale < 225) and dark_color_grayscale < 125):
            multiplier_light = 250/light_color_grayscale
            for i in range(3):
                light_color[i] = round(light_color[i] * multiplier_light)
                if light_color[i] > 255:
                    too_high = True
            if too_high == True:
                normalization_factor = 250/max(light_color)
                for i in range(len(light_color)):
                    light_color[i] = round(light_color[i] * normalization_factor)
        #If the "light_color" is either white (255,255,255) or the grayscale
        #equivalence of the RGB for "light_color" is very pale ("light_color_grayscale">250),
        #or if "light_color_grayscale" is too dark ("light_color_grayscale" < 225) and
        #the "dark_color_grayscale" is too light ("dark_color_grayscale >= 125"), then
        #a correction factor will be applied to every channel of "dark_color", such that
        #its grayscale equivalence reaches 125. Then, every channel of "light_color" will
        #be set to the corresponding channel of the corrected "dark_color", multiplied by two.
        #If the highest channel of the resulting "light_color" is over 255, it will be
        #normalized so that it equals 250, and the other channels will be decreased proportionally.
        elif ((light_color == [255,255,255] or light_color_grayscale > 250 or
        light_color_grayscale < 225) and dark_color_grayscale >= 125):
            multiplier_dark = 125/dark_color_grayscale
            for i in range(3):
                dark_color[i] = round(dark_color[i] * multiplier_dark)
                light_color[i] = round(dark_color[i] * 2)
                if light_color[i] > 255:
                    too_high = True
            if too_high == True:
                normalization_factor = 250/max(light_color)
                for i in range(len(light_color)):
                    light_color[i] = round(light_color[i] * normalization_factor)
        #If the only issue is that the grayscale equivalence of "dark_color" is too
        #light ("dark_color_grayscale >= 125"), then a correction factor will be
        #applied to every channel of "dark_color", such that its grayscale equivalence
        #reaches 125.
        elif dark_color_grayscale >= 150:
            multiplier_dark = 125/dark_color_grayscale
            for i in range(len(dark_color)):
                dark_color[i] = round(dark_color[i] * multiplier_dark)

        #The lists "light_color" and "dark_color" are
        #converted into tuple form in order to be passed in
        #as parameters when drawing the rectangles and writing
        #the text onto the cover page.
        cover_text_color = "rgb" + str(tuple(light_color))
        cover_box_color = "rgb" + str(tuple(dark_color))
        #The recycling symbol on the back cover will be 
        #filled with the "cover_box_color", and its outline
        #will correspond to the "cover_text_color"
        recycling_symbol_color = (dark_color[0], dark_color[1], dark_color[2], 255)
        recycling_symbol_outline_color = (light_color[0], light_color[1], light_color[2])

    else:
        if cover_box_color != None and cover_box_color[0] == "(":
            cover_box_color = "rgb" + cover_box_color
        elif cover_box_color == None:
            cover_box_color = "Black"
            #The recycling symbol on the back cover
            #will be filled in black when the "Black"
            #is selected is selected as the "cover_box_color"
            recycling_symbol_color = (0,0,0,255)
        if cover_text_color != None and cover_text_color[0] == "(":
            cover_text_color = "rgb" + cover_text_color
        elif cover_text_color == None:
            cover_text_color = "White"
            if cover_box_color != None and cover_box_color[:4] == "rgb(":
                #the outline of the recycling symbol on the back
                #cover will be set to white if no color has been
                #specified for "cover_text_color" and if the 
                #the color of the text box ("cover_box_color")
                #is set to an HTML color name (it doesn't start with
                #"rgb(").
                recycling_symbol_outline_color = (255,255,255,255)
    
    #The "available_horizontal_space_pixels" that is available within the
    #black rectangle is determined as the difference between
    #"right_margin_cover_text" and "left_margin_cover_text". These margins
    #are 100 pixels farther inside from the edges of the black rectangle
    #and will prevent the text from being too close to them.
    available_horizontal_space_pixels = round((right_margin_cover_text-left_margin_cover_text))
    #If the "title_length_pixels" (written using the formatting parameters specified in
    #"font_title") is above the "available_horizontal_space_pixels", then the title text
    #will be split in the same way as for the title page, and the font size will be
    #decremented by one unit in the "while" loop below until each of the split lines
    #of the title can fit within the black rectangle, down to a minimum font size of 50.
    cover_title_height = cover_title_font_size
    #Here the same conditions as for the title page need to be met
    #("title_width_twips > width_threshold"), as we want the title to 
    #be split in the same way as for the title page.

    #If the title didn't contain sequences of at least two
    #consecutive spaces, which would indicate that the user
    #wants to manually insert line breaks at these locations,
    #and that the title width in twips is too large to fit
    #on one line, then the title string is split into
    #individual words, which are assessed for length
    #in the while loop in the "if" statement below.
    #The "title_size" is decremented until both fragments
    #of the title can fit onto their own line or a font size
    #of 27 is reached.
    length_title_pixels = image_editable.textlength(title, font_title)
    if title_with_spaces == None and length_title_pixels > available_horizontal_space_pixels:
        if " " in title:
            title_words = re.split(r"( )", title)
            number_of_title_words = len(title_words)
            #The middle index in the title will be the threshold
            #for including a carriage return in the title.
            middle_index_in_title = math.ceil(len(title_words)/2)
            first_half_words = title_words[:middle_index_in_title]
            title_first_half_words_string = "".join(first_half_words)
            second_half_words = title_words[middle_index_in_title:]
            title_second_half_words_string = "".join(second_half_words)

            adjusted_title_cover = title_first_half_words_string + "\n" + title_second_half_words_string
            longest_title_line = sorted([title_first_half_words_string, title_second_half_words_string], key=len)[-1]

        #If there weren't any spaces in the title and the width of the 
        #title wasn't within bounds of the page, then "adjusted_title_cover" 
        #is set to the #value of "title".
        else:
            adjusted_title_cover = title
    #Should the title contain sequences of at least two
    #consecutive spaces, which indicate that the user
    #wants to manually insert line breaks at these locations,
    #these instances are changed for a new line RTF command 
    #("\line "), with the space after it being required here
    #in order to prevent the word following it to be merged to 
    #the RTF command (ex: "\lineNextWord"),
    #and the length of the longest line would be determined
    #by splitting the resulting string along the "\line " dividers.
    #The font size of the title is then automatically adjusted,
    #such that the longest line may fit within the available
    #horizontal space.
    elif title_with_spaces != None:
        #The variable "custom_title_line_breaks" indicates
        #that the user has included sequences of at least
        #two successive spaces within the title, so that
        #linebreaks may be inserted at these locations.
        custom_title_line_breaks = True
        adjusted_title_cover = re.sub(r"[ ]{2,}", "\n", title_with_spaces)
        split_adjusted_title_cover = adjusted_title_cover.split("\n")
        longest_title_line = sorted(split_adjusted_title_cover, key=len)[-1]
    
    if author != None:
        #If the author didn't contain sequences of at least two
        #consecutive spaces, which would indicate that the user
        #wants to manually insert line breaks at these locations,
        #and that the author width in twips is too large to fit
        #on one line, then the author string is split into
        #individual words, which are assessed for length
        #in the while loop in the "if" statement below.
        #The "author_size" is decremented until both fragments
        #of the author can fit onto their own line or a font size
        #of 27 is reached.
        length_author_pixels = image_editable.textlength(author, font_author)
        if author_with_spaces == None and length_author_pixels > available_horizontal_space_pixels:
            if " " in author:
                author_words = re.split(r"( )", author)
                number_of_author_words = len(author_words)
                #The middle index in the author will be the threshold
                #for including a carriage return in the author.
                middle_index_in_author = math.ceil(len(author_words)/2)
                first_half_words = author_words[:middle_index_in_author]
                author_first_half_words_string = "".join(first_half_words)
                second_half_words = author_words[middle_index_in_author:]
                author_second_half_words_string = "".join(second_half_words)

                adjusted_author_cover = author_first_half_words_string + "\n" + author_second_half_words_string
                longest_author_line = sorted([author_first_half_words_string, author_second_half_words_string], key=len)[-1]

            #If there weren't any spaces in the author and the width of the 
            #author wasn't within bounds of the page, then "adjusted_author_cover" 
            #is set to the #value of "author".
            else:
                adjusted_author_cover = author
        #Should the author contain sequences of at least two
        #consecutive spaces, which indicate that the user
        #wants to manually insert line breaks at these locations,
        #these instances are changed for a new line RTF command 
        #("\line "), with the space after it being required here
        #in order to prevent the word following it to be merged to 
        #the RTF command (ex: "\lineNextWord"),
        #and the length of the longest line would be determined
        #by splitting the resulting string along the "\line " dividers.
        #The font size of the author is then automatically adjusted,
        #such that the longest line may fit within the available
        #horizontal space.
        elif author_with_spaces != None:
            #The variable "custom_author_line_breaks" indicates
            #that the user has included sequences of at least
            #two successive spaces within the author, so that
            #linebreaks may be inserted at these locations.
            custom_author_line_breaks = True
            adjusted_author_cover = re.sub(r"[ ]{2,}", "\n", author_with_spaces)
            split_adjusted_author_cover = adjusted_author_cover.split("\n")
            longest_author_line = sorted(split_adjusted_author_cover, key=len)[-1]

    
    #The function "resize_string_cover_page" automatically decrements the "cover_title_font_size"
    #and "cover_author_font_size" if the longest line in the "title" or "author" is too wide to 
    #fit in the "available_horizontal_space_pixels". It returns the updated "cover_title_font_size"
    #or "cover_author_font_size", along with "cover_title_height" or "cover_author_height" 
    #and the instance of "font_title" or "font_author".
    def resize_string_cover_page(cover_string_font_size, image_editable, longest_string_line, 
    font_string, available_horizontal_space_pixels, cover_font, adjusted_string_cover, cover_string_line_spacing):
        while cover_string_font_size > 50:
                #The length (in pixels) taken up by the longest title or author line is determined 
                #using the "textlength()" method, using the "font_title" or "font_author" with the 
                #current value of "cover_title_font_size".
                length_longest_string_line_pixels = image_editable.textlength(longest_string_line, font_string)
                if length_longest_string_line_pixels > available_horizontal_space_pixels:
                    cover_string_font_size-=1
                    font_string = ImageFont.truetype(cover_font, cover_string_font_size)
                else:
                    extra_horizontal_px_both_sides_of_cover_string = round(
                    (available_horizontal_space_pixels - length_longest_string_line_pixels)/2)
                    #If the title was split, the "cover_string_height" variable is updated to
                    #reflect that the text now spans multiple lines, including the spacing
                    #in-between the lines ("cover_string_line_spacing").
                    number_of_carriage_returns = adjusted_string_cover.count("\n")
                    #The number of lines of the "adjusted_string_cover" equals the number of 
                    #carriage returns ("\n") in the string plus one (so a title with two carriage 
                    #returns actually spans three lines) and the number of spaces in-between lines
                    #corresponds to the number of carriage returns multiplied by "cover_string_line_spacing".
                    cover_string_height = ((number_of_carriage_returns+1)*cover_string_font_size + 
                    (number_of_carriage_returns)*cover_string_line_spacing)

                    return cover_string_font_size, cover_string_height, font_string, extra_horizontal_px_both_sides_of_cover_string
    
    #If there were sequences of at least two successive spaces in the title indicating the location
    #where the user wanted to insert carriage returns or if the title width ("length_title_pixels")
    #exceeded the "available_horizontal_space_pixels", then the function "resize_string_cover_page"
    #is called and the font size of the title will be automatically decreased until its longest
    #line fits within the available horizontal space.
    if custom_title_line_breaks or length_title_pixels > available_horizontal_space_pixels:
        cover_title_font_size, cover_title_height, font_title, extra_horizontal_px_both_sides_of_cover_title = (
        resize_string_cover_page(cover_title_font_size, image_editable, longest_title_line, font_title, 
        available_horizontal_space_pixels, cover_font, adjusted_title_cover, cover_title_line_spacing))

    #If the title could fit in the available space and that
    #the user didn't include instances of two or more spaces
    #in the title string to indicate the location of 
    #carriage returns, then the length of the title in pixels
    #is determined, and the difference in-between the available
    #pixels on the horizontal axis in the cover box and the
    #title length in pixels is stored in the variable
    #"extra_horizontal_px_both_sides_of_cover_title". This needs
    #to be done here, as the function "resize_string_cover_page()",
    #which returns "extra_horizontal_px_both_sides_of_cover_title",
    #isn't called in this case.
    else:
        title_length_pixels = image_editable.textlength(title, font_title)
        extra_horizontal_px_both_sides_of_cover_title = round((
        available_horizontal_space_pixels - title_length_pixels)/2)
    
    if author != None:
        #As the author name font size should be at most 75% of that of the title
        #(or whatever the value of "max_author_title_font_ratio" is), the initial 
        #font size is set to 75% of "cover_title_font_size".
        cover_author_font_size = round(max_author_title_font_ratio*cover_title_font_size)
        font_author = ImageFont.truetype(cover_font, cover_author_font_size)
        cover_author_height = cover_author_font_size

        if custom_author_line_breaks or length_author_pixels > available_horizontal_space_pixels:
            cover_author_font_size, cover_author_height, font_author, extra_horizontal_px_both_sides_of_cover_author = (
            resize_string_cover_page(cover_author_font_size, image_editable, longest_author_line, font_author, 
            available_horizontal_space_pixels, cover_font, adjusted_author_cover, cover_author_line_spacing))
        else:
            author_length_pixels = image_editable.textlength(author, font_author)
            extra_horizontal_px_both_sides_of_cover_author = round((
            available_horizontal_space_pixels - author_length_pixels)/2)
    
        #The smallest difference between the available space on the page and the 
        #pixel length of either the longest title or author line will be used to 
        #automatically decrease the width of the dark and light rounded rectangles 
        #on the cover page. This way, the cover rectangle will snuggly fit the 
        #horizontal length of the longest line between the title and author text, 
        #when taking in consideration their respective font sizes. 
        extra_horizontal_px_both_sides_of_cover_string = min([extra_horizontal_px_both_sides_of_cover_title, 
        extra_horizontal_px_both_sides_of_cover_author])
    else:
        extra_horizontal_px_both_sides_of_cover_string = extra_horizontal_px_both_sides_of_cover_title
        cover_author_height = 0

    #If the title line was split by the code, then "title_length_pixels"
    #is set to the pixel length of the longest title line.
    if longest_title_line != None:
        title_length_pixels = image_editable.textlength(longest_title_line, font_title)
    #Otherwise, "title_length_pixels" is set to the pixel length of the full title.
    else:
        title_length_pixels = image_editable.textlength(title, font_title)
    #The "cover_author_offset" variable stores the offset length in pixels required on
    #the x axis so that the author is centered within the dark rectangle. Please note 
    #that the "textlength()" method does not allow for carriage returns ("\n") to be 
    #present in the string (there shouldn't be any, as the "title" string was stripped
    #when defining the "title" variable) The offset is calculated as the difference
    #between the middle points of the total available horizontal space and 
    #"title_length_pixels". The extra horizontal pixels on the left and right side
    #of the title are subtracted from the horizontal space in-between the right and
    #left margins in the dark rectangle ("right_margin_cover_text - left_margin_cover_text"),
    #in order to factor in that the horizontal dimention of the rectangle is automatically
    #adjusted to fit the text.
    cover_title_offset = round(
    (right_margin_cover_text - left_margin_cover_text - 
    2*extra_horizontal_px_both_sides_of_cover_string)/2 - title_length_pixels/2)
    
    if author != None:
        #The same approach is taken for the author text.
        if longest_author_line != None:
            author_length_pixels = image_editable.textlength(longest_author_line, font_author)
        else:
            author_length_pixels = image_editable.textlength(author, font_author)
        cover_author_offset = round(
        (right_margin_cover_text - left_margin_cover_text - 
        2*extra_horizontal_px_both_sides_of_cover_string)/2 - author_length_pixels/2) 

    #In order to determine the number of pixels making up the space
    #above the text in the font itself, we need to use the method
    #".getbbox()" on the first line of the title. If the title spans
    #multiple lines, the "adjusted_title_cover" is split along the
    #carriage returns ("\n") and the first element is chosen. If the
    #title spans only one line, then the "title" string is used in the
    #".getbbox()" method. The ".getbbox()" method returns a tuple
    #"(x0, y0, x1, y1)", so the it is indexed at the second index ("[1]")
    #to get the vertical pixel at which the text starts on the "y" axis. 
    if adjusted_title_cover != None:
        metrics_string = re.split("\n", adjusted_title_cover)[0].strip()
    else:
        metrics_string = title
    blank_pixels_above_top_of_title = font_title.getbbox(metrics_string)[1]
    
    #The lowest y coordinates of the black and light rectangles are determined below by
    #adding the vertical distances of the elements above it. They add the y coordinate
    #at which the text starts to be written ("vertical_margin_cover_text") to the optional
    #additional pixels on the "y" axis if the user wants there to be a larger vertical margin
    #between the white trim and the text ("pixels_from_top_cover_title_box"), the height
    #of the title ("cover_title_height"), the vertical spacing in-between title and author
    #name ("round(cover_spacing_title_height_ratio*cover_title_height)") if there is an author
    #name, the height of the author name ("cover_author_height") and finally the number of 
    #pixels matching the spacing above the text on top of the rectangle (100 px from the top 
    #of the dark rectangle (see "vertical_margin_cover_text = top_margin_cover_textbox + 100"),
    #the optional additional pixels on the "y" axis ("pixels_from_top_cover_title_box"), 
    #and the space above the text in the font itself ("blank_pixels_above_top_of_title")).
    cover_dark_rectangle_end_y = (vertical_margin_cover_text + pixels_from_top_cover_title_box + 
    cover_title_height + (author != None)*round(cover_spacing_title_height_ratio*cover_title_height) + 
    cover_author_height + (pixels_from_top_cover_title_box + 100 + blank_pixels_above_top_of_title))

    #A filled-in rectangle with rounded corners is drawn on the background using
    #the "rounded_rectangle()" method from the Pillow module. Its top left "x"
    #coordinate is "left_margin_cover_textbox" plus the automatic narrowing of the
    #rectangle according to the value of "extra_horizontal_px_both_sides_of_cover_string", 
    #while its top left "y" coordinate is "top_margin_cover_textbox".
    #Its bottom right "x" coordinate is "right_margin_cover_textbox" minus the
    #automatic narrowing of the rectangle according to the value of
    #"extra_horizontal_px_both_sides_of_cover_string", while its bottom right "y"
    #coordinate is "cover_dark_rectangle_end_y". The radius of the corners are set 
    #to 50 pixels for the darker and larger rectangle and 48 pixels for the smaller
    #lighter rectangle (proportional radius to the decrease in size of the rectangle).

    #The "cover_trim_width_pixels" is calculated from the variable "cover_trim_width"
    #and the known ratio of 4200 pixels per 14 inches at 300 ppi resolution. The
    #"cover_trim_width_pixels" will be used to draw a white trim around the canvas
    #to account for the non-printable area. As such, the rectangle and text containing
    #the title and author information on the front cover will be offset by that amount
    #(split evenly on either side of the rectangle), to keep the margins on either side
    #of the rectangle even despite the presence of such a white trim.

    cover_trim_width_pixels = round(cover_trim_width*300)
    image_editable.rounded_rectangle([(left_margin_cover_textbox + 
    extra_horizontal_px_both_sides_of_cover_string -
    round(cover_trim_width_pixels/2),top_margin_cover_textbox),
    (right_margin_cover_textbox - extra_horizontal_px_both_sides_of_cover_string - 
    round(cover_trim_width_pixels/2), cover_dark_rectangle_end_y)], 
    radius=50, fill=cover_box_color)
    #The lighter rectangle has vertical and horizontal dimensions
    #50 pixels smaller than the larger darker rectangle.
    image_editable.rounded_rectangle([(left_margin_cover_textbox+ 
    extra_horizontal_px_both_sides_of_cover_string + 25 -
    round(cover_trim_width_pixels/2), top_margin_cover_textbox + 25),
    (right_margin_cover_textbox - extra_horizontal_px_both_sides_of_cover_string - 
    25 - round(cover_trim_width_pixels/2), cover_dark_rectangle_end_y - 25)], 
    radius=48, outline=cover_text_color, width=10)

    #If the title was too large to fit within the "available_horizontal_space_pixels",
    #it was split into two lines and will be written in light font (fill = light_text_color)
    #with centered alignment and starting at the "x,y" coordinate "left_margin_cover_text",
    #"vertical_margin_cover_text", using the "multiline_text()" method of the Pillow module
    #with the "adjusted_title_cover" string containing a carriage return "\n" after the
    #"first_half_words_string".

    #The variable "extra_horizontal_px_both_sides_of_cover_string" stores the number
    #of pixels that will be added to the "x" coordinate where the text will start
    #to be written, to account for the automatic narrowing of the dark rectangle.
    
    #The "pixels_from_top_cover_title_box" variable
    #determines how many pixels are added to the
    #starting "y" coordinate (in the unrotated image)
    #from the top of the cover title box to reach the
    #point where the cover title text will start to be
    #written. Negative values will bring the text up.

    #A similar approach is taken with the variable
    #"pixels_from_left_cover_title_box" to determine how
    #many pixels are added to the starting "x" coordinate
    #(in the unrotated image) from the left edge of the
    #cover title box to reach the point where the cover
    #title text will start to be written. Negative
    #values will bring the text left.
                    
    if adjusted_title_cover != None:
        image_editable.multiline_text((left_margin_cover_text + extra_horizontal_px_both_sides_of_cover_string +
        cover_title_offset - round(cover_trim_width_pixels/2) + pixels_from_left_cover_title_box,
        vertical_margin_cover_text + pixels_from_top_cover_title_box),
        adjusted_title_cover, fill=cover_text_color, font=font_title, align="center",
        spacing=cover_title_line_spacing)
    #If the title wasn't split, it will be written using the "text"() method of the Pillow module
    else:
        image_editable.text((left_margin_cover_text + extra_horizontal_px_both_sides_of_cover_string + 
        cover_title_offset - round(cover_trim_width_pixels/2) + pixels_from_left_cover_title_box,
        vertical_margin_cover_text + pixels_from_top_cover_title_box),
        title, fill=cover_text_color, font=font_title, align="center")
    if author != None:
        #A similar approach is taken for the author name, except that since it is written in smaller sized font,
        #it needs a horizontal offset ("cover_author_offset") in order to be centered. Also, the text begins at
        #a lower point in the dark rectangle, which is the "vertical_margin_cover_text" y coordinate plus the
        #height of the title "cover_title_height" and the vertical spacing in-between the title and the author
        #name ("round(cover_spacing_title_height_ratio*cover_title_height)")
        if adjusted_author_cover != None:
            image_editable.multiline_text((left_margin_cover_text + extra_horizontal_px_both_sides_of_cover_string +
            cover_author_offset - round(cover_trim_width_pixels/2) + pixels_from_left_cover_title_box,
            vertical_margin_cover_text + cover_title_height +
            round(cover_spacing_title_height_ratio*cover_title_height)),
            adjusted_author_cover, fill=cover_text_color, font=font_author,
            align="center", spacing=cover_author_line_spacing)
        else:
            image_editable.text((left_margin_cover_text + extra_horizontal_px_both_sides_of_cover_string +
            cover_author_offset - round(cover_trim_width_pixels/2) + pixels_from_left_cover_title_box,
            vertical_margin_cover_text + cover_title_height +
            round(cover_spacing_title_height_ratio*cover_title_height)),
            author, fill=cover_text_color, font=font_author, align="center")
    
    #The recycling symbol image entitled "Universal Recycling Symbol (U+2672).png" was taken 
    #from the following source and is licenced for public domain use ("CC0 Public Domain"):
    #https://www.recycling.com. This image (if present in the working folder) will be pasted
    #onto the back cover to remind users that the paperback books are recyclable.
    path_png = os.path.join(cwd, "Recycling Symbol", "recycling symbol.png")
    png_files = glob.glob(path_png)
    if png_files != []:
        recycling_symbol = Image.open(png_files[0]).convert("RGBA")
        recycling_symbol_width, recycling_symbol_height = recycling_symbol.size
        #The recycling symbol is resized to about 1 inch x 1 inch.
        recycling_symbol = recycling_symbol.resize((round(recycling_symbol_width/recycling_symbol_height*300),
        round(recycling_symbol_height/recycling_symbol_width*300)))
        #The width and height are determined once more after resizing the image.
        recycling_symbol_width, recycling_symbol_height = recycling_symbol.size
        #A list of every pixel of the recycling symbol is collated
        #in the "recycling_symbol_pixels".
        recycling_symbol_pixels = list(recycling_symbol.get_flattened_data())
        #The "new_recycling_symbol_pixels" list wil change every
        #black pixel (originally the arrow fill) to the "recycling_symbol_color"
        #which in most instances should match the color of the "cover_box_color",
        #unless the user passed in a HTML color name instead of an rgb tuple for
        #"cover_box_color". Any other non-transparent pixels (originally grey pixels
        #for the arrow outlines) will be changed to the "cover_text_color" 
        #("recycling_symbol_outline_color"). Any other pixels will be left 
        #unchanged.
        new_recycling_symbol_pixels = []
        for pixel in recycling_symbol_pixels:
            if pixel == (0,0,0,255):
                new_recycling_symbol_pixels.append(recycling_symbol_color)
            elif pixel != (0,0,0,0):
                new_recycling_symbol_pixels.append(recycling_symbol_outline_color)
            else:
                new_recycling_symbol_pixels.append(pixel)
        #The "recycling_symbol" image is overwritten with the new pixels
        #from the "new_recycling_symbol_pixels" list.
        recycling_symbol = Image.new("RGBA", recycling_symbol.size)
        recycling_symbol.putdata(new_recycling_symbol_pixels)
 
    if perforated_cover == True:
        #A white trim of "cover_trim_width_pixels" pixels in width will be drawn on the outer 
        #edges of the canvas. 
        
        #This is the upper horizontal trim white rectangle.
        image_editable.rectangle([(0,0),(paper_height, cover_trim_width_pixels)], fill="white")
        #This is the rightmost vertical trim white rectangle.
        image_editable.rectangle([((paper_height - cover_trim_width_pixels),0),
        (paper_height, paper_width)], fill="white")
        #This is the lower horizontal white rectangle. 
        image_editable.rectangle([(0, paper_width - cover_trim_width_pixels),
        (paper_height, paper_width)], fill="white")
        #This is the leftmost vertical trim white rectangle..
        image_editable.rectangle([(0, 0), (cover_trim_width_pixels, paper_width)], fill="white")
        
        if cover_line == True:
            #If the variable "cover_line" is set to "True" , a dark trim
            #of color "dark_color" is drawn directly within the white border, so as to harmonize
            #the white border with the rest of the contents of the cover and to show the user
            #where to cut the letter page in half to generate the front and back notebook covers.                    
            image_editable.rectangle([(cover_trim_width_pixels, cover_trim_width_pixels),
            (paper_height/2 - 2, paper_width - cover_trim_width_pixels)], outline=cover_box_color, width = 25)
            image_editable.rectangle([(paper_height/2 + 2, cover_trim_width_pixels), 
            (paper_height - cover_trim_width_pixels, paper_width - cover_trim_width_pixels)], 
            outline=cover_box_color, width = 25)

        #A recycling symbol will be added to the back cover
        #of the notebook, if the code could locate the 
        #image in the "Recycling Symbol" subfolder in the 
        #working folder.
        if recycling_symbol != None:
            #The center of the back cover when "perforated_cover" is set to "True"
            #is calculated as the half-point in the page (one half of the longest 
            #dimension of the A4 or US Letter page), minus "cover_trim_width_pixels",
            #which amounts to the back cover horizontal space minus the trim. You then
            #divide that value by two to find the center in the colored area of the
            #back cover. You then add "cover_trim_width_pixels" to reach that point
            #from the beginning of the page.
            #(US Letter: 0.50*11*300 = 1650 px; A4 0.50*297/25.4*300 = 1754 px)
            center_of_back_cover_x = cover_trim_width_pixels + round(((A4 == False)*1650 + (A4 == True)*1754 - cover_trim_width_pixels)/2)
            #The recycling symbol is placed in the lower three-quarters of the back
            #cover on the vertixal axis.
            #(US Letter: round(0.75*2550) = 1913 px; A4: round(0.75*(210/25.4*300)) = 1860 px)
            lower_three_quarter_back_cover_y = (A4 == False)*1913 + (A4 == True)*1860
            #The top left coordinate where the recycling symbol will be pasted is 
            #calculated by subtracting half of its width from the "center_of_back_cover_x",
            #and half of its height from the "lower_three_quarter_back_cover_y" coordinates.
            recycling_symbol_x = round(center_of_back_cover_x - recycling_symbol_width/2)
            recycling_symbol_y = round(lower_three_quarter_back_cover_y - recycling_symbol_height/2)
            #The image is pasted, with the "mask=recycling_symbol" being required so that 
            #the transparency applies correctly during the "paste" method.
            image.paste(recycling_symbol, (recycling_symbol_x,recycling_symbol_y), mask=recycling_symbol)       

    elif perforated_cover == False:
        #The rectangles for the spine are drawn in a similar way as for the title and author name,
        #except that the width depends on the number of pages in the book and the thickness of a
        #ream of paper of 500 pages, which are both provided as additional arguments by the user
        #when running the code. The width of the spine in pixels "width_of_spine_pixels" is
        #determined by multiplying the "inches_per_ream_500_pages" by the number of pages in the
        #book ("number_of_pages"), and then dividing by two (as every sheet of 8.5x11" paper will
        #result in two leaves of the book (each containing two pages) pages in the book) and then
        #by 500 to get the number of inches of thickness for the book. The number of inches is
        #then multiplied by the pixel count for the width of the Legal page in landscape mode
        #(4200 pixels at 300 ppi) and then divided by the corresponding inch measurement for
        #that width (14").
        width_of_spine_pixels = round(inches_per_ream_500_pages*number_of_pages/2/500*300)

        #A white trim of "cover_trim_width_pixels" pixels in width will be drawn on the outer 
        #edges of the canvas, except the left side, where another similar trim will be drawn 
        #where the back cover ends, enabling the user to easily cut out the excess paper from 
        #the Legal cardstock after printing.
        image_editable.rectangle([(0,0),(4200, cover_trim_width_pixels)], fill="white")
        image_editable.rectangle([((4200 - cover_trim_width_pixels),0),(4200, paper_width)], fill="white")
        #This is the lower horizontal white rectangle. It starts at an x0 of 0 and a y0 of 
        #the small side of the A4 or US letter apper format, minus the "cover_trim_width_pixels"
        #(default 0.25 inch or 75 px). The x1 and y1 are the lower right coordinates of the 
        #Legal 8.5x14 inch paper at 300 ppi (4200, 2550) so that the white rectangle extends
        #all the way down the legal page.
        image_editable.rectangle([(0, paper_width - cover_trim_width_pixels),(4200, 2550)], fill="white")
        #This white rectangle is the leftmost vertical rectangle, drawn after the length of 
        #both sides of the cover (which amounts to "paper_height") plus the spine width.
        #The top left corner of the white rectangle is shifted to the left by "2*cover_extra_pixels"
        #pixels, to account for the extra pixels added on the left and right covers. Also, an extra
        #6 pixels (equivalent to about 0.5 mm) are added to the width of the white rectangle on the
        #left vertical side, to allow to cut the line while excluding the pattern on the excess cardstock.
        image_editable.rectangle([(4200-(paper_height + width_of_spine_pixels + 2*cover_extra_pixels + 6),0),
        (4200 - (paper_height + width_of_spine_pixels + 2*cover_extra_pixels) + cover_trim_width_pixels, 
        paper_width)], fill="white")
        
        if cover_line:
            #If the variable "cover_line" is set to "True", a dark trim
            #of color "dark_color" is drawn directly within the white border, so as to harmonize
            #the white border with the rest of the contents of the cover. Once again, the top left
            #corner of the dark rectangle is shifted to the left by "2*cover_extra_pixels"
            #pixels, to account for the extra pixels added on the left and right covers.                    
            image_editable.rectangle([((4200 - (paper_height + width_of_spine_pixels + 
            2*cover_extra_pixels)) + cover_trim_width_pixels, cover_trim_width_pixels),
            (4200 - cover_trim_width_pixels, paper_width - cover_trim_width_pixels)], 
            outline=cover_box_color, width = 25)

        #The "x,y" coordinates of the top left corner of the rectangle are calculated based on the
        #width of the covers of the book (14 inch - 5.5 inch * 300 pixels/inch = 2550 px) 
        #(for A4: (round(14 inch - 297 mm/25.4/2 mm/inch)* 300 pixels/inch) = 2446 px) and 
        #The width of the spine is then subracted in order to reach the left "x" coordinate with
        #the subtraction of "cover_extra_pixels" pixels to account for the space needed to fold
        #the spine and for the added thickness imparted by the glue. The top "y" coordinate is set
        #at one inch from the top of the page (1 inch * 300 pixles/inch = 300 px), and the bottom 
        #"y" coordinate of the bottom right corner is set at one inch from the bottom of the page 
        # (8.5"-1"=7.5", 7.5 inch * 300 pixels/inch = 2250 px) 
        #(for A4: round((210 mm/25.4 mm/inch - 1 inch)*300 pixels/inch) = 2180 px).
        #The bottom "x" coordinate is the same as the top "x" coordinate, except that
        #The "width_of_spine_pixels" isn't subtracted from 2550 px (or 2446 px for A4).
        image_editable.rounded_rectangle([((A4 == False)*2550 + (A4 == True)*2446 - 
        width_of_spine_pixels - cover_extra_pixels, 300),
        ((A4 == False)*2550 + (A4 == True)*2446 - cover_extra_pixels, 
        (A4 == False)*2250 + (A4 == True)*2180)], radius=50, fill=cover_box_color)

        if spine_text == None and author == None:
            spine_text = title
            initialized_author_name = None
        #If the user hasn't specified some text to be included on the spine ("spine_text == None"),
        #the spine string is assembled with the full author name and book title. 
        elif spine_text == None and author != None:
            #The "spine_text" containing the text written on the spine is assembled.
            spine_text = author + " — " + title
        
            #The author name is initialized to take up less space in on the book spine. 
            #First, the name is split at every space or hyphen, with inclusion of those characters as 
            #separate elements in the "author_name_split" list (given the use of parentheses). Then, 
            #the names are cycled through in the "for" loop and initialized accordingly. If there are 
            #no hyphens in the name, then every name up to but not including the last one are 
            #initialized. Otherwise, everything up to the first space is initialized and then 
            #the remaining names are handled differently depending on the number and relative
            #position of the remaining spaces and hyphens in the name.
            if re.search(r"[-—–]", author):
                author_name_split = re.split(r"([- —–])", author)
                space_indices = [i for i in range(len(author_name_split)) if author_name_split[i] == r" "]
                #If a hyphen is present before the first space in the split 
                #author name, it means that the author's first name is 
                #hyphenated.
                hyphenation_indices = [i for i in range(len(author_name_split)) if author_name_split[i] in r"-—–"]
                first_hyphenation_index = hyphenation_indices[0]
                first_space_index = space_indices[0]
                hyphenated_first_name = False
                for i in range(len(author_name_split)):
                    if author_name_split[i] not in r"-—– &":
                        #If the name is already initialized and no space was included
                        #in-between initialized letters, we assume that the hyphenation
                        #has already been done, and we break out of the "for" loop, 
                        #as we do not want the code to extract the first letter only.
                        if len(author_name_split[i]) > 1 and author_name_split[i][-1] == ".":
                            break
                        #If the name is already initialized, but there isn't any
                        #period after the initials, these are added. The resulting
                        #two character initials will behave as the unitialized names
                        #in the code below.
                        elif len(author_name_split[i]) == 1:
                            author_name_split[i] = author_name_split[i].upper() + "."
                        #John Doe-Smith => J. Doe-Smith
                        if i < first_space_index and len(author_name_split[i]) > 1:
                            author_name_split[i] = author_name_split[i][0].upper() + "."
                            if author_name_split[i+1] in r"-—–":
                                hyphenated_first_name = True
                        elif i > first_space_index:
                            if len(hyphenation_indices) == 1:    
                                #J. Doe-Smith => J. Doe-Smith, break out of the loop
                                if len(space_indices) == 1:
                                    break
                                #J. Middlename Doe-Smith => J.M. Doe-Smith, break out of the loop
                                elif len(space_indices) > 1 and hyphenation_indices[0] > space_indices[1]:
                                    author_name_split[i] = author_name_split[i][0] + "."
                                    break
                                #J. Hyphenated-Middlename Doe => J.H.-M. Doe, break out of the loop
                                elif len(space_indices) > 1 and space_indices[1] > hyphenation_indices[0]:
                                    if author_name_split[i-1] not in r"-—–":
                                        author_name_split[i] = author_name_split[i][0] + "."
                                        author_name_split[i+2] = author_name_split[i+2][0] + "."
                                        break
                            #J.-L. Crusher-Picard => J.-L. Crusher-Picard, break out of the loop
                            elif len(hyphenation_indices) > 1 and len(space_indices) == 1:
                                break
                            elif len(hyphenation_indices) > 1 and len(space_indices) > 1:
                                #J.-L. Hyphenated-Middlename Picard => J.-L H.-M. Picard, break out of the loop
                                if space_indices[-1] > hyphenation_indices[-1]:
                                    if author_name_split[i-1] not in r"-—–":
                                        author_name_split[i] = author_name_split[i][0].upper() + "."
                                        author_name_split[i+2] = author_name_split[i+2][0].upper() + "."
                                        break 
                                elif hyphenation_indices[-1] > space_indices[-1]:
                                    #J.-L. Hyphenated-Middlename Crusher-Picard => J.-L. H.-M. Crusher-Picard, break out of the loop
                                    #OR
                                    #J. Hyphenated-Middlename Doe-Smith => J. H.-M. Doe-Smith, break out of the loop
                                    if ((hyphenated_first_name == True and len(hyphenation_indices) == 3) or
                                        (hyphenated_first_name == False and len(hyphenation_indices) == 2)):
                                        #If the next element in "author_name_split" isn't the last hyphen and 
                                        #the previous element isn't a hyphen. Then hyphenated middle name is 
                                        #initialized.
                                        if i+1 != hyphenation_indices[-1] and author_name_split[i-1] not in r"-—–":
                                            author_name_split[i] = author_name_split[i][0].upper() + "."
                                            author_name_split[i+2] = author_name_split[i+2][0].upper() + "."
                                            break
                                    #J.-L. Middlename Crusher-Picard => J.-L. M. Crusher-Picard, break out of the loop
                                    elif hyphenated_first_name == True and len(hyphenation_indices) == 2:
                                        author_name_split[i] = author_name_split[i][0] + "."
                                        break
            #If there are no hyphens in the name, then every name 
            #up to but not including the last one are initialized.
            else:
                author_name_split = re.split(r"([ ])", author)
                for i in range(len(author_name_split)):
                    if i < len(author_name_split)-1 and author_name_split[i] not in r"-—– &":
                        #If the name is already initialized and no space was included
                        #in-between initialized letters, we assume that the hyphenation
                        #has already been done, and we break out of the "for" loop, 
                        #as we do not want the code to extract the first letter only.
                        if len(author_name_split[i]) > 1 and author_name_split[i][-1] == ".":
                            break
                        #If the name is already initialized, but there isn't any
                        #period after the initials, these are added. The resulting
                        #two character initials will behave as the unitialized names
                        #in the code below.
                        elif len(author_name_split[i]) == 1:
                            author_name_split[i] = author_name_split[i].upper() + "."
                            author_name_split[i] = author_name_split[i].upper() + "."

                        author_name_split[i] = author_name_split[i][0].upper() + "."
            #The initialized author name elements in the list "author_name_split"
            #are merged without adding any spaces, as these were preserved in the
            #"re.split()" method.                           
            initialized_author_name = "".join(author_name_split)

        #Similar to what was done above, the font size of the spine
        #initialized to 100 pixels (unless the user specified something different),
        #will be optimized to the available space.
        #However, in this case both the horizontal and vertical
        #space need to be considered, as only one line of text can fit
        #onto the spine (so the string will not be split into two lines
        #as for the title and author box).
        font_spine = ImageFont.truetype(cover_font, spine_font_size)
        spine_text_length_pixels = image_editable.textlength(spine_text, font_spine)
        
        #The function "resize_spine_string" automatically decrements the "spine_font_size"
        #if the "spine_text" is either too tall and/or too wide to fit in the 
        #"available_vertical_space_pixels" and/or "available_horizontal_space_pixels", respectively. 
        #It returns the updated "spine_font_size", "font_spine", along with "spine_text_length_pixels
        #and "spine_text", which may have been modified if the full author name didn't fit in the
        #available space (the author name would then have been initialized).
        def resize_spine_string(spine_font_size, image_editable, spine_text, font_spine, 
        available_vertical_space_pixels, available_horizontal_space_pixels, cover_font, initialized_author_name):
            original_spine_font_size = spine_font_size
            while True:
                #The "spine_text" initially contains the full author name, which is initialized if the 
                #"spine_font_size" drops down to 50, provided that the author name contains at least
                #one space ("author.find(" ") != -1", single name author names aren't initialized, ex: Voltaire). 
                #The font size is then reset to "original_spine_font_size" and the code resizes the initialized 
                #"spine_text" accordingly.
                if spine_font_size < 51 and author != None and author.find(" ") != -1 and spine_text == author + " — " + title:
                    spine_text = initialized_author_name + " — " + title
                    spine_font_size = original_spine_font_size
                    font_spine = ImageFont.truetype(cover_font, spine_font_size)
                if (image_editable.textlength(spine_text, font_spine) > available_vertical_space_pixels or
                spine_font_size > available_horizontal_space_pixels):
                    spine_font_size-=1
                    font_spine = ImageFont.truetype(cover_font, spine_font_size)
                else:
                    spine_text_length_pixels = image_editable.textlength(spine_text, font_spine)
                    if spine_font_size < 40:
                        print("\nYou might need to abbreviate the title for the spine text, as the font size " +
                        "is quite small. You may enter the spine text of your choosing by passing it as a separate " +
                        'argument, after "spine_text:". For example: "spine_text:Your Spine Text".')
                    return spine_text, font_spine, spine_text_length_pixels, spine_font_size                

        #A recycling symbol will be added to the back cover
        #of the notebook, if the code could locate the 
        #image in the "Recycling Symbol" subfolder in the 
        #working folder.
        if recycling_symbol != None:
            #Half of a landscape page gives 1650 px for US Letter and 1754 px for A4.
            #Assuming that pixel x 4200 is located at the right-hand side of the cover page in the
            #unrotated cover image, in order to reach the middle "x" coorinate of the back cover page,
            #we need to proceed as follows. First travel back the distance corresponding to the front
            #cover (1650 px for US Letter or 1754 px for A4) plus "cover_extra_pixels" and then travel 
            #back the "width_of_spine_pixels" to end up on the left side of the spine. In order for the 
            #recycling symbol to be centered on the image (excluding the white trim) on the back cover, 
            #you need to subtract the "cover_trim_width_pixels" white trim width from from the sum of 
            #the back cover width (1650 px for US Letter or 1754 for A4) and "cover_extra_pixels" and 
            #then divide the resulting sum of the distances by two to reach the halfway point.
            
            #(US Letter: 5.5*300 = 1650 px; A4 297/2/25.4*300 = 1754 px)
            center_of_back_cover_x = round(4200 - ((A4 == False)*1650 + 
            (A4 == True)*1754) - width_of_spine_pixels - cover_extra_pixels - (((A4 == False)*1650 + 
            (A4 == True)*1754) + cover_extra_pixels - cover_trim_width_pixels)/2)
            
            #The recycling symbol is placed in the lower three-quarters of the back
            #cover on the vertixal axis.
            #(US Letter: round(0.75*2550) = 1913 px; A4: round(0.75*(210/25.4*300)) = 1860 px)
            lower_three_quarter_back_cover_y = (A4 == False)*1913 + (A4 == True)*1860
            #The top left coordinate where the recycling symbol will be pasted is 
            #calculated by subtracting half of its width from the "center_of_back_cover_x",
            #and half of its height from the "lower_three_quarter_back_cover_y" coordinates.
            recycling_symbol_x = round(center_of_back_cover_x - recycling_symbol_width/2)
            recycling_symbol_y = round(lower_three_quarter_back_cover_y - recycling_symbol_height/2)
            #The image is pasted, with the "mask=recycling_symbol" being required so that 
            #the transparency applies correctly during the "paste" method.
            image.paste(recycling_symbol, (recycling_symbol_x,recycling_symbol_y), mask=recycling_symbol)
        
        #Similarly to the title and author box, a white rectangle 25 pixels distant from the edge
        #of the black rectangle (25 pixels down from the start of the spine dark rectangle, which
        #itself starts 1 inch from the top of the page (1 inch * 300 pixels/inch + 25 px = 325 px))
        #is drawn only if the number of pages is over 300, as its presence
        #decreases the available space for the spine text.
        if number_of_pages >= 300:
            image_editable.rounded_rectangle([((A4 == False)*2550 + (A4 == True)*2446 - 
            width_of_spine_pixels + 25 - cover_extra_pixels, 325),
            ((A4 == False)*2550 + (A4 == True)*2446 - 25 - cover_extra_pixels, 
            (A4 == False)*2250 + (A4 == True)*2180 - 25)], radius=round((width_of_spine_pixels
            -50)/width_of_spine_pixels*50), outline=cover_text_color, width=10)

            #The available space on the horizontal axis is determined by subtracting the
            #"x" coordinate of the bottom right corner of the spine dark rectangle from
            #that of the top left corner. 70 pixels are subtracted from that amount to
            #account for the space between the pale rectangle vertical edges and the text.
            available_horizontal_space_pixels = (round(((A4 == False)*2550 + (A4 == True)*2446 - 25) -
            ((A4 == False)*2550 + (A4 == True)*2446 - width_of_spine_pixels + 25)) - 70)
            #As there is one inch above and below the dark rectangle, the height of the
            #dark rectangle is equal to the width of the US Letter or A4 page (as it is 
            #in landscape mode) minus two inches (2 inch * 300 pixels/inch = 600 px). 
            #50 pixels are subtracted to account for the margins between the edges of the
            #dark rectangle and the lighter line, and another 70 pixels are subtracted 
            #from that amount to allow for space between the pale rectangle horizontal 
            #edges and the text (600+50+70 = 720 px).
            available_vertical_space_pixels = paper_width-720             

            #If either the length of the "spine_text" in pixels ("spine_text_length_pixels")
            #exceeds the "available_vertical_space_pixels" or if the height of the spine font
            #"spine_font_size" is above the "available_horizontal_space_pixels", the "spine_font_size"
            #will be decremented until both dimensions are within range of the available space.
            if (spine_text_length_pixels > available_vertical_space_pixels or
            spine_font_size > available_horizontal_space_pixels):

                spine_text, font_spine, spine_text_length_pixels, spine_font_size = resize_spine_string(spine_font_size, image_editable, 
                spine_text, font_spine, available_vertical_space_pixels, available_horizontal_space_pixels, cover_font, 
                initialized_author_name)

            #The offset on the x and y axis are determined by subtracting the halfpoint of
            #either dimension of the "spine_text" from the that of the available space in
            #the corresponding dimension of the rectangle. In the case of "offset_y", the
            #"pixels_from_bottom_cover_spine" are subtracted from it in order to bring the
            #text further up from the bottom of the spine dark rectangle. This allows to
            #fine-tune the automatic centering on the vertixal axis, given that the spine
            #is fairly narrow and any unevenness are easily noticeable. Furthermore, the 
            #"blank_pixels_above_top_of_spine" accounts for the fact that the text does 
            #not start at the "y" coordinate of zero in the bounding box. The method 
            #".getbbox(spine_text)" provides a tuple "(x0, y0, x1, y1)", so indexing at
            #the second index ("[1]") allows to get the starting vertical pixel in the 
            #bounding box at which the text starts to be written. A similar approach
            #is taken with the variable "pixels_from_left_cover_spine", where pixels are
            #added to the "x" axis (in the rotated image) to adjust the point where the
            #spine text will start to be written.
            offset_x = (round(available_vertical_space_pixels/2 - spine_text_length_pixels/2) +
            pixels_from_left_cover_spine)
            blank_pixels_above_top_of_spine = font_spine.getbbox(spine_text)[1]
            offset_y = (round(available_horizontal_space_pixels/2 - spine_font_size/2) +
            cover_extra_pixels - blank_pixels_above_top_of_spine - pixels_from_bottom_cover_spine)

            #The image is outputted in PNG format.
            image.save(title + " (cover).png", "PNG")

            #As text can only be written horizontally in Pillow, the image is reloaded and
            #rotated 90 degrees clockwise in order to write the text on the spine.
            image_rotated = (Image.open(title +
            " (cover).png").convert("RGB").rotate(90, expand = True))
            image_rotated_editable = ImageDraw.Draw(image_rotated)

            #The starting x and y coordinates mirror the measurements in the unrotated image.
            #The left side of the dark rectangle is then one inch (300 px) from the side of the 
            #canvas in the rotated image, with 25 pixels added to reach the light line and another
            #35 pixels (300 + 25 + 35 = 360) to reach the point where the text will start to be 
            #written, with the addition of the "offset_x".
            spine_text_starting_x = 360 + offset_x
            #The top of the dark rectangle now stands 5.5 inches from the top of the canvas for
            #US Letter book pages (the origin 0,0 being in the top left corner, 
            #or 297 mm /25.4 mm/inch/2 for A4 paper), 
            #with 25 pixels added to reach the lighter line, and 40 more pixels 
            #to reach the point where the text will start to be written, with the 
            #addition of the "offset_y"
            
            #For US Letter:  5.5 inch * 300 pixels/inch + 65 px = 1715 px
            #For A4: 297 mm /25.4 mm/inch/2 * 300 pixels/inch + 65 = 1819 px
            
            if A4:
                spine_text_starting_y = 1819 + offset_y
            else:
                spine_text_starting_y = 1715 + offset_y

            image_rotated_editable.text((spine_text_starting_x, spine_text_starting_y),
            spine_text, fill=cover_text_color, font=font_spine, align="center")

        #If the "number_of_pages" is below 300, the white rectangle will not be drawn to allow
        #for more space for the text on a smaller spine. The margins are adjusted in consequence.
        else:
            #The available space on the horizontal axis is determined by subtracting the
            #"x" coordinate of the bottom right corner of the spine dark rectangle from
            #that of the top left corner. 70 pixels are subtracted from that amount to
            #account for the space between the dark rectangle vertical edges and the text.
            available_horizontal_space_pixels = ((((A4 == False)*2550 + (A4 == True)*2446) -
            ((A4 == False)*2550 + (A4 == True)*2446 - width_of_spine_pixels))-70)

            #As there is one inch above and below the dark rectangle, the height of the
            #dark rectangle is equal to the width of the US Letter or A4 page (as it is 
            #in landscape mode) minus two inches (2 inch * 300 pixels/inch = 600 px). 
            #70 pixels are subtracted from that amount to allow for space between the dark 
            #rectangle horizontal edges and the text (600+70 = 670 px).
            available_vertical_space_pixels = paper_width-670           

            #If either the length of the "spine_text" in pixels ("spine_text_length_pixels")
            #exceeds the "available_vertical_space_pixels" or if the height of the spine font
            #"spine_font_size" is above the "available_horizontal_space_pixels", the "spine_font_size"
            #will be decremented until both dimensions are within range of the available space.
            if (spine_text_length_pixels > available_vertical_space_pixels or
            spine_font_size > available_horizontal_space_pixels):

                spine_text, font_spine, spine_text_length_pixels, spine_font_size = resize_spine_string(spine_font_size, image_editable, 
                spine_text, font_spine, available_vertical_space_pixels, available_horizontal_space_pixels, cover_font, 
                initialized_author_name)
                
            #The offset on the x and y axis are determined by subtracting the halfpoint of
            #either dimension of the "spine_text" from the that of the available space in
            #the corresponding dimension of the rectangle. In the case of "offset_y", the
            #"pixels_from_bottom_cover_spine" are subtracted from it in order to bring the
            #text further up from the bottom of the spine dark rectangle. This allows to
            #fine-tune the automatic centering on the vertixal axis, given that the spine
            #is fairly narrow and any unevenness are easily noticeable. Furthermore, the 
            #"blank_pixels_above_top_of_spine" accounts for the fact that the text does 
            #not start at the "y" coordinate of zero in the bounding box. The method 
            #".getbbox(spine_text)" provides a tuple "(x0, y0, x1, y1)", so indexing at
            #the second index ("[1]") allows to get the starting vertical pixel in the 
            #bounding box at which the text starts to be written.
            offset_x = (round(available_vertical_space_pixels/2 - spine_text_length_pixels/2) +
            pixels_from_left_cover_spine)
            blank_pixels_above_top_of_spine = font_spine.getbbox(spine_text)[1]
            offset_y = (round(available_horizontal_space_pixels/2 - spine_font_size/2) +
            cover_extra_pixels - blank_pixels_above_top_of_spine - pixels_from_bottom_cover_spine)

            #The image is outputted in PNG format.
            image.save(title + " (cover).png", "PNG")

            #As text can only be written horizontally in Pillow, the image is reloaded and
            #rotated 90 degrees clockwise in order to write the text on the spine.
            image_rotated = (Image.open(title +
            " (cover).png").convert("RGB").rotate(90, expand = True))
            image_rotated_editable = ImageDraw.Draw(image_rotated)

            #The starting x and y coordinates mirror the measurements in the unrotated image.
            #The left side of the dark rectangle is then one inch (300 px) from the side of 
            #the canvas in the rotated image, with 35 pixels added pixels (300 + 35 = 335) 
            #to reach the point where the text will start to be written, with the addition 
            #of the "offset_x".
            spine_text_starting_x = 335 + offset_x
            #The top of the dark rectangle now stands 5.5 inches from the top of the canvas for
            #US Letter book pages (the origin 0,0 being in the top left corner, 
            #or 297 mm /25.4 mm/inch/2 for A4 paper), with 40 pixels added to 
            #reach the point where the text will start to be written, with the 
            #addition of the "offset_y"
            
            #For US Letter:  5.5 inch * 300 pixels/inch + 40 px = 1690 px
            #For A4: 297 mm /25.4 mm/inch/2 * 300 pixels/inch + 40 = 1794 px 
            if A4:
                spine_text_starting_y = 1794 + offset_y
            else:
                spine_text_starting_y = 1690 + offset_y

            image_rotated_editable.text((spine_text_starting_x, spine_text_starting_y),
            spine_text, fill=cover_text_color, font=font_spine, align="center")    
        
    #The image is once more outputted in PDF format, and the original
    #unrotated PNG image is deleted.
    if not os.path.exists(os.path.join(cwd, "Notebooks")):
        os.makedirs(os.path.join(cwd, "Notebooks"))
    os.makedirs(os.path.join(cwd, "Notebooks", str(date.today()) +
    "-" + title))
    
    if perforated_cover == True:
        image.save(os.path.join(cwd, "Notebooks", str(date.today()) +
        "-" + title, str(date.today()) + "-" + title + " (cover).pdf"),
        quality=100, resolution=300)
    else:
        image_rotated.save(os.path.join(cwd, "Notebooks", str(date.today()) +
        "-" + title, str(date.today()) + "-" + title + " (cover).pdf"),
        quality=100, resolution=300)
        os.remove(title + " (cover).png")


    current_page = 1
    page_numbers_list = list(range(1, number_of_pages+1))

    #The function "get_line_y_coordinates" determines the "y" coordinates of
    #the lines drawn for the ruled pages (college ruled, wide rule or custom ruled lines).
    def get_line_y_coordinates(line_distance_inches, line_width):
        #The starting "y" pixel is initialized as the
        #highest pixel outside of the quarter-inch
        #non-printable area ("top_margin_y_pixel"), and
        #is incremented by the distance in-between lines
        #(in pixels, "pixel_increment") after each run
        #through the "while" loop. This allows to gather
        #all of the line "y" coordinates.
        starting_y = top_margin_y_pixel
        pixel_increment = round(line_distance_inches*300)
        line_y_coordinates = []
        while starting_y <= bottom_margin_y_pixel:
            line_y_coordinates.append(starting_y)
            starting_y += pixel_increment
        return line_y_coordinates

    #The function "get_line_y_coordinates_TOC" determines the 
    #"y" coordinates of the lines drawn for the ruled pages for 
    #the TOC (college ruled, wide rule or custom ruled lines).
    def get_line_y_coordinates_TOC(line_distance_inches, line_width):
        starting_y = top_margin_y_pixel
        pixel_increment = round(line_distance_inches*300)
        line_y_coordinates = []
        #The bottom margin for TOC pages is 0.25 inch
        #instead of 0.6 inch, as the TOC pages do not
        #need to accomodate page numbers.
        while starting_y <= bottom_margin_y_pixel_TOC:
            line_y_coordinates.append(starting_y)
            starting_y += pixel_increment
        return line_y_coordinates
    
    def get_dot_y_coordinates_TOC(inches_between_dots, dot_diameter_pixels):
        starting_y = top_margin_y_pixel
        pixel_increment = round(inches_between_dots*300)
        dot_y_coordinates = []
        while starting_y <= bottom_margin_y_pixel_TOC:
            dot_y_coordinates.append(starting_y)
            starting_y += pixel_increment
        return dot_y_coordinates

    #The "if" and "elif" statements below return the list of "y" coordinates
    #("line_y_coordinates") and the list of the two last "y" coordinates ("two_last_y_lines").
    #The latter will be important when lining up the lines of the ruled lines and
    #dots or graph squares, so that they end at around the same "y" coordinate at the
    #bottom of the page. The "line_width" in pixels, and the line spacing in inches
    #get passed into the "get_line_y_coordinates" function (9/32 of an inch for
    #college ruled, 11/32 of an inch for wide ruled and the "custom_line_distance_inches"
    #for custom line width).
    if college_ruled == True or college_ruled_left == True or college_ruled_right == True:
        line_y_coordinates = get_line_y_coordinates(9/32, line_width)
        two_last_y_lines = [line_y_coordinates[-2], line_y_coordinates[-1]]

    elif wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True:
        line_y_coordinates = get_line_y_coordinates(11/32, line_width)
        two_last_y_lines = [line_y_coordinates[-2], line_y_coordinates[-1]]

    elif custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True:
        line_y_coordinates = get_line_y_coordinates(custom_line_distance_inches, line_width)
        two_last_y_lines = [line_y_coordinates[-2], line_y_coordinates[-1]]

    def get_line_y_coordinates_graph_paper(line_distance_inches, graph_line_width):
        if ((graph_paper_left == True or graph_paper_right == True) and (dot_grid_left == True or
        dot_grid_right == True)):
            starting_y = top_margin_y_pixel
        else:
            starting_y = top_margin_y_pixel
        pixel_increment = round(line_distance_inches*300)
        line_y_coordinates_graph = []
        while starting_y <= bottom_margin_y_pixel:
            line_y_coordinates_graph.append(starting_y)
            starting_y += pixel_increment
        return line_y_coordinates_graph

    if graph_paper == True or graph_paper_left == True or graph_paper_right == True:
        line_y_coordinates_graph = get_line_y_coordinates_graph_paper(1/squares_per_inch, graph_line_width)
        two_last_y_graph = [line_y_coordinates_graph[-2], line_y_coordinates_graph[-1]]

    def get_dot_y_coordinates(inches_between_dots, dot_diameter_pixels):
        starting_y = top_margin_y_pixel
        pixel_increment = round(inches_between_dots*300)
        dot_y_coordinates = []
        while starting_y <= bottom_margin_y_pixel:
            dot_y_coordinates.append(starting_y)
            starting_y += pixel_increment
        return dot_y_coordinates

    if dot_grid == True or dot_grid_left == True or dot_grid_right == True:
        dot_y_coordinates = get_dot_y_coordinates(inches_between_dots, dot_diameter_pixels)
        two_last_y_dots = [dot_y_coordinates[-2], dot_y_coordinates[-1]]

    #The function "get_last_y" will compare the last "y" coordinate
    #for any two ruled/dot/graph formats in order to line them up
    #better at the bottom of the page.
    def get_last_y(y_coordinates_1, y_coordinates_2):
        #If the last "y" coordinate for "y_coordinate_2" is
        #greater (further down the page, "y_coordinates_1[-1] <
        #y_coordinates_2[-1]") with respect to that
        #of "y_coordinate_1", then the two last "y" coordinates
        #of "y_coordinates_2" are compared with the last "y"
        #coordinate of "y_coordinate_1" in order to determine
        #which is closest (which has a lower absolute value
        #difference). If the penultimate "y" coordinate from
        #"y_coordinates_2" is closest to the last coordinate of
        #"y_coordinates_1", then the last coordinate from
        #"y_coordinates_2" is removed ("y_coordinates_2.pop(-1)"),
        #in order to keep the end of pages as even as possible.
        if y_coordinates_1[-1] < y_coordinates_2[-1]:
            if (abs(y_coordinates_2[-2]-y_coordinates_1[-1]) <
            abs(y_coordinates_2[-1]-y_coordinates_1[-1])):
                y_coordinates_2.pop(-1)
                maximum_y_coordinate = max([y_coordinates_1[-1], y_coordinates_2[-1]])
                return maximum_y_coordinate, y_coordinates_1, y_coordinates_2
            else:
                maximum_y_coordinate = max([y_coordinates_1[-1], y_coordinates_2[-1]])
                return maximum_y_coordinate, y_coordinates_1, y_coordinates_2
        #The reverse is done in the "elif" statement.
        elif y_coordinates_1[-1] > y_coordinates_2[-1]:
            if (abs(y_coordinates_1[-2]-y_coordinates_2[-1]) <
            abs(y_coordinates_1[-1]-y_coordinates_2[-1])):
                y_coordinates_1.pop(-1)
                maximum_y_coordinate = max([y_coordinates_1[-1], y_coordinates_2[-1]])
                return maximum_y_coordinate, y_coordinates_1, y_coordinates_2
            else:
                maximum_y_coordinate = max([y_coordinates_1[-1], y_coordinates_2[-1]])
                return maximum_y_coordinate, y_coordinates_1, y_coordinates_2
        else:
            #since both last "y" coordinates are equal in value, one of them is returned
            #as the "maximum_y_coordinate"
            return y_coordinates_1[-1], y_coordinates_1, y_coordinates_2

    #In the case of ScriptReader custom dot grid pages, the final line displayed on the page
    #will not necessarily line up with the final "dot_y_coordinates" list item, so it isn't
    #important to line it up with the TOC. That is to say that the dot grid lines that will
    #be visible will be alternated with some empty lines, to accomodate for ascenders and
    #descenders when handwriting. The "y" coordinate of the last line will then depend on
    #the values of the dot spacing ("inches_between_dots") and number of empty lines in-between
    #lines of text ("lines_between_text") variables.
    if (scriptreader == True or scriptreader_left == True or scriptreader_right == True or scriptreader_acetate == True):
        dot_y_coordinates = get_dot_y_coordinates(inches_between_dots, dot_diameter_pixels)
        #The list of line indices where characters will be segmented ("text_line_numbers")
        #is initialized including the zero index, as the first line of text needs to be
        #on the first line, and then at a regular interval thereafter after that. There
        #is a default of three empty lines in-between every line of text, to minimize
        #the overlapping of ascenders and descenders of adjacent text lines.
        text_line_numbers = [0, 1]
        #Here there is one less dot than the total number of lines, so there is no
        #need to add "+1" after "len(dot_y_coordinates)"
        for j in range(len(dot_y_coordinates)):
            #If the current "dot_y_coordinates" list index is prior to the penultimate
            #list index (as room needs to be provided to add a "y" coordinate and the next one,
            #so as to frame a line of text in-between two successive horizontal dot lines), and
            #if the current index is equal to that of the last text line, plus the number
            #of empty lines in-between text lines, then it is included in the list of
            #text line indices "text_line_numbers".
            if j < len(dot_y_coordinates)-2 and j == text_line_numbers[-1] + lines_between_text:
                text_line_numbers.append(j)
                text_line_numbers.append(j+1)
        #If the lower "y" coordinate of the last set of two successive horizontal dot lines framing
        #a text line, plus the pixel diameter of a dot, plus the vertical overlap allocated to
        #accomodate for ascenders and descenders when handwriting (round(0.40*lines_between_text*
        #inches_between_dots*300)) is inferior to the lower margin of the page ("bottom_margin_y_pixel"),
        #it means that there is likely to be excessive space at the bottom of the page, relative to the space
        #above the header. To improve the page layout esthetics, the whole page will be shifted down by the
        #difference in pixels in-between the lower margin of the page and point described above, by adjusting
        #the margins accordingly. All of the "y_coordinate" lists therefore need to be recalculated at this
        #point, to reflect the changes in margins.
        top_y_shift = 0
        if (dot_y_coordinates[text_line_numbers[-1]] + dot_diameter_pixels +
        round(0.40*lines_between_text*inches_between_dots*300) < bottom_margin_y_pixel):
            top_y_shift = (bottom_margin_y_pixel-dot_y_coordinates[text_line_numbers[-1]] -
            (dot_diameter_pixels + round(0.40*lines_between_text*inches_between_dots*300)))
            heading_top_margin_y_pixel += top_y_shift
            top_margin_y_pixel += top_y_shift
            bottom_margin_y_pixel -+ (bottom_margin_y_pixel-dot_y_coordinates[text_line_numbers[-1]] +
            (dot_diameter_pixels + round(0.40*lines_between_text*inches_between_dots*300)))
            dot_y_coordinates = get_dot_y_coordinates(inches_between_dots, dot_diameter_pixels)
            two_last_y_dots = [dot_y_coordinates[-2], dot_y_coordinates[-1]]
            if college_ruled == True or college_ruled_left == True or college_ruled_right == True:
                line_y_coordinates = get_line_y_coordinates(9/32, line_width)
                two_last_y_lines = [line_y_coordinates[-2], line_y_coordinates[-1]]
            elif wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True:
                line_y_coordinates = get_line_y_coordinates(11/32, line_width)
                two_last_y_lines = [line_y_coordinates[-2], line_y_coordinates[-1]]
            elif custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True:
                line_y_coordinates = get_line_y_coordinates(custom_line_distance_inches, line_width)
                two_last_y_lines = [line_y_coordinates[-2], line_y_coordinates[-1]]
            if graph_paper == True or graph_paper_left == True or graph_paper_right == True:
                line_y_coordinates_graph = get_line_y_coordinates_graph_paper(1/squares_per_inch, graph_line_width)
                two_last_y_graph = [line_y_coordinates_graph[-2], line_y_coordinates_graph[-1]]

        #If the ScriptReader custom dot grid pages are used in combination with another type of
        #page, then the same page number alignment will be used, taking into account the
        #"page_number_vertical_center_point" that was calculated for the other type of page.
        #Otherwise, if the user didn't input an measurement for "page_numbers_bottom_margin:" or
        #"page_numbers_bottom_margin_cm:", the default value of "page_width-(75 + page_numbers_font_size/2)" 
        #for "page_numbers_bottom_margin_y_pixel" will be used.
        maximum_y_coordinate = dot_y_coordinates[-1]
        page_number_vertical_center_point = (paper_width - maximum_y_coordinate)/2
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - page_numbers_font_size/2 > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point


    #The three "if" and "elif" statements below determine what type of lines/dots
    #are present on the left and right pages. If it is a combination of dots and
    #graph paper ("if" statement), or dots and lines (first "elif" statement) or
    #graph paper and lines (second "elif" statement), then the corresponding
    #lists of "y" coordinates are passed into the "get_last_y" function in order
    #to ensure that both pages end as closely as possible on the "y" axis.
    if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
    (graph_paper == True or graph_paper_left == True or graph_paper_right == True)):
        maximum_y_coordinate, dot_y_coordinates, line_y_coordinates_graph = get_last_y(dot_y_coordinates, line_y_coordinates_graph)
        #The variable "page_numbers_bottom_margin_y_pixel" designates
        #the "y" coordinate mapping to the vertical middle point of the
        #page numbers. By default, this variable is set as "None", and the
        #user can either set it manually, or the code will determine whether there
        #is sufficient space to vertically center the page numbers in the space
        #in-between the last horizontal line and the bottom of the page. Should
        #there be less than 75 pixels below the page number for it to be
        #vertically centered, the code will automatically bring the text up,
        #such that the lowest "y" pixel of the page number is above 75 pixels
        #from the bottom of the page, thereby respecting the default 0.25 inch
        #non-printable area for most printers.
        page_number_vertical_center_point = (paper_width-maximum_y_coordinate)/2
        
        
        #If the user hasn't specified a value for "page_numbers_bottom_margin_y_pixel" and
        #the center "y" coordinate of the page numbers, when half the font size in pixels are subtracted
        #from it (to give the lowest "y" coordinate of the page numbers) is greater than 75 pixels
        #(the equivalent of 0.25 inch at 300 ppi, 0.25 in * 300 px/in = 75 px), it means that
        #there is enough room to center the text and the value of "page_numbers_bottom_margin_y_pixel"
        #is set to that corresponding pixel.
        
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - page_numbers_font_size/2 > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point
    elif ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
    (college_ruled == True or college_ruled_left == True or college_ruled_right == True or
    wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True or
    custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True)):
        maximum_y_coordinate, dot_y_coordinates, line_y_coordinates = get_last_y(dot_y_coordinates, line_y_coordinates)
        page_number_vertical_center_point = (paper_width-maximum_y_coordinate)/2
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - (page_numbers_font_size/2) > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point
    elif ((graph_paper == True or graph_paper_left == True or graph_paper_right == True) and
    (college_ruled == True or college_ruled_left == True or college_ruled_right == True or
    wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True or
    custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True)):
        maximum_y_coordinate, line_y_coordinates_graph, line_y_coordinates = get_last_y(line_y_coordinates_graph, line_y_coordinates)
        page_number_vertical_center_point = (paper_width-maximum_y_coordinate)/2
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - page_numbers_font_size/2 > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point
    #If the notebook doesn't contain ruled pages and has dot grids or custom ScriptReader
    #dot grids (left pages, right pages or both pages), then dots lining up with the horizontal
    #lines of the dot grid pages will be drawn on the TOC. The function "get_dot_y_coordinates" is
    #called instead of "get_line_y_coordinates" in this case. This will allow users to use the
    #"High Five" indexing method, as the TOC lines and dots line up. Otherwise, the "y" coordinates
    #of the lines of the TOC will be gathered using the "get_line_y_coordinates" function.
    if (college_ruled == False and college_ruled_left == False and college_ruled_right == False and
    wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False and
    custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False and
    (dot_grid == True or dot_grid_left == True or dot_grid_right == True)):
        dot_y_coordinates_TOC = get_dot_y_coordinates_TOC(TOC_line_spacing, TOC_line_width)
    else:
        line_y_coordinates_TOC = get_line_y_coordinates_TOC(TOC_line_spacing, TOC_line_width)

    #The following "if" and "elif" statements deal with notebooks comprised of only one
    #design (ruled lines, graph paper or dot grids) or combinations of any one of those
    #designs with blank pages. The "page_number_vertical_center_point" variable stores the
    #"y" coordinate of the center of the blank space beneath the final line, or dot grid line
    #on the page. This will help the code to vertically center the page numbers on the page.
    if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
    (graph_paper == False and graph_paper_left == False and graph_paper_right == False) and
    (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
    (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
    (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)): 
        page_number_vertical_center_point = (paper_width-dot_y_coordinates[-1])/2
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - page_numbers_font_size/2 > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point
    elif ((dot_grid == False and dot_grid_left == False and dot_grid_right == False) and
    (graph_paper == True or graph_paper_left == True or graph_paper_right == True) and
    (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
    (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
    (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
        page_number_vertical_center_point = (paper_width-line_y_coordinates_graph[-1])/2
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - page_numbers_font_size/2 > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point
    elif ((dot_grid == False and dot_grid_left == False and dot_grid_right == False) and
    (graph_paper == False and graph_paper_left == False and graph_paper_right == False) and
    ((college_ruled == True or college_ruled_left == True or college_ruled_right == True) or
    (wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True) or
    (custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True))):
        page_number_vertical_center_point = (paper_width-line_y_coordinates[-1])/2
        if (default_page_numbers_bottom_margin_y_pixel == True and
        (page_number_vertical_center_point - page_numbers_font_size/2 > 75)):
            page_numbers_bottom_margin_y_pixel = paper_width - page_number_vertical_center_point

    #If the user has "erased" the default values for the TOC subheadings by passing in "TOC_pages_text:" and
    #"TOC_subject_text:", then the first line or dot grid horizontal line of the TOC will start at index 0,
    #Otherwise, a line is skipped to leave room for the subheadings.
    if TOC_pages_text == "" and TOC_subject_text == "":
        first_TOC_line_index = 0
    #If the TOC will have dot grids instead of ruled lines (only when the notebook only has 
    #dot grid pages), then the two first line indices (0 and 1) are skipped over, so that
    #the first line of dots isn't too close to the subheadings.
    elif ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
    (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
    (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
    (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
        first_TOC_line_index = 2
    else:
        first_TOC_line_index = 1

    #A new blank canvas in landscape format (in A4 or US Letter format)
    #is created for every page of the notebook. An editable version is created to allow
    #for modifications ("blank_canvas_editable").
    for i in range(round((total_number_of_pages)/2)):
        blank_canvas = Image.new("RGB", (paper_height, paper_width), (255,255,255))
        blank_canvas_editable = ImageDraw.Draw(blank_canvas)

        #If the user didn't discard the table of contents ("TOC_pages_list != []") by entering zero
        #pages ("TOC_pages_spacing:0") and if the first page in "TOC_pages_list" is an odd number
        #(the first page of the list is popped out upon drawing a TOC page, hence this verification),
        #then the TOC heading is written on the right-hand (odd numbered) page. If the notebook
        #pages only contain dot grids, then the TOC page will contain dot grids as well, otherwise
        #the TOC pages will have ruled lines.
        if TOC_pages_list != [] and (TOC_pages_list[0])%2 != 0:
            if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
            (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
            (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
            (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
                #Using the ImageDraw module, some ellipses are drawn, with a square dimensioned
                #bounding box, giving the corresponding circles with a diameter of "dot_diameter_pixels".
                #The dots are evenly spaced on the horizontal and vertical axes by a distance of
                #"inches_between_dots*300" pixels, as there are 2550 pixels in 8.5 inches at an image
                #resolution of 300 ppi. The first horizontal line of dots at index 0 of "dot_y_coordinates_TOC"
                #is skipped over in order to allow for some space for the "Pages" and "Subject" subheadings
                #below the "Contents" TOC heading.
                for j in range(first_TOC_line_index, len(dot_y_coordinates_TOC)):
                    #Here half of the diameter of the dots ("round(dot_diameter_pixels/2)")
                    #is subtracted from "right_margin_x_pixel" to ensure that the right edge of the 
                    #rightmost dots is within the border (otherwise half of the dot would
                    #be outside of the border horizontally)
                    starting_x = right_margin_x_pixel - round(dot_diameter_pixels/2)
                    while starting_x >= (paper_height/2+gutter_margin_width_pixels):
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates_TOC[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates_TOC[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x -= round(inches_between_dots*300)
            else:
                #The lines are then drawn for each of the "y" coordinates within the "line_y_coordinates_TOC"
                #list, starting at the "x" coordinate to the right of the gutter margin on the odd pages
                #("paper_height/2 + gutter_margin_width_pixels", so starting at the halfway point of the page on the
                #horizontal axis (paper_height/2 pixels), and then adding the number of pixels for the width of the
                #gutter margin), and ending at the right margin ("right_margin_x_pixel").
                for j in range(first_TOC_line_index, len(line_y_coordinates_TOC)):
                    blank_canvas_editable.line([(paper_height/2+gutter_margin_width_pixels, line_y_coordinates_TOC[j]),
                    (right_margin_x_pixel, line_y_coordinates_TOC[j])], fill = TOC_line_color, width = line_width)
            #The headers will be centered, using the "x" coordinate located at
            #three quarter of the page width pixels ("paper_height*0.75") and "y" coordinate at the
            #top of the upper margin ("heading_top_margin_y_pixel").
            blank_canvas_editable.text((round(paper_height/2 + paper_height/4+gutter_margin_width_pixels/2-left_margin_x_pixel/2), heading_top_margin_y_pixel),
            TOC_heading_text, fill=TOC_heading_text_color, font=TOC_heading_font, anchor="ms")
            #The "page" and "Subject" headings are written at a vertical distance 1.5 times the heading text size,
            #to ensure that it is always proportionally spaced to the "Contents" heading. The horizontal alignment
            #for the "pages" heading is set to the midway point of the horizontal dimension of the blank canvas
            #(paper_height/2 pixels, plus a quarter of the right page, with middle baseline "ms" anchoring.
            #On the other hand, the "Subject" heading is written a three-quarters of the page width to the right
            #of the midway point of the page.
            blank_canvas_editable.text((round(paper_height/2 + 0.25*paper_height/2+gutter_margin_width_pixels/2-left_margin_x_pixel/2), heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_pages_text, fill=TOC_pages_text_color, font=TOC_pages_font, anchor="ms")
            blank_canvas_editable.text((round(paper_height/2+ 0.75*paper_height/2+gutter_margin_width_pixels/2-left_margin_x_pixel/2), heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_subject_text, fill=TOC_subject_text_color, font=TOC_pages_font, anchor="ms")
        #A similar approach is taken if the first page in the "TOC_pages_list" is an even number.
        #Here the "scriptreader_acetate == False" needs to be met because the notebook printed on
        #transparencies (acetates) can only be written on one side, which is the right side by default.
        #The code will flip the image when the "scriptreader_acetate" page will be completely generated,
        #allowing it to be printed on the left-hand side and the user will write on the opposite right-hand side.
        elif scriptreader_acetate == False and TOC_pages_list != [] and (TOC_pages_list[0])%2 == 0:
            if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
            (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
            (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
            (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
                for j in range(first_TOC_line_index, len(dot_y_coordinates_TOC)):
                    #Here half of the diameter of the dots ("round(dot_diameter_pixels/2)")
                    #is added to "left_margin_x_pixel" to ensure that the left edge of the 
                    #leftmost dots is within the border (otherwise half of the dot would
                    #be outside of the border horizontally)
                    starting_x = left_margin_x_pixel + round(dot_diameter_pixels/2)
                    while starting_x <= paper_height/2-gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates_TOC[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates_TOC[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x += round(inches_between_dots*300)
            else:
                for j in range(first_TOC_line_index, len(line_y_coordinates_TOC)):
                    blank_canvas_editable.line([(left_margin_x_pixel, line_y_coordinates_TOC[j]),
                    (paper_height/2-gutter_margin_width_pixels, line_y_coordinates_TOC[j])], fill = TOC_line_color, width = line_width)
            blank_canvas_editable.text((round(paper_height/4-gutter_margin_width_pixels/2+left_margin_x_pixel/2), heading_top_margin_y_pixel),
            TOC_heading_text, fill=TOC_heading_text_color, font=TOC_heading_font, anchor="ms")
            blank_canvas_editable.text((round(0.25*paper_height/2-gutter_margin_width_pixels/2+left_margin_x_pixel/2), heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_pages_text, fill=TOC_pages_text_color, font=TOC_pages_font, anchor="ms")
            blank_canvas_editable.text((round(0.75*paper_height/2-gutter_margin_width_pixels/2+left_margin_x_pixel/2), heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_subject_text, fill=TOC_subject_text_color, font=TOC_pages_font, anchor="ms")

        #The user can choose to add a design to one or both pages by adding the JPEG image(s) to the
        #working folder, of which the file name starts with "left page" and/or "right page", so that the
        #code might distinguish it from the cover image (of which the file name begins with "cover").
        #The user would then pass in "custom_template_both_pages", "custom_template_left_page" or
        #"custom_template_right_page" when running the code.
        #The three "if" and "elif" statements below paste the design image onto both left and right pages
        #("if" statement), only on the left pages (first "elif" statement), or only on the right pages
        #("elif" statement).

        #If the user has provided a custom template page JPEG image, it will be
        #opened and an editable version will be instantiated. Two subsequent "if"
        #statements are required here, as there may be different images for the
        #left and right pages (if the designs are to be present on both pages,
        #accordingly with the "").
        if left_page_background_img != None:
            left_custom_template_image = Image.open(left_page_background_img)
        if right_page_background_img != None:
            right_custom_template_image = Image.open(right_page_background_img)

        if custom_template_left_page == True and custom_template_right_page == True:
            #If there are no more table of contents pages to be drawn ("TOC_pages_list == []") or there are
            #still some table of contents pages to be drawn ("TOC_pages_list != []"), but the first page in
            #the "TOC_pages_list" is an odd number, then the custom template page for the left side notebook
            #page (even numbered) can be drawn in the first "if" statement. There needs to be two sequential
            #"if" statements here, as there are custom templates on every page following the table of contents,
            #and the pages of the TOC alternate between even and odd pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                #The custom design is pasted onto the "blank_canvas" at the left corner (0,0 coordinates) or the
                #left hand page.
                blank_canvas.paste(left_custom_template_image, (0, 0))
            #If there are no more table of contents pages to be drawn ("TOC_pages_list == []") or there are
            #still some table of contents pages to be drawn ("TOC_pages_list != []"), but the first page in
            #the "TOC_pages_list" is an even number, then the custom pages for the right side notebook page
            #(odd numbered) can be drawn in the second "if" statement.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                #The custom design is pasted onto the left corner of the right hand page or the "blank_canvas",
                #which corresponds to the coordinates (paper_height/2+gutter_margin_width_pixels).
                blank_canvas.paste(right_custom_template_image, (int(paper_height/2), 0))
        elif custom_template_left_page == True:
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
               blank_canvas.paste(left_custom_template_image, (0, 0))

        elif custom_template_right_page == True:
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                blank_canvas.paste(right_custom_template_image, (int(paper_height/2), 0))


        #The three "if" and "elif" statements below draw horizontal lines for each scenario involving
        #ruled lines: for both even and odd pages ("if" statement), for left pages only (first "elif" statement),
        #or for right pages only (second "elif" statement).
        if ((college_ruled == True or wide_ruled == True or custom_ruled == True) and
        college_ruled_left == False and wide_ruled_left == False and custom_ruled_left == False and
        college_ruled_right == False  and wide_ruled_right == False and custom_ruled_right == False):
            #If there are no more table of contents pages to be drawn ("TOC_pages_list == []") or there are
            #still some table of contents pages to be drawn ("TOC_pages_list != []"), but the first page in
            #the "TOC_pages_list" is an odd number, then the lines for the left side notebook page (even numbered)
            #can be drawn in the first "if" statement. There needs to be two sequential "if" statements here, as
            #there are ruled lines on every page following the table of contents, and the pages of the TOC alternate
            #between even and odd pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(left_margin_x_pixel, y),
                    (paper_height/2-gutter_margin_width_pixels, y)], fill = line_color, width = line_width)
            #If there are no more table of contents pages to be drawn ("TOC_pages_list == []") or there are
            #still some table of contents pages to be drawn ("TOC_pages_list != []"), but the first page in
            #the "TOC_pages_list" is an even number, then the lines for the right side notebook page (odd numbered)
            #can be drawn in the second "if" statement.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(paper_height/2+gutter_margin_width_pixels, y),
                    (right_margin_x_pixel, y)], fill = line_color, width = line_width)
        elif (college_ruled == False and wide_ruled == False and custom_ruled == False and
        (college_ruled_left == True or wide_ruled_left == True or custom_ruled_left == True) and
        college_ruled_right == False and wide_ruled_right == False and custom_ruled_right == False):
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(left_margin_x_pixel, y),
                    (paper_height/2-gutter_margin_width_pixels, y)], fill = line_color, width = line_width)
        elif (college_ruled == False and wide_ruled == False and custom_ruled == False and
        college_ruled_left == False and wide_ruled_left == False and custom_ruled_left == False and
        (college_ruled_right == True or wide_ruled_right == True or custom_ruled_right == True)):
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(paper_height/2+gutter_margin_width_pixels, y),
                    (right_margin_x_pixel, y)], fill = line_color, width = line_width)

        #The three "if" and "elif" statements below draw graph paper lines for each scenario involving
        #graph paper: for both even and odd pages ("if" statement), for left pages only (first "elif" statement),
        #or for right pages only (second "elif" statement).
        if graph_paper == True and graph_paper_left == False and graph_paper_right == False:
            #Here the vertical lines are drawn at pixel increments equal to the rounded up number
            #of pixels taken up by one inch of squares (ex: an inch of squares at a "squares_per_inch=4"
            #contains four squares). The lines are only drawn on the left pages if there are no more table
            #of content pages to be drawn, or if the next TOC page is a right hand page (odd number).
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                starting_x = left_margin_x_pixel
                pixel_increment = round(1/squares_per_inch*300)
                line_x_coordinates = []
                #The list of "x" coordinates where to draw the vertical lines is stored in the
                #"line_x_coordinates" list.
                while starting_x <= paper_height/2-gutter_margin_width_pixels:
                    line_x_coordinates.append(starting_x)
                    starting_x += pixel_increment
                #Similarly to when drawing horizontal lines, bold lines are drawn whenever
                #the current line number is a multiple of "bold_line_every_n_squares" (if it isn't
                #equal to zero).
                #A half of the "graph_line_width" will be added to the left-hand page "x"
                #coordinates when drawing the vertical lines, to factor in the line thickness
                #and to respect the 0.25 inch left margin. The opposite is done for right-hand
                #pages, with "half_graph_line_width" being subtracted from the "x" coordinates.
                #Similarly, "half_graph_line_width" is subtracted from "line_y_coordinates_graph[0]"
                #and added to "line_x_coordinates[j]" to ensure that the vertical lines account for
                #the thickness of the vertical lines.
                half_graph_line_width = round(graph_line_width/2)
                for j in range(len(line_x_coordinates)): 
                    if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                        blank_canvas_editable.line([(line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                        (line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)], fill = graph_line_color,
                        width = round(line_boldness_factor*graph_line_width))
                    elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                        blank_canvas_editable.line([(line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                        (line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)], fill = graph_line_color,
                        width = graph_line_width)

                #Similar code than for ruled lines is applied for the horizontal lines of graph paper.
                for j in range(len(line_y_coordinates_graph)):
                    #If there are to be no bold lines every certain number of squares
                    #("bold_line_every_n_squares == 0") or if the current line isn't one
                    #of them (j%bold_line_every_n_squares != 0), then a horizontal line
                    #with a normal line width ("graph_line_width") is drawn.
                    if bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                        blank_canvas_editable.line([(line_x_coordinates[0], line_y_coordinates_graph[j]),
                        (line_x_coordinates[-1], line_y_coordinates_graph[j])],
                        fill = graph_line_color, width = graph_line_width)
                    #If the variable "bold_line_every_n_squares" isn't set to zero and if the
                    #current line number is a multiple of "bold_line_every_n_squares" (remainder
                    #of zero after a modulus operation), then a bold horizontal line is drawn,
                    #with a line width equal to "line_boldness_factor" times "graph_line_width"
                    #(rounded up).
                    elif bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                        blank_canvas_editable.line([(line_x_coordinates[0], line_y_coordinates_graph[j]),
                        (line_x_coordinates[-1], line_y_coordinates_graph[j])],
                        fill = graph_line_color, width = round(line_boldness_factor*graph_line_width))
            #Similar to above, but for right (odd number) pages. There needs to be two sequential
            #"if" statements here, as there is graph paper on every page following the table of
            #contents, and the pages of the TOC alternate between even and odd pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                starting_x = right_margin_x_pixel
                pixel_increment = round(1/squares_per_inch*300)
                line_x_coordinates = []
                while starting_x >= paper_height/2+gutter_margin_width_pixels:
                    line_x_coordinates.append(starting_x)
                    starting_x -= pixel_increment
                for j in range(len(line_x_coordinates)):
                    if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                        blank_canvas_editable.line([(line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                        (line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)], fill = graph_line_color,
                        width = round(line_boldness_factor*graph_line_width))
                    elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                        blank_canvas_editable.line([(line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                        (line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)],
                        fill = graph_line_color, width = graph_line_width)
                #This is very similar to the horizontal lines drawn for the ruled lines.
                for j in range(len(line_y_coordinates_graph)):
                    if bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                        blank_canvas_editable.line([(line_x_coordinates[0],
                        line_y_coordinates_graph[j]), (line_x_coordinates[-1],
                        line_y_coordinates_graph[j])], fill = graph_line_color,
                        width = graph_line_width)
                    elif bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                        blank_canvas_editable.line([(line_x_coordinates[0],
                        line_y_coordinates_graph[j]), (line_x_coordinates[-1], line_y_coordinates_graph[j])],
                        fill = graph_line_color, width = round(line_boldness_factor*graph_line_width))

        elif (graph_paper == False and graph_paper_left == True and graph_paper_right == False and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0))):
            starting_x = left_margin_x_pixel
            pixel_increment = round(1/squares_per_inch*300)
            line_x_coordinates = []
            while starting_x <= paper_height/2-gutter_margin_width_pixels:
                line_x_coordinates.append(starting_x)
                starting_x += pixel_increment
            half_graph_line_width = round(graph_line_width/2)
            for j in range(len(line_x_coordinates)): 
                if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                    blank_canvas_editable.line([(line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                    (line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)], fill = graph_line_color,
                    width = round(line_boldness_factor*graph_line_width))
                elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                    blank_canvas_editable.line([(line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                    (line_x_coordinates[j] + half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)], fill = graph_line_color,
                    width = graph_line_width)
            for j in range(len(line_y_coordinates_graph)):
                if bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                    blank_canvas_editable.line([(line_x_coordinates[0], line_y_coordinates_graph[j]),
                    (line_x_coordinates[-1], line_y_coordinates_graph[j])],
                    fill = graph_line_color, width = graph_line_width)
                elif bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                    blank_canvas_editable.line([(line_x_coordinates[0], line_y_coordinates_graph[j]),
                    (line_x_coordinates[-1], line_y_coordinates_graph[j])],
                    fill = graph_line_color, width = round(line_boldness_factor*graph_line_width))

        elif (graph_paper == False and graph_paper_left == False and graph_paper_right == True and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0))):
            starting_x = right_margin_x_pixel
            pixel_increment = round(1/squares_per_inch*300)
            line_x_coordinates = []
            while starting_x >= paper_height/2+gutter_margin_width_pixels:
                line_x_coordinates.append(starting_x)
                starting_x -= pixel_increment
            half_graph_line_width = round(graph_line_width/2)
            for j in range(len(line_x_coordinates)):
                if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                    blank_canvas_editable.line([(line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                    (line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)], fill = graph_line_color,
                    width = round(line_boldness_factor*graph_line_width))
                elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                    blank_canvas_editable.line([(line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[0] - half_graph_line_width),
                    (line_x_coordinates[j] - half_graph_line_width, line_y_coordinates_graph[-1] + half_graph_line_width)],
                    fill = graph_line_color, width = graph_line_width)
            for j in range(len(line_y_coordinates_graph)):
                if bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                    blank_canvas_editable.line([(line_x_coordinates[0],
                    line_y_coordinates_graph[j]), (line_x_coordinates[-1],
                    line_y_coordinates_graph[j])], fill = graph_line_color,
                    width = graph_line_width)
                elif bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                    blank_canvas_editable.line([(line_x_coordinates[0],
                    line_y_coordinates_graph[j]), (line_x_coordinates[-1], line_y_coordinates_graph[j])],
                    fill = graph_line_color, width = round(line_boldness_factor*graph_line_width))

        #The following "if" and "elif" statements deal with dot grids on both pages ("if" statement),
        #dot grids on left pages (first "elif" statement) or on right pages (second "elif" statement).
        if dot_grid == True and dot_grid_left == False and dot_grid_right == False:
            #If all the pages of the table of contents have aldready been included ("TOC_pages_list == []"),
            #or if the next TOC page is a right hand page (odd numbered, "TOC_pages_list[0]%2 != 0"),
            #then the dots are drawn on the left (even numbered) pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                #Using the ImageDraw module, some ellipses are drawn, with a square dimensioned
                #bounding box, giving the corresponding circles with a diameter of "dot_diameter_pixels".
                #The dots are evenly spaced on the horizontal and vertical axes by a distance of
                #"inches_between_dots*300" pixels, as there are 2550 pixels in 8.5 inches at an image
                #resolution of 300 ppi.
                for j in range(len(dot_y_coordinates)):
                    #Here half of the diameter of the dots ("round(dot_diameter_pixels/2)")
                    #is added to "left_margin_x_pixel" to ensure that the left edge of the 
                    #leftmost dots is within the border (otherwise half of the dot would
                    #be outside of the border horizontally)
                    starting_x = left_margin_x_pixel + round(dot_diameter_pixels/2)
                    while starting_x <= paper_height/2-gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x += round(inches_between_dots*300)
            #Similar to the lined and graph pages on even and odd pages above, a second "if"
            #statement deals with drawing dots on the odd (right) pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                for j in range(len(dot_y_coordinates)):
                    #Here half of the diameter of the dots ("round(dot_diameter_pixels/2)")
                    #is subtracted from "right_margin_x_pixel" to ensure that the right edge of the 
                    #rightmost dots is within the border (otherwise half of the dot would
                    #be outside of the border horizontally)
                    starting_x = right_margin_x_pixel - round(dot_diameter_pixels/2)
                    while starting_x >= paper_height/2+gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x -= round(inches_between_dots*300)

        elif (dot_grid == False and dot_grid_left == True and dot_grid_right == False and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0))):
            for j in range(len(dot_y_coordinates)):
                starting_x = left_margin_x_pixel + round(dot_diameter_pixels/2)
                while starting_x <= paper_height/2-gutter_margin_width_pixels:
                    blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                    dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                    (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                    fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                    starting_x += round(inches_between_dots*300)

        elif (dot_grid == False and dot_grid_left == False and dot_grid_right == True and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0))):
            for j in range(len(dot_y_coordinates)):
                starting_x = right_margin_x_pixel - round(dot_diameter_pixels/2)
                while starting_x >= paper_height/2+gutter_margin_width_pixels:
                    blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                    dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                    (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                    fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                    starting_x -= round(inches_between_dots*300)


        #The following "if" and "elif" statements deal with ScriptReader custom dot grids on both pages
        #("if" statement), only on left pages (first "elif" statement) or only on right pages (second "elif" statement).
        #ScriptReader is another github repo that enables the user to train a OCR convoluted neural network model on
        #their handwriting, using customized dot grid sheets that have alternating dot grid horizontal lines with
        #empty lines, to accomodate for the ascenders and descenders when handwriting.
        if scriptreader == True and scriptreader_left == False and scriptreader_right == False:
            #If all the pages of the table of contents have aldready been included ("TOC_pages_list == []"),
            #or if the next TOC page is a right hand page (odd numbered, "TOC_pages_list[0]%2 != 0"),
            #then the dots are drawn on the left (even numbered) pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                #Using the ImageDraw module, some ellipses are drawn, with a square dimensioned
                #bounding box, giving the corresponding circles with a diameter of "dot_diameter_pixels".
                #The dots are evenly spaced on the horizontal and vertical axes by a distance of
                #"inches_between_dots*300" pixels, as there are 2550 pixels in 8.5 inches at an image
                #resolution of 300 ppi.
                for j in range(len(text_line_numbers)):
                    #Here half of the diameter of the dots ("round(dot_diameter_pixels/2)")
                    #is added to "left_margin_x_pixel" to ensure that the left edge of the 
                    #leftmost dots is within the border (otherwise half of the dot would
                    #be outside of the border horizontally)
                    starting_x = left_margin_x_pixel + round(dot_diameter_pixels/2)
                    while starting_x <= paper_height/2-gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[text_line_numbers[j]] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[text_line_numbers[j]] +
                        int(dot_diameter_pixels/2))], fill = dot_fill_color, outline = dot_outline_color,
                        width = dot_line_width)
                        starting_x += round(inches_between_dots*300)
                        
                gutter_dot_x = starting_x - round(inches_between_dots*300)
                #Black squares are drawn in the top corners of the page, for the segmentation
                #code to be able to align the pages accurately. Of note, "gutter_dot_x" is used
                #as the "x1" coordinate for the squares nearest to the gutter margin, to account
                #for the fact that the dot nearest to the gutter margin may not be exactly on
                #the gutter margin.
                blank_canvas_editable.rectangle([(left_margin_x_pixel, pixels_above_black_squares + top_y_shift),
                (left_margin_x_pixel + 50, pixels_above_black_squares + 50 + top_y_shift)], fill="Black")

                blank_canvas_editable.rectangle([(gutter_dot_x - 50,
                pixels_above_black_squares + top_y_shift), (gutter_dot_x,
                pixels_above_black_squares + 50 + top_y_shift)],
                fill="Black")
            #Similar to the lined and graph pages on even and odd pages above, a second "if"
            #statement deals with drawing dots on the odd (right) pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):

                for j in range(len(text_line_numbers)):
                    #Here half of the diameter of the dots ("round(dot_diameter_pixels/2)")
                    #is subtracted from "right_margin_x_pixel" to ensure that the right edge of the 
                    #rightmost dots is within the border (otherwise half of the dot would
                    #be outside of the border horizontally)
                    starting_x = right_margin_x_pixel - round(dot_diameter_pixels/2)
                    while starting_x >= paper_height/2+gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[text_line_numbers[j]] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[text_line_numbers[j]] +
                        int(dot_diameter_pixels/2))], fill = dot_fill_color, outline = dot_outline_color,
                        width = dot_line_width)
                        starting_x -= round(inches_between_dots*300)
                gutter_dot_x = starting_x + round(inches_between_dots*300)

                blank_canvas_editable.rectangle([(right_margin_x_pixel - 50, pixels_above_black_squares + top_y_shift),
                (right_margin_x_pixel, pixels_above_black_squares + 50 + top_y_shift)], fill="Black")

                blank_canvas_editable.rectangle([(gutter_dot_x,
                pixels_above_black_squares + top_y_shift), 
                (gutter_dot_x + 50, pixels_above_black_squares + 50 + top_y_shift)],
                fill="Black")

        elif (scriptreader == False and scriptreader_left == True and scriptreader_right == False and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0))):

            for j in range(len(text_line_numbers)):
                starting_x = left_margin_x_pixel + round(dot_diameter_pixels/2)
                while starting_x <= paper_height/2-gutter_margin_width_pixels:
                    blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                    dot_y_coordinates[text_line_numbers[j]] - int(dot_diameter_pixels/2)),
                    (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[text_line_numbers[j]] +
                    int(dot_diameter_pixels/2))], fill = dot_fill_color, outline = dot_outline_color,
                    width = dot_line_width)
                    starting_x += round(inches_between_dots*300)

            gutter_dot_x = starting_x - round(inches_between_dots*300)

            blank_canvas_editable.rectangle([(left_margin_x_pixel, pixels_above_black_squares + top_y_shift),
            (left_margin_x_pixel + 50, pixels_above_black_squares + 50 + top_y_shift)], fill="Black")

            blank_canvas_editable.rectangle([(gutter_dot_x - 50,
            pixels_above_black_squares + top_y_shift), 
            (gutter_dot_x, pixels_above_black_squares + 50 + top_y_shift)],
            fill="Black")

        elif (scriptreader == False and scriptreader_left == False and scriptreader_right == True and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0))):

            for j in range(len(text_line_numbers)):
                starting_x = right_margin_x_pixel - round(dot_diameter_pixels/2)
                while starting_x >= paper_height/2+gutter_margin_width_pixels:
                    blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                    dot_y_coordinates[text_line_numbers[j]] - int(dot_diameter_pixels/2)),
                    (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[text_line_numbers[j]] +
                    int(dot_diameter_pixels/2))], fill = dot_fill_color, outline = dot_outline_color,
                    width = dot_line_width)
                    starting_x -= round(inches_between_dots*300)
            gutter_dot_x = starting_x + round(inches_between_dots*300)

            blank_canvas_editable.rectangle([(right_margin_x_pixel - 50, pixels_above_black_squares + top_y_shift),
            (right_margin_x_pixel, pixels_above_black_squares + 50 + top_y_shift)], fill="Black")

            blank_canvas_editable.rectangle([(gutter_dot_x,
            pixels_above_black_squares + top_y_shift), 
            (gutter_dot_x + 50, pixels_above_black_squares + 50 + top_y_shift)],
            fill="Black")


        #The following "if" and "elif" statements deal with notebook page headers on both pages ("if" statement),
        #only on left (even) pages (first "elif" statement) or on right (odd) pages (second "elif" statement).
        #The variables "heading_text_left" and "heading_text_right" designate the actual text strings that will
        #be writton on the left and right pages, respectively. If headings are to be included on both pages,
        #then the values of "heading_text_left" and "heading_text_right" will be the same.
        if heading_text_left != None and heading_text_right != None:
            #If all of the table of contents pages already have been included, or if the next
            #TOC page is odd numbered, then the heading is written on the left (even numbered) page.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                #If the headings are to be written in the outer page corners, "heading_corner == True",
                #then the anchoring "x" pixel is set as "left_margin_x_pixel", with left baseline ("ls")
                #text anchoring.
                if heading_corner == True:
                    blank_canvas_editable.text((left_margin_x_pixel, heading_top_margin_y_pixel),
                    heading_text_left, fill=heading_text_color, font=heading_font, anchor="ls")
                #Otherwise, the headings on left pages are centered, by adding the left margin "x"
                #pixels ("left_margin_x_pixel") to the center of the available space on the left page,
                #excluding the margins. The available space on the page is calculated by taking
                #the cental "x" coordinate (paper_height/2) and subtracting the pixels for the gutter martin
                #and those for the right margin (which is equivalent to "left_margin_x_pixel").
                else:
                    blank_canvas_editable.text((round(left_margin_x_pixel + (paper_height/2-gutter_margin_width_pixels-
                    left_margin_x_pixel)/2), heading_top_margin_y_pixel),
                    heading_text_left, fill=heading_text_color, font=heading_font, anchor="ms")
            #If all of the table of contents pages already have been included, or if the next
            #TOC page is even numbered, then the heading is written on the right (odd numbered) page.
            #Again, there needs to be two sequential "if" statements here, as there are headings on
            #every page following the table of contents, and the pages of the TOC alternate between
            #even and odd pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                if heading_corner == True:
                    blank_canvas_editable.text((right_margin_x_pixel, heading_top_margin_y_pixel),
                    heading_text_right, fill=heading_text_color, font=heading_font, anchor="rs")
                #The centering point for the headings on the right-hand pages is determined by taking
                #the central point on the sheet (paper_height/2) and adding the pixels for the gutter margin,
                #and then the center of the available space on the right page. The available space on
                #the page is calculated by taking the cental "x" coordinate (paper_height/2) and subtracting
                #the pixels for the gutter martin and those for the left margin ("left_margin_x_pixel").
                else:
                    blank_canvas_editable.text((round(paper_height/2 + gutter_margin_width_pixels +
                    (paper_height/2-gutter_margin_width_pixels-left_margin_x_pixel)/2), heading_top_margin_y_pixel),
                    heading_text_right, fill=heading_text_color, font=heading_font, anchor="ms")

        #Similar to above, except that the headings are only written on the left hand pages, provided
        #that all of the TOC pages have been included, or that the next TOC page is odd numbered.
        elif (heading_text_left != None and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0))):
            if heading_corner == True:
                blank_canvas_editable.text((left_margin_x_pixel, heading_top_margin_y_pixel),
                heading_text_left, fill=heading_text_color, font=heading_font, anchor="ls")
            else:
                blank_canvas_editable.text((round(left_margin_x_pixel + (paper_height/2-gutter_margin_width_pixels-
                left_margin_x_pixel)/2), heading_top_margin_y_pixel),
                heading_text_left, fill=heading_text_color, font=heading_font, anchor="ms")

        #Similar to above, except that the headings are only written on the right hand pages, provided
        #that all of the TOC pages have been included, or that the next TOC page is even numbered.
        elif (heading_text_right != None and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0))):
            if heading_corner == True:
                blank_canvas_editable.text((right_margin_x_pixel, heading_top_margin_y_pixel),
                heading_text_right, fill=heading_text_color, font=heading_font, anchor="rs")
            else:
                blank_canvas_editable.text((round(paper_height/2 + gutter_margin_width_pixels +
                (paper_height/2-gutter_margin_width_pixels-left_margin_x_pixel)/2), heading_top_margin_y_pixel),
                heading_text_right, fill=heading_text_color, font=heading_font, anchor="ms")

        #The following "if" and "elif" statements deal with page numbering either on both pages
        #("if" statement), on left pages only (first "elif" statement) or only on right pages
        #(second "elif" statement). The user could also choose not to write page numbers, by not
        #passing in any of the following arguments: "page_numbers", "page_numbers_left" or
        #"page_numbers_right". The page numbers are written with left or right middle text
        #anchoring ("lm" or "rm", respectively), in order to simplify the automatic vertical
        #centering of the page numbers in the available space in-between the last horizontal
        #line and the bottom of the page.
        if page_numbers != None and page_numbers_left == None and page_numbers_right == None and scriptreader_acetate == False:
            #If the list of page numbers to be written isn't empty, meaning that either all page
            #numbers have already been written down or the user didn't choose to write page
            #numbers ("page_numbers_list != []") and if the next descending page number to be
            #written down is odd numbered ("page_numbers_list[-1]%2 != 0"), then it means that
            #the next ascending page number to be written is even numbered (on the left page).
            if page_numbers_list != [] and page_numbers_list[-1]%2 != 0:
                #If all of the table of contents pages already have been included, or if the next
                #TOC page is odd numbered, then the page number is written on the left (even numbered) page.
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                    blank_canvas_editable.text((left_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[0]), fill=page_numbers_text_color, font=page_numbers_font, anchor="lm")
                    #The first element (ascending page number) of the "page_numbers_list" is removed,
                    #as it was just written down on the left side of the "blank_canvas_editable".
                    page_numbers_list.pop(0)
                #If all of the table of contents pages already have been included, or if the next
                #TOC page is even numbered, then the page number is written on the right (odd numbered) page.
                #Again, there needs to be two sequential "if" statements here, as there are page numbers on
                #every page following the table of contents, and the pages of the TOC alternate between
                #even and odd pages.
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                    blank_canvas_editable.text((right_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[-1]), fill=page_numbers_text_color, font=page_numbers_font, anchor="rm")
                    #The last element (descending page number) of the "page_numbers_list" is removed,
                    #as it was just written down on the left side of the "blank_canvas_editable".
                    page_numbers_list.pop(-1)
            #The reverse logic is applied if the next descending page is even numbered.
            elif page_numbers_list != [] and page_numbers_list[-1]%2 == 0:
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                    blank_canvas_editable.text((left_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[-1]), fill=page_numbers_text_color, font=page_numbers_font, anchor="lm")
                    page_numbers_list.pop(-1)
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                    blank_canvas_editable.text((right_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[0]), fill=page_numbers_text_color, font=page_numbers_font, anchor="rm")
                    page_numbers_list.pop(0)
        #A similar logic to the above (page_numbers != None) is applied here, except that whenever
        #the right page number is encountered, it isn't written on the page and is popped out from
        #the "page_numbers_list".
        elif page_numbers_left != None and page_numbers == None and page_numbers_right == None and scriptreader_acetate == False:
            if page_numbers_list != [] and page_numbers_list[-1]%2 != 0:
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                    blank_canvas_editable.text((left_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[0]), fill=page_numbers_text_color, font=page_numbers_font, anchor="lm")
                    page_numbers_list.pop(0)
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                    page_numbers_list.pop(-1)
            elif page_numbers_list != [] and page_numbers_list[-1]%2 == 0:
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                    blank_canvas_editable.text((left_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[-1]), fill=page_numbers_text_color, font=page_numbers_font, anchor="lm")
                    page_numbers_list.pop(-1)
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                    page_numbers_list.pop(0)
        #A similar logic to the above (page_numbers != None) is applied here, except that whenever
        #the left page number is encountered, it isn't written on the page and is popped out from
        #the "page_numbers_list".
        elif page_numbers_right != None and page_numbers == None and page_numbers_left == None and scriptreader_acetate == False:
            if page_numbers_list != [] and page_numbers_list[-1]%2 != 0:
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                    page_numbers_list.pop(0)
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                    blank_canvas_editable.text((right_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[-1]), fill=page_numbers_text_color, font=page_numbers_font, anchor="rm")
                    page_numbers_list.pop(-1)
            elif page_numbers_list != [] and page_numbers_list[-1]%2 == 0:
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                    page_numbers_list.pop(-1)
                if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                    blank_canvas_editable.text((right_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
                    str(page_numbers_list[0]), fill=page_numbers_text_color, font=page_numbers_font, anchor="rm")
                    page_numbers_list.pop(0)
        elif scriptreader_acetate == True and page_numbers_list != [] and TOC_pages_list == []:
            blank_canvas_editable.text((right_margin_x_pixel, page_numbers_bottom_margin_y_pixel),
            str(page_numbers_list[0]), fill=page_numbers_text_color, font=page_numbers_font, anchor="rm")
            page_numbers_list.pop(0)

        #If the list of table of contents pages ("TOC_pages_list")
        #isn't empty, the first page (that was just included in the
        #current "blank_canvas_editable") is removed from the list.
        if TOC_pages_list != [] and scriptreader_acetate == False:
            TOC_pages_list.pop(0)
        if scriptreader_acetate == True:
            if TOC_pages_list != []:
                #Both the odd and even-numbered page needs to be removed
                #from "TOC_pages_list"
                try:
                    TOC_pages_list.pop(0)
                    TOC_pages_list.pop(0)
                #If the number of pages is odd-numbered, the code won't be
                #able to perform two successive pops at the very last page.
                except:
                    TOC_pages_list.pop(0)
            #The counter "current_acetate_page_number" keeps track
            #of the acetate sheet number (two pages per acetate sheet),
            #in order to only draw a vertical line on one side of the acetate
            #sheet (as an indicator of where to cut the acetate in half).
            #Otherwise, if the lines were drawn on both sides of the
            #acetate, it would end up looking messy, as they would likely
            #not line up.
            if current_acetate_page_number%2 == 0:
                blank_canvas_editable.line([(paper_height/2, 0), 
                (paper_height/2, paper_width)], fill="Gainsboro", width=5)
            current_acetate_page_number += 1
            #The page will be mirrored, in order to print on the back side of that
            #you will be writing on. This way, the toner will not be scratched when
            #writing on the page.
            blank_canvas = ImageOps.mirror(blank_canvas)
        if no_merging == True:
            blank_canvas.save(os.path.join(cwd, "Notebooks", str(date.today()) +
            "-" + title, str(date.today()) + "-" + title + " (page " +
            str(current_page) + ").pdf"), quality=100, resolution=300)
        elif no_merging == False and current_page == 1:
            blank_canvas.save(os.path.join(cwd, "Notebooks", str(date.today()) +
            "-" + title, str(date.today()) + "-" + title + " (notebook pages).pdf"),
            quality=100, resolution=300)
        elif no_merging == False and current_page > 1:
            blank_canvas.save(os.path.join(cwd, "Notebooks", str(date.today()) +
            "-" + title, str(date.today()) + "-" + title + " (notebook pages).pdf"),
            append=True, quality=100, resolution=300)
        current_page += 1

    no_need_to_add_cover_box_color = False
    no_need_to_add_cover_text_color = False
    command_string = ""
    for i in range(1, len(sys.argv)):
        command_string += '"' + sys.argv[i] + '" '
        if sys.argv[i][:16].lower() == "cover_box_color:" or grayscale == True:
            no_need_to_add_cover_box_color = True
        if sys.argv[i][:17].lower() == "cover_text_color:" or grayscale == True:
            no_need_to_add_cover_text_color = True
    if no_need_to_add_cover_box_color == False:
        command_string += ' "cover_box_color:' + cover_box_color + '"'
    if no_need_to_add_cover_text_color == False:
        command_string += ' "cover_text_color:' + cover_text_color + '"'

    with open(os.path.join(cwd, "Notebooks", str(date.today()) + "-" + title,
    "Parameters Passed In.txt"), "w", encoding = "utf-8") as text_file:
        text_file.write('py printanotebook.py ' + command_string)

    print("\nYour notebook has been created successfully!")
    print("Here are the colors used for the boxes and text:")
    print("Cover boxes color: " + cover_box_color)
    print("Cover text color: " + cover_text_color)
    print("\nAnd here are the font sizes (in pixels of font height) used for the cover page PDF document:")
    print("Cover title font size: ", cover_title_font_size)
    if author != None:
        print("Cover author font size: ", cover_author_font_size)
    if perforated_cover == False:
        print("Spine text font size: ", spine_font_size)

#If the user hasn't provided a title, author and valid file name,
#the following error message will be displayed on screen.
else:
    print("\nPlease provide the title and number of pages of the notebook as additional " +
    "arguments (with a space in-between each argument) when running the code. Also, " +
    "if you will be perfect binding your notebook, add the number of pages and " + 
    "thickness of a ream of 500 pages (in inches) when running " +
    "the code, so that the spine dimensions may be determined accordingly.\n")

    print('For example: python3 printanotebook.py "title:Skeches and Poetry" '
    + '"author:Your Name Here" "number_of_pages:192" "inches_per_ream_500_pages:2"')
