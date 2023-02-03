import glob
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re
import sys


cwd = os.getcwd()

#The "problem" variable is initialized to "False"
#and will be set to "True" should the code encounter
#any problems, in order to give the user relevant error
#messages along the  way.
problem = False

title = None
author = None

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
#Should the cover title need to be split,
#the default line spacing in-between title lines
#is initialized at 5 pixels, and may be altered
#by the user.
cover_title_line_spacing = 5
cover_author_line_spacing = 4
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
pixels_from_bottom_cover_spine = 3
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
pixels_from_top_cover_title_box = 10
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
#text of these headings, as well as that of the "Content" heading.
TOC_subject_font_size = 60
TOC_subject_text = "Subject"
TOC_subject_text_color = "LightSlateGrey"
TOC_pages_font_size = 60
TOC_pages_text = "Pages"
TOC_pages_text_color = "LightSlateGrey"
TOC_line_spacing = None
TOC_heading_font_size = 75
TOC_heading_text = "Content"
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
heading_top_margin_y_pixel = 0.60*2550/8.5
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
top_margin_y_pixel = 0.95*2550/8.5
#Similarly, the "bottom_margin_y_pixel" maps to
#the "y" pixel where the lines and dots end.
bottom_margin_y_pixel = 2550-(0.60*2550/8.5)
#The variables "left_margin_x_pixel"  and
#"right_margin_x_pixel" map to the "x"
#pixels where the lines and dots start and
#stop being drawn on the pages, respectively.
left_margin_x_pixel = 0.25*3300/8.5
right_margin_x_pixel = 3300-(0.25*3300/8.5)
#The "gutter_margin_width_pixels" designates the
#width (in pixels) of the gutter margins of the
#notebook. They are set to the pixel equivalent
#of an eighth of an inch, so they won't be noticeable
#when opening a bound book.
gutter_margin_width_pixels = 0.125*3300/8.5
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
#The "dot_y_shift_down" variable stores the
#amount of pixels that will be added to the
#starting "y" coordinate.  The value of
#"dot_y_shift_down" is only different than
#zero if there are no ruled lines in the notebook,
#so that the dots may line up with TOC ruled lines.
dot_y_shift_down = 0
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

#The left margin can be determined by subtracting the space
#in-between the margins (4.75 inches) from the right edge
#pixel count: (4200 - 4.75*4200/14) = 2775 px
left_margin_cover_textbox = 2775

#The right margin can simply be calculated given the pixel
#width of the canvas: 4220-(0.75*4200/14) = 3995 px
right_margin_cover_textbox = 3995

#The top margin of the text box on the cover page can
#be determined by adding a 25% of the vertical
#pixels to the starting y corrdinate of 0. (0+(2550/4)).
top_margin_cover_textbox = 640

if len(sys.argv) > 1:
    #The "try/except" statement will
    #intercept any "ValueErrors" and
    #ask the users to correctly enter
    #the desired values for the variables
    #directly after the colon separating
    #the variable name from the value.
    try:
        for i in range(1, len(sys.argv)):
            if len(sys.argv[i]) > 1 and sys.argv[i][:6] == "title:":
                title = sys.argv[i][6:]
            elif len(sys.argv[i]) > 1 and sys.argv[i][:7] == "author:":
                if len(sys.argv[i][7:]) > 3 and sys.argv[i][7:10].lower() == "by ":
                    author = sys.argv[i][10:]
                    author_names = re.split(r"( )", author)
                    for j in range(len(author_names)):
                        if author_names[j].lower() != "by":
                            author_names[j] == author_names[j].capitalize()
                    author = "".join(author_names).strip()
                elif len(sys.argv[i][7:]) > 3 and sys.argv[i][7:10] != "by ":
                    author = sys.argv[i][7:].strip()
                    author_names = re.split(r"( )", author)
                    for j in range(len(author_names)):
                        author_names[j] == author_names[j].capitalize()
                    author = "".join(author_names).strip()
                else:
                    author = sys.argv[i][7:].strip()
            elif sys.argv[i].lower()[:16] == "number_of_pages:":
                number_of_pages = int(sys.argv[i].lower()[16:].strip())
            elif sys.argv[i].lower()[:26] == "inches_per_ream_500_pages:":
                make_cover = True
                inches_per_ream_500_pages = float(sys.argv[i][26:].strip())
            elif sys.argv[i].lower()[:22] == "cm_per_ream_500_pages:":
                make_cover = True
                cm_per_ream_500_pages = float(sys.argv[i][22:].strip())
                inches_per_ream_500_pages = cm_per_ream_500_pages/2.54
            elif sys.argv[i].strip().lower() == "grayscale" or sys.argv[i].strip().lower() == "greyscale":
                grayscale = True
            elif sys.argv[i].lower()[:16] == "cover_box_color:":
                cover_box_color = sys.argv[i].lower()[16:].strip()
            elif sys.argv[i].lower()[:17] == "cover_text_color:":
                cover_text_color =  sys.argv[i].lower()[17:].strip()
            elif sys.argv[i].lower()[:22] == "cover_title_font_size:":
                cover_title_font_size = round(sys.argv[i][22:].strip())
            elif sys.argv[i].lower()[:23] == "cover_author_font_size:":
                cover_author_font_size = round(sys.argv[i][23:].strip())
            elif sys.argv[i].lower()[:16] == "spine_font_size:":
                spine_font_size = round(sys.argv[i][16:].strip())
            elif sys.argv[i].lower()[:33] == "cover_spacing_title_height_ratio:":
                cover_spacing_title_height_ratio = float(sys.argv[i][33:].strip())
            elif sys.argv[i].strip().lower()[:17] == "cover_trim_width:":
                cover_trim_width = float(sys.argv[i][17:].strip())
            elif sys.argv[i].strip().lower()[:20] == "cover_trim_width_cm:":
                cover_trim_width = float(sys.argv[i][20:].strip())/2.54
            elif sys.argv[i].strip().lower()[:13] == "no_cover_line":
                cover_line = False
            elif sys.argv[i].strip().lower()[:19] == "cover_extra_inches:":
                inches = float(sys.argv[i].strip()[19:])
                cover_extra_pixels = round(inches*4200/14)
            elif sys.argv[i].strip().lower()[:15] == "cover_extra_cm:":
                cm = float(sys.argv[i].strip()[15:])
                cover_extra_pixels = round(cm/2.54*4200/14)
            elif sys.argv[i].strip().lower()[:31] == "pixels_from_bottom_cover_spine:":
                pixels_from_bottom_cover_spine = int(sys.argv[i].strip()[31:])
            elif sys.argv[i].strip().lower()[:29] == "pixels_from_left_cover_spine:":
                pixels_from_left_cover_spine = int(sys.argv[i].strip()[29:])
            elif sys.argv[i].strip().lower()[:32] == "pixels_from_top_cover_title_box:":
                pixels_from_top_cover_title_box = int(sys.argv[i].strip()[32:])
            elif sys.argv[i].strip().lower()[:33] == "pixels_from_left_cover_title_box:":
                pixels_from_left_cover_title_box = int(sys.argv[i].strip()[33:])
            elif sys.argv[i].strip().lower()[:11] == "spine_text:":
                spine_text = sys.argv[i].strip()[11:]
            #The elif statements below are specific to PrintANotebook
            elif sys.argv[i].lower()[:12] == "left_margin:":
                inches = float(sys.argv[i][12:].strip())
                left_margin_x_pixel = round(inches*3300/8.5)
            elif sys.argv[i].lower()[:13] == "right_margin:":
                inches = float(sys.argv[i][13:].strip())
                right_margin_x_pixel = 3300-round(inches*3300/8.5)
            elif sys.argv[i].lower()[:11] == "top_margin:":
                inches = float(sys.argv[i][11:].strip())
                top_margin_y_pixel = round(inches*2550/8.5)
            elif sys.argv[i].lower()[:14] == "bottom_margin:":
                inches = float(sys.argv[i][14:].strip())
                bottom_margin_y_pixel = 2550-round(inches*2550/8.5)
            elif sys.argv[i].lower()[:19] == "heading_top_margin:":
                inches = float(sys.argv[i][19:].strip())
                heading_top_margin_y_pixel = round(inches*2550/8.5)
            elif sys.argv[i].lower()[:27] == "page_numbers_bottom_margin:":
                inches = float(sys.argv[i][27:].strip())
                page_numbers_bottom_margin_y_pixel = 2550-round(inches*2550/8.5)
            elif sys.argv[i].strip().lower()[:18] == "heading_text_left:":
                heading_text_left = sys.argv[i][18:]
            elif sys.argv[i].strip().lower()[:19] == "heading_text_right:":
                heading_text_right = sys.argv[i][19:]
            elif sys.argv[i].strip().lower()[:13] == "heading_text:":
                heading_text_left = sys.argv[i][13:]
                heading_text_right = sys.argv[i][13:]
            elif sys.argv[i].lower()[:19] == "heading_text_color:":
                heading_text_color =  sys.argv[i].lower()[19:].strip()
                if heading_text_color[0] == "(":
                    heading_text_color = "rgb" + heading_text_color
            elif sys.argv[i].lower()[:14] == "heading_corner":
                heading_corner = True
            elif sys.argv[i].strip().lower()[:22] == "toc_heading_font_size:":
                TOC_heading_font_size = int(sys.argv[i].strip()[22:])
            elif sys.argv[i].strip().lower()[:17] == "toc_heading_text:":
                TOC_heading_text = sys.argv[i][17:]
            elif sys.argv[i].lower()[:23] == "toc_heading_text_color:":
                TOC_heading_text_color =  sys.argv[i].lower()[23:].strip()
                if TOC_heading_text_color[0] == "(":
                    TOC_heading_text_color = "rgb" + TOC_heading_text_color
            elif sys.argv[i].strip().lower()[:18] == "heading_font_size:":
                heading_font_size = int(sys.argv[i].strip()[18:])
            elif sys.argv[i].strip().lower()[:18] == "heading_left_pages":
                heading_left_pages = True
            elif sys.argv[i].strip().lower()[:19] == "heading_right_pages":
                heading_right_pages = True
            elif sys.argv[i].lower()[:24] == "page_numbers_text_color:":
                page_numbers_text_color =  sys.argv[i].lower()[24:].strip()
                if page_numbers_text_color[0] == "(":
                    page_numbers_text_color = "rgb" + page_numbers_text_color
            elif sys.argv[i].strip().lower()[:23] == "page_numbers_font_size:":
                page_numbers_font_size = int(sys.argv[i].strip()[23:])
            elif sys.argv[i].strip().lower()[:17] == "page_numbers_left":
                page_numbers_left = True
            elif sys.argv[i].strip().lower()[:18] == "page_numbers_right":
                page_numbers_right = True
            elif sys.argv[i].strip().lower()[:12] == "page_numbers":
                page_numbers = True
            elif sys.argv[i].strip().lower()[:18] == "college_ruled_left":
                college_ruled_left = True
            elif sys.argv[i].strip().lower()[:19] == "college_ruled_right":
                college_ruled_right = True
            elif sys.argv[i].strip().lower()[:13] == "college_ruled":
                college_ruled = True
            elif sys.argv[i].strip().lower()[:15] == "wide_ruled_left":
                wide_ruled_left = True
            elif sys.argv[i].strip().lower()[:16] == "wide_ruled_right":
                wide_ruled_right = True
            elif sys.argv[i].strip().lower()[:10] == "wide_ruled":
                wide_ruled = True
            elif sys.argv[i].strip().lower()[:18] == "custom_ruled_left:":
                custom_line_distance_inches = float(sys.argv[i].strip()[18:])
                custom_ruled_left = True
            elif sys.argv[i].strip().lower()[:19] == "custom_ruled_right:":
                custom_line_distance_inches = float(sys.argv[i].strip()[19:])
                custom_ruled_right = True
            elif sys.argv[i].strip().lower()[:13] == "custom_ruled:":
                custom_line_distance_inches = float(sys.argv[i].strip()[13:])
                custom_ruled = True
            elif sys.argv[i].strip().lower()[:17] == "graph_paper_left:":
                graph_paper_left = True
                arguments = sys.argv[i].strip()[17:].split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            squares_per_inch = int(arguments[j])
                        elif j == 1:
                            bold_line_every_n_squares = int(arguments[j])
                        elif j == 2:
                            line_boldness_factor = float(arguments[j])
            elif sys.argv[i].strip().lower()[:18] == "graph_paper_right:":
                graph_paper_right = True
                arguments = sys.argv[i].strip()[18:].split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            squares_per_inch = int(arguments[j])
                        elif j == 1:
                            bold_line_every_n_squares = int(arguments[j])
                        elif j == 2:
                            line_boldness_factor = float(arguments[j])
            elif sys.argv[i].strip().lower()[:12] == "graph_paper:":
                graph_paper = True
                arguments = sys.argv[i].strip()[12:].split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            squares_per_inch = int(arguments[j])
                        elif j == 1:
                            bold_line_every_n_squares = int(arguments[j])
                        elif j == 2:
                            line_boldness_factor = float(arguments[j])

            elif (sys.argv[i].strip().lower()[:14] == "dot_grid_left:" or
            sys.argv[i].strip().lower()[:13] == "dot_grid_left"):
                dot_grid_left = True
                arguments = sys.argv[i].strip()[14:].split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
            elif (sys.argv[i].strip().lower()[:15] == "dot_grid_right:" or
            sys.argv[i].strip().lower()[:14] == "dot_grid_right"):
                dot_grid_right = True
                arguments = sys.argv[i].strip()[15:].split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
            elif (sys.argv[i].strip().lower()[:9] == "dot_grid:" or
            sys.argv[i].strip().lower()[:8] == "dot_grid"):
                dot_grid = True
                arguments = sys.argv[i].strip()[9:].split(":")
                if arguments != [""]:
                    for j in range(len(arguments)):
                        if j == 0:
                            inches_between_dots = float(arguments[j])
                        elif j == 1:
                            dot_diameter_pixels = int(arguments[j])
                        elif j == 2:
                            dot_line_width = int(arguments[j])
            elif sys.argv[i].strip().lower()[:25] == "custom_template_left_page":
                custom_template_left_page = True
            elif sys.argv[i].strip().lower()[:26] == "custom_template_right_page":
                custom_template_right_page = True
            elif sys.argv[i].strip().lower()[:26] == "custom_template_both_pages":
                custom_template_left_page = True
                custom_template_right_page = True
            elif sys.argv[i].strip().lower()[:15] == "dot_fill_color:":
                dot_fill_color = sys.argv[i].strip().lower()[15:]
                if dot_fill_color[0] == "(":
                    dot_fill_color = "rgb" + dot_fill_color
            elif sys.argv[i].strip().lower()[:18] == "dot_outline_color:":
                dot_outline_color = sys.argv[i].strip().lower()[18:]
                if dot_outline_color[0] == "(":
                    dot_outline_color = "rgb" + dot_outline_color
            elif sys.argv[i].strip().lower()[:17] == "graph_line_color:":
                graph_line_color = sys.argv[i].strip().lower()[17:]
                if graph_line_color[0] == "(":
                    graph_line_color = "rgb" + graph_line_color
            elif sys.argv[i].strip().lower()[:17] == "graph_line_width:":
                graph_line_width = int(sys.argv[i].strip()[17:])
            elif sys.argv[i].strip().lower()[:15] == "toc_line_color:":
                TOC_line_color = sys.argv[i].strip().lower()[15:]
                if TOC_line_color[0] == "(":
                    TOC_line_color = "rgb" + TOC_line_color
            elif sys.argv[i].strip().lower()[:11] == "line_color:":
                line_color = sys.argv[i].strip().lower()[11:]
                if line_color[0] == "(":
                    line_color = "rgb" + line_color
            elif sys.argv[i].strip().lower()[:15] == "toc_line_width:":
                TOC_line_width = int(sys.argv[i].strip()[15:])
            elif sys.argv[i].strip().lower()[:11] == "line_width:":
                line_width = int(sys.argv[i].strip()[11:])
            elif sys.argv[i].strip().lower()[:18] == "toc_pages_spacing:":
                arguments = sys.argv[i].strip()[18:].split(":")
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
            elif sys.argv[i].strip().lower()[:10] == "no_merging":
                no_merging = True
            elif sys.argv[i].strip().lower()[:22] == "toc_subject_font_size:":
                TOC_subject_font_size = int(sys.argv[i].strip()[22:])
            elif sys.argv[i].strip().lower()[:23] == "toc_subject_text_color:":
                TOC_subject_text_color = sys.argv[i].strip()[23:]
                if TOC_subject_text_color[0] == "(":
                    TOC_subject_text_color = "rgb" + TOC_subject_text_color
            elif sys.argv[i].strip().lower()[:17] == "toc_subject_text:":
                TOC_subject_text = sys.argv[i].strip()[17:]
            elif sys.argv[i].strip().lower()[:20] == "toc_pages_font_size:":
                TOC_pages_font_size = int(sys.argv[i].strip()[20:])
            elif sys.argv[i].strip().lower()[:21] == "toc_pages_text_color:":
                TOC_pages_text_color = sys.argv[i].strip()[21:]
                if TOC_pages_text_color[0] == "(":
                    TOC_pages_text_color = "rgb" + TOC_pages_text_color
            elif sys.argv[i].strip().lower()[:15] == "toc_pages_text:":
                TOC_pages_text = sys.argv[i].strip()[15:]

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
if jpeg_files == []:
    print('\nPlease include a JPEG file containing the image that you ' +
    'wish to use as a background for the book cover in the working folder. Also, please ' +
    'make sure that the provided background image is in JPEG format, ' +
    "with a resolution of 300 ppi and a canvas size of US Legal dimensions in " +
    "landscape mode (width of 4200 pixels and height of 2550 pixels).\n")
    problem = True
else:
    cover_background_img = None
    page_background_img = None
    for i in range(len(jpeg_files)):
        if os.path.split(jpeg_files[i])[-1][:5].lower() == "cover":
            cover_background_img = jpeg_files[i]
        elif os.path.split(jpeg_files[i])[-1][:9].lower() in ["left page", "left_page"]:
            left_page_background_img = jpeg_files[i]
        elif os.path.split(jpeg_files[i])[-1][:10].lower() in ["right page", "right_page"]:
            right_page_background_img = jpeg_files[i]
    if (cover_background_img == None or (len(jpeg_files) > 1 and
    left_page_background_img == None and right_page_background_img == None)):
        print('\nPlease include a JPEG file containing the image that you ' +
        'wish to use as a background for the book cover in the working folder. Also, please ' +
        'make sure that the provided background image is in JPEG format, ' +
        "with a resolution of 300 ppi and a canvas size of US Legal dimensions in " +
        'landscape mode (width of 4200 pixels and height of 2550 pixels) and that the ' +
        'file name starts with "cover".\n\n' +
        "Moreover, if you wish to add an image template to your notebook, the image " +
        "needs to have a resolution of 300 ppi and a canvas size of US Letter dimensions in " +
        "landscape mode (width of 3300 pixels and height of 2550 pixels), with margins according " +
        "to the specifications (default left and margins 1/4 inch, top margin 1 inch and bottom " +
        'margin 3/4 inch). Also, make sure to add the prefix "left page" or "right page" to the jpeg file name.')
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
not in [0, None] and inches_per_ream_500_pages not in [0, None]):

    #In order for the booklet numbering to allow for duplex printing,
    #the sum of the TOC pages and the notebook pages needs to be
    #dividable by four (as one sheet of paper contains two pages on
    #each side). If this is not the case, the "number_of_pages" will
    #be incremented by one page until this criterion is met.
    if (number_of_pages + TOC_pages)%4 != 0:
        while (number_of_pages + TOC_pages)%4 != 0:
            number_of_pages += 1

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

    #It was found that the page numbers written with the Baskerville font at 60 px of font size
    #were in fact 40 px in height, most likely because the Baskerville typeface leaves 10 px above
    #and below the characters for diacritics. Therefore, the correction factor of 2/3 is applied when
    #determining the value of the "y" coordinate of the middle point of the page numbers
    #("page_numbers_bottom_margin_y_pixel"). This correction factor may not be valid for other typefaces,
    #but the the user always has the option of overriding this code by providing a value for
    #"page_numbers_bottom_margin_y_pixel" when running the Python code.
    if page_numbers_bottom_margin_y_pixel == None:
        page_numbers_bottom_margin_y_pixel = 2550-(75 + (page_numbers_font_size/2)*2/3)

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

    #The number of pages and thickness of a ream of paper of 500 pages will allow to determine
    #the dimensions of the rectangle that will mark the location of the spine of the book
    #on a US Legal canvas in Landscape mode and with a resolution of 300 ppi.
    spine_thickness_inches = inches_per_ream_500_pages*total_number_of_pages/500
    spine_thickness_pixels = int(inches_per_ream_500_pages*4200/14)

    #The "ImageDraw" module will load the default background image (which
    #the user can change by selecting another image in the working folder and
    #passing in its name as an additional argument, when calling the Python code.
    font_title = ImageFont.truetype(cover_font, cover_title_font_size)
    image = Image.open(cover_background_img)
    #If the user has provided a custom template page JPEG image, it will be
    #opened and an editable version will be instantiated. Two subsequent "if"
    #statements are required here, as there may be different images for the
    #left and right pages (if the designs are to be present on both pages,
    #accordingly with the "").
    if left_page_background_img != None:
        left_custom_template_image = Image.open(left_page_background_img)
    if right_page_background_img != None:
        right_custom_template_image = Image.open(right_page_background_img)


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
            cover_text_color = "LightGrey"
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

    else:
        if cover_box_color != None and cover_box_color[0] == "(":
            cover_box_color = "rgb" + cover_box_color
        elif cover_box_color == None:
            cover_box_color = "Black"
        if cover_text_color != None and cover_text_color[0] == "(":
            cover_text_color = "rgb" + cover_text_color
        elif cover_text_color == None:
            cover_text_color = "White"
    #The length (in pixels) taken up by the title is determined using the
    #"textlength()" method, using the "font_title" with the default font size
    #"cover_title_font_size".
    title_length_pixels = image_editable.textlength(title, font_title)
    #The "cover_title_offset" variable stores the offset length in pixels required on the x axis so that the
    #title is centered within the black rectangle. The offset is calculated as the difference between the
    #middle points of the total available horizontal space and the length of the title.
    cover_title_offset = round((right_margin_cover_text-left_margin_cover_text)/2 - title_length_pixels/2)
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
    if title_length_pixels > available_horizontal_space_pixels:
        title_words = re.split(r"( )", title)
        number_of_title_words = len(title_words)
        middle_index_in_title = len(title)//2
        character_count = 0
        word_delimitor = None
        for i in range(len(title_words)):
            if character_count <= middle_index_in_title - (len(title_words[i])+1):
                character_count += len(title_words[i])
            else:
                word_delimitor = i
                break
        first_half_words = title_words[:word_delimitor]
        first_half_words_string = "".join(first_half_words)
        second_half_words = title_words[word_delimitor:]
        second_half_words_string = "".join(second_half_words)
        if first_half_words != []:
            adjusted_title_cover = first_half_words_string + "\n" + second_half_words_string

            while cover_title_font_size > 50:
                if (image_editable.textlength(first_half_words_string, font_title) >
                available_horizontal_space_pixels or
                image_editable.textlength(second_half_words_string, font_title) >
                available_horizontal_space_pixels):
                    cover_title_font_size-=1
                    font_title = ImageFont.truetype(cover_font, cover_title_font_size)
                else:
                    #If the title was split, the "cover_title_height" variable is updated to
                    #reflect that the text now spans two lines, including the spacing
                    #in-between the lines ("cover_title_line_spacing").
                    cover_title_height = 2*cover_title_font_size + cover_title_line_spacing
                    break
        #If there is only one word in the title and that word happens to be very long,
        #then instead of splitting the title in half, the font size "cover_title_font_size"
        #will be decremented until the fitle fits within the cover box.
        else:
            while cover_title_font_size > 50:
                if (image_editable.textlength(title, font_title) >
                available_horizontal_space_pixels):
                    cover_title_font_size-=1
                    font_title = ImageFont.truetype(cover_font, cover_title_font_size)
                else:
                    #If the title wasn't split, but was resized, the "cover_title_height"
                    #variable is updated to reflect this. As the text does not span two lines,
                    #"cover_title_font_size" isn't multiplied by 2.
                    cover_title_height = cover_title_font_size + cover_title_line_spacing
                    break

        #The "cover_title_offset" variable stores the offset length in pixels required on
        #the x axis so that the title is centered within the black rectangle. The carriage
        #returns ("\n") are removed if present, as the "textlength()" method does not allow
        #for them within the passed in string. The offset is calculated as the difference
        #between the middle points of the total available horizontal space and the length of the
        #longest of the two lines of the split title. Since the title has been split, the
        #original offset is overwritten with the one reflecting the length of the split title.
        first_half_words_string_length = (image_editable.textlength(first_half_words_string
        .replace("\n", ""), font_title))
        second_half_words_string_length = (image_editable.textlength(second_half_words_string
        .replace("\n", ""), font_title))
        cover_title_offset = (round((right_margin_cover_text-left_margin_cover_text)/2-
        max([first_half_words_string_length, second_half_words_string_length])/2))

    #As the author name font size should be at most 75% of that of the title,
    #the initial font size is set to 75% of "cover_title_font_size".
    cover_author_font_size = round(0.75*cover_title_font_size)
    font_author = ImageFont.truetype(cover_font, cover_author_font_size)
    cover_author_height = cover_author_font_size
    author_length_pixels = image_editable.textlength(author, font_author)
    #The "cover_author_offset" variable stores the offset length in pixels required on the
    #x axis so that the author name (which should be smaller than the title, in principle)
    #is centered within the black rectangle. The offset is calculated as the difference
    #between the middle points of the total available horizontal space and the length of
    #the author name.
    cover_author_offset = (round((right_margin_cover_text-left_margin_cover_text)/2 -
    author_length_pixels/2))
    available_horizontal_space_pixels = round((right_margin_cover_text-left_margin_cover_text))
    if author_length_pixels > available_horizontal_space_pixels:
        author_words = re.split(r"( )", author)
        number_of_author_words = len(author_words)
        middle_index_in_author = len(author)//2
        character_count = 0
        word_delimitor = None
        for i in range(len(author_words)):
            if character_count <= middle_index_in_author - (len(author_words[i])+1):
                character_count += len(author_words[i])
            else:
                word_delimitor = i
                break
        first_half_words = author_words[:word_delimitor]
        first_half_words_string = "".join(first_half_words)
        second_half_words = author_words[word_delimitor:]
        second_half_words_string = "".join(second_half_words)
        adjusted_author_cover = first_half_words_string + "\n" + second_half_words_string
        adjusted_author = first_half_words_string + "\n" + second_half_words_string

        while cover_author_font_size > 50*max_author_title_font_ratio:
            if (image_editable.textlength(first_half_words_string, font_author) >
            available_horizontal_space_pixels or
            image_editable.textlength(second_half_words_string, font_author) >
            available_horizontal_space_pixels):
                cover_author_font_size-=1
                font_author = ImageFont.truetype(cover_font, cover_author_font_size)
            else:
                break
        cover_author_height = 2*cover_author_font_size + cover_author_line_spacing

        #The "cover_author_offset" variable stores the offset length in pixels required on
        #the x axis so that the author name (which should be smaller than the title, in
        #principle) is centered within the black rectangle. The carriage returns ("\n") are
        #removed if present, as the "textlength()" method does not allow for them within the
        #passed in string. The offset is calculated as the difference between the middle points
        #of the total available horizontal space and the length of the longest of the two lines
        #of the split author name.
        first_half_words_string_length = (image_editable.textlength(first_half_words_string
        .replace("\n", ""), font_author))
        second_half_words_string_length = (image_editable.textlength(second_half_words_string
        .replace("\n", ""), font_author))
        cover_author_offset = (round((right_margin_cover_text-left_margin_cover_text)/2-
        max([first_half_words_string_length, second_half_words_string_length])/2))

    #The lowest y coordinates of the black and light rectangles are determined below by
    #adding the vertical distances of the elements above it. They add the y coordinate
    #at which the text starts to be written ("vertical_margin_cover_text") to the height
    #of the title ("cover_title_height"), the vertical spacing in-between title and author
    #name ("round(cover_spacing_title_height_ratio*cover_title_height)"), the height of
    #the author name ("cover_author_height") and finally the number of pixels matching
    #the spacing above the text on top of the rectangle (125 px).
    cover_dark_rectangle_end_y = (vertical_margin_cover_text + cover_title_height +
    round(cover_spacing_title_height_ratio*cover_title_height) + cover_author_height + 125)

    #A filled-in rectangle with rounded is drawn on the background using the
    #"rounded_rectangle()" method from the Pillow module. It's top left "x,y"
    #coordinates are "left_margin_cover_textbox", "top_margin_cover_textbox"
    #and it s bottom right "x,y" coordinates are "right_margin_cover_textbox",
    #"cover_dark_rectangle_end_y". The radius of the corners are set to 50
    #pixels for the darker and larger rectangle and 48 pixels for the smaller
    #lighter rectangle (proportional radius to the decrease in size of the rectangle).

    #The "cover_trim_width_pixels" is calculated from the variable "cover_trim_width"
    #and the know ratio of 4200 pixels per 14 inches at 300 ppi resolution. The
    #"cover_trim_width_pixels" will be used to draw a white trim around the canvas
    #to account for the non-printable area. As such, the rectangle and text containing
    #the title and author information on the front cover will be offset by that amount
    #(split evenly on either side of the rectangle), to keep the margins on either side
    #of the rectangle even despite the presence of such a white trim.

    cover_trim_width_pixels = round(cover_trim_width*4200/14)
    image_editable.rounded_rectangle([(left_margin_cover_textbox-
    round(cover_trim_width_pixels/2),top_margin_cover_textbox),
    (right_margin_cover_textbox-round(cover_trim_width_pixels/2),
    cover_dark_rectangle_end_y)], radius=50, fill=cover_box_color)
    #The lighter rectangle has vertical and horizontal dimensions
    #50 pixels smaller than the larger darker rectangle.
    image_editable.rounded_rectangle([(left_margin_cover_textbox+25-
    round(cover_trim_width_pixels/2), top_margin_cover_textbox+25),
    (right_margin_cover_textbox-25-round(cover_trim_width_pixels/2),
    cover_dark_rectangle_end_y-25)], radius=48, outline=cover_text_color, width=10)
    #If the title was too large to fit within the "available_horizontal_space_pixels",
    #it was split into two lines and will be written in light font (fill = light_text_color)
    #with centered alignment and starting at the "x,y" coordinate "left_margin_cover_text",
    #"vertical_margin_cover_text", using the "multiline_text()" method of the Pillow module
    #with the "adjusted_title_cover" string containing a carriage return "\n" after the
    #"first_half_words_string".

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
        image_editable.multiline_text((left_margin_cover_text +
        cover_title_offset-round(cover_trim_width_pixels/2) +
        pixels_from_left_cover_title_box, vertical_margin_cover_text +
        pixels_from_top_cover_title_box),
        adjusted_title_cover, fill=cover_text_color, font=font_title, align="center",
        spacing=cover_title_line_spacing)
    #If the title wasn't split, it will be written using the "text"() method of the Pillow module
    else:
        image_editable.text((left_margin_cover_text + cover_title_offset
        -round(cover_trim_width_pixels/2) + pixels_from_left_cover_title_box,
        vertical_margin_cover_text + pixels_from_top_cover_title_box),
        title, fill=cover_text_color, font=font_title, align="center")
    #A similar approach is taken for the author name, except that since it is written in smaller sized font,
    #it needs a horizontal offset ("cover_author_offset") in order to be centered. Also, the text begins at
    #a lower point in the dark rectangle, which is the "vertical_margin_cover_text" y coordinate plus the
    #height of the title "cover_title_height" and the vertical spacing in-between the title and the author
    #name ("round(cover_spacing_title_height_ratio*cover_title_height)")
    if adjusted_author_cover != None:
        image_editable.multiline_text((left_margin_cover_text +
        cover_author_offset-round(cover_trim_width_pixels/2),
        vertical_margin_cover_text + cover_title_height +
        round(cover_spacing_title_height_ratio*cover_title_height)),
        adjusted_author_cover, fill=cover_text_color, font=font_author,
        align="center", spacing=cover_author_line_spacing)
    else:
        image_editable.text((left_margin_cover_text +
        cover_author_offset-round(cover_trim_width_pixels/2),
        vertical_margin_cover_text + cover_title_height +
        round(cover_spacing_title_height_ratio*cover_title_height)),
        author, fill=cover_text_color, font=font_author, align="center")

    #The rectangles for the spine are drawn in a similar way as for the title and author name,
    #except that the width depends on the number of pages in the book and the thickness of a
    #ream of paper of 500 pages, which are both provided as additional arguments by the user
    #when running the code. The width of the spine in pixels "width_of_spine_pixels" is
    #determined by multiplying the "inches_per_ream_500_pages" by the number of pages in the
    #book ("total_number_of_pages"), and then dividing by two (as every sheet of 8.5x11" paper will
    #result in two leaves of the book (each containing two pages) pages in the book) and then
    #by 500 to get the number of inches of thickness for the book. The number of inches is
    #then multiplied by the pixel count for the width of the Legal page in landscape mode
    #(4200 pixels at 300 ppi) and then divided by the corresponding inch measurement for
    #that width (14").
    width_of_spine_pixels = inches_per_ream_500_pages*total_number_of_pages/2/500*4200/14

    #A white trim of "cover_trim_width" inches in width (which is converted into pixels
    #(cover_trim_width*4200/14)) will be drawn on the outer edges of the canvas, except
    #the left side, where another similar trim will be drawn where the back cover ends,
    #enabling the user to easily cut out the excess paper from the Legal cardstock after printing.
    image_editable.rectangle([(0,0),(4200, cover_trim_width_pixels)], fill="white")
    image_editable.rectangle([(round(4200-cover_trim_width*4200/14),0),(4200, 2550)], fill="white")
    image_editable.rectangle([(0,2550-cover_trim_width_pixels),(4200, 2550)], fill="white")
    #The top left corner of the white rectangle is shifted to the left by "2*cover_extra_pixels"
    #pixels, to account for the extra pixels added on the left and right covers. Also, an extra
    #6 pixels (equivalent to about 0.5 mm) are added to the width of the white rectangle on the
    #left vertical side, to allow to cut the line while excluding the pattern on the excess cardstock.
    image_editable.rectangle([(4200-round(11*4200/14+width_of_spine_pixels+2*cover_extra_pixels)-6,0),
    (4200-round(11*4200/14+width_of_spine_pixels+2*cover_extra_pixels) + cover_trim_width_pixels, 2550)], fill="white")
    if cover_line == True:
        #If the variable "cover_line" is set to "True" , a dark trim
        #of color "dark_color" is drawn directly within the white border, so as to harmonize
        #the white border with the rest of the contents of the cover. Once again, the top left
        #corner of the dark rectangle is shifted to the left by "2*cover_extra_pixels"
        #pixels, to account for the extra pixels added on the left and right covers.
        image_editable.rectangle([((4200-round(11*4200/14+width_of_spine_pixels+2*cover_extra_pixels))+
        cover_trim_width_pixels,cover_trim_width_pixels),(4200-cover_trim_width_pixels,
        2550-cover_trim_width_pixels)], outline=cover_box_color, width = 25)

    #The "x,y" coordinates of the top left corner of the rectangle are calculated based on the
    #width of the covers of the book (14"-5.5"=8.5") and the pixel count is given using the known
    #pixel numbers for the width of a Legal page in landscape mode (4200 pixels at 300 ppi).
    #The width of the spine is then subracted in order to reach the left "x" coordinate with
    #the subtraction of "cover_extra_pixels" pixels to account for the space needed to fold
    #the spine and for the added thickness imparted by the glue. The top "y" coordinate is set
    #at one inch from the top of the page, and the bottom "y" coordinate of the bottom right
    #corner is set at one inche from the bottom of the page (8.5"-1"=7.5"). The bottom right
    #corner "x" coordinate is calculated based on the width of the covers of the book (14"-5.5"=8.5")
    #and the pixel count is determined using the Legal proportions as above, with "cover_extra_pixels"
    #pixels being subtracted to avoid spillover of the black spine onto the cover page when folding
    #the cover paper.
    image_editable.rounded_rectangle([(8.5*4200/14-width_of_spine_pixels-cover_extra_pixels,1.0*4200/14),
    (8.5*4200/14-cover_extra_pixels,7.5*4200/14)], radius=50, fill=cover_box_color)

    #If the user hasn't specified some text to be included on the spine ("spine_text == None"),
    #the author name is initialized to take up less space on the spine. First, the name is
    #split at every space or hyphen, with inclusion of those characters as separate elements
    #in the "author_name_split" list (given the use of parentheses). Then, the names are
    #cycled through in the "for" loop and if the element isn't the last one in the list,
    #meaning that it is not the last name, and if it isn't a space or a hyphen and if its
    #length is more than 1 and the second character isn't a period, then that name is
    #initialized.
    if spine_text == None:
        author_name_split = re.split(r"([' '-])", author)
        for i in range(len(author_name_split)):
            if (author_name_split[i] not in [" ", "-"] and (len(author_name_split[i]) > 1 and
            author_name_split[i][1] != ".") and i < len(author_name_split)-1):
                author_name_split[i] = author_name_split[i][0] + "."
        author_spine = "".join(author_name_split) + " — "

        #The "spine_text" containing the text written on the spine is assembled.
        spine_text = author_spine + title.strip()
    #Similar to what was done above, the font size of the spine
    #initialized to 100 pixels (unless the user specified something different),
    #will be optimized to the available space.
    #However, in this case both the horizontal and vertical
    #space need to be considered, as only one line of text can fit
    #onto the spine (so the string will not be split into two lines
    #as for the title and author box).
    font_spine = ImageFont.truetype(cover_font, spine_font_size)

    spine_text_length_pixels = image_editable.textlength(spine_text, font_spine)

    #Similarly to the title and author box, a white rectangle 25 pixels distant from the edge
    #of the black rectangle is drawn only if the number of pages is over 300, as its presence
    #decreases the available space for the spine text.
    if total_number_of_pages >= 300:
        image_editable.rounded_rectangle([(8.5*4200/14-width_of_spine_pixels+25-cover_extra_pixels,1.0*4200/14+25),
        (8.5*4200/14-25-cover_extra_pixels,7.5*4200/14-25)], radius=round((width_of_spine_pixels
        -50)/width_of_spine_pixels*50), outline=cover_text_color, width=10)

        #The available space on the horizontal axis is determined by subtracting the
        #"x" coordinate of the bottom right corner of the spine dark rectangle from
        #that of the top left corner. 70 pixels are subtracted from that amount to
        #account for the space between the pale rectangle vertical edges and the text.
        available_horizontal_space_pixels = (round((8.5*4200/14-25)-
        (8.5*4200/14-width_of_spine_pixels+25))-70)
        #As there is one inch above and below the dark rectangle, the height of the
        #dark rectangle is equal to the height of the Legal page in landscape mode
        #minus two inches (8.5"-2"=6.5"). 50 pixels are subtracted to account for the
        #margins between the edges of the dark rectangle and the lighter line, and
        #another 70 pixels are subtracted from that amount to allow for space between
        #the pale rectangle horizontal edges and the text.
        available_vertical_space_pixels = 6.5*4200/14-50-70

        #If either the length of the "spine_text" in pixels ("spine_text_length_pixels")
        #exceeds the "available_vertical_space_pixels" or if the height of the spine font
        #"spine_font_size" is above the "available_horizontal_space_pixels", the "spine_font_size"
        #will be decremented until both dimensions are within range of the available space.
        if (spine_text_length_pixels > available_vertical_space_pixels or
        spine_font_size > available_horizontal_space_pixels):
            while cover_title_font_size > 25:
                if (image_editable.textlength(spine_text, font_spine) > available_vertical_space_pixels or
                spine_font_size > available_horizontal_space_pixels):
                    spine_font_size-=1
                    font_spine = ImageFont.truetype(cover_font, spine_font_size)
                else:
                    spine_text_length_pixels = image_editable.textlength(spine_text, font_spine)
                    break

        #The offset on the x and y axis are determined by subtracting the halfpoint of
        #either dimension of the "spine_text" from the that of the available space in
        #the corresponding dimension of the rectangle. In the case of "offset_y", the
        #"pixels_from_bottom_cover_spine" are subtracted from it in order to bring the
        #text further up from the bottom of the spine dark rectangle. This allows to
        #fine-tune the automatic centering on the vertixal axis, given that the spine
        #is fairly narrow and any unevenness are easily noticeable. A similar approach
        #is taken with the variable "pixels_from_left_cover_spine", where pixels are
        #added to the "x" axis (in the rotated image) to adjust the point where the
        #spine text will start to be written.
        offset_x = (round(available_vertical_space_pixels/2 - spine_text_length_pixels/2) +
        pixels_from_left_cover_spine)
        offset_y = (round(available_horizontal_space_pixels/2 - spine_font_size/2) +
        cover_extra_pixels - pixels_from_bottom_cover_spine)

        #The image is outputted in PNG format.
        image.save(title + " (cover).png", "PNG")

        #As text can only be written horizontally in Pillow, the image is reloaded and
        #rotated 90 degrees clockwise in order to write the text on the spine.
        image_rotated = (Image.open(title +
        " (cover).png").convert("RGB").rotate(90, expand = True))
        image_rotated_editable = ImageDraw.Draw(image_rotated)

        #The starting x and y coordinates mirror the measurements in the unrotated image.
        #The left side of the dark rectangle is then one inch from the top of the canvas
        #in the rotated image, with 25 pixels added to reach the light line and another 35
        #pixels to reach the point where the text will start to be written, with the addition
        #of the "offset_x".
        #The top of the dark rectangle now stands 5.5 inches from the top of the canvas
        #(the origin 0,0 being in the top left corner), with 25 pixels added to reach the
        #lighter line, and 28 pixels to reach the point where the text will start to be
        #written, with the addition of the "offset_y"
        spine_text_starting_x = round(1.0*4200/14+25 + 35 + offset_x)
        spine_text_starting_y = round(5.5*4200/14+25+28 + offset_y)

        image_rotated_editable.text((spine_text_starting_x, spine_text_starting_y),
        spine_text, fill=cover_text_color, font=font_spine, align="center")

    #If the "total_number_of_pages" is below 300, the white rectangle will not be drawn to allow
    #for more space for the text on a smaller spine. The margins are adjusted in consequence.
    else:
        #The "space_offset" was determined by linear regression between a number of pages
        #of 299 and 200, and represents the combined number of pixels on either side of the
        #spine text, between the edges of the long sides of the spine and the spine text. That
        #margin decreases linearly down to zero at a page count of 200, below which the
        #"space_offset" is set to 12 pixels.
        space_offset = round(0.71*total_number_of_pages-142)
        if total_number_of_pages < 200:
            space_offset = 12
        #The available space on the horizontal axis is determined by subtracting the
        #"x" coordinate of the bottom right corner of the spine dark rectangle from
        #that of the top left corner. "space_offset" pixels are subtracted from that amount to
        #account for the space between the pale rectangle vertical edges and the text.
        #As "space_offset" effectively acts as a margin, it is subtracted from the
        #available horizontal pixels.
        available_horizontal_space_pixels = (round((8.5*4200/14)-
        (8.5*4200/14-width_of_spine_pixels))-space_offset)

        #As there is one inch above and below the dark rectangle, the height of the
        #dark rectangle is equal to the height of the Legal page in landscape mode
        #minus two inches (8.5"-2"=6.5"). 70 pixels are subtracted from that amount
        #to allow for space between the pale rectangle horizontal edges and the text.
        available_vertical_space_pixels = 6.5*4200/14-70

        #If either the length of the "spine_text" in pixels ("spine_text_length_pixels")
        #exceeds the "available_vertical_space_pixels" or if the height of the spine font
        #"spine_font_size" is above the "available_horizontal_space_pixels", the "spine_font_size"
        #will be decremented until both dimensions are within range of the available space.
        if (spine_text_length_pixels > available_vertical_space_pixels or
        spine_font_size > available_horizontal_space_pixels):
            while spine_font_size > 25:
                if (image_editable.textlength(spine_text, font_spine) >
                available_vertical_space_pixels or
                spine_font_size > available_horizontal_space_pixels):
                    spine_font_size-=1
                    font_spine = ImageFont.truetype(cover_font, spine_font_size)
                else:
                    break
            spine_text_length_pixels = image_editable.textlength(spine_text, font_spine)
        #The offset on the x and y axis are determined by subtracting the halfpoint of
        #either dimension of the "spine_text" from the that of the available space in
        #the corresponding dimension of the rectangle. In the case of "offset_y", the
        #"pixels_from_bottom_cover_spine" are subtracted from it in order to bring the
        #text further up from the bottom of the spine dark rectangle. This allows to
        #fine-tune the automatic centering on the vertixal axis, given that the spine
        #is fairly narrow and any unevenness are easily noticeable.
        offset_x = round(available_vertical_space_pixels/2 - spine_text_length_pixels/2)
        offset_y = (round(available_horizontal_space_pixels/2 - spine_font_size/2) +
        cover_extra_pixels - pixels_from_bottom_cover_spine)

        #The image is outputted in PNG format.
        image.save(title + " (cover).png", "PNG")

        #As text can only be written horizontally in Pillow, the image is reloaded and
        #rotated 90 degrees clockwise in order to write the text on the spine.
        image_rotated = (Image.open(title +
        " (cover).png").convert("RGB").rotate(90, expand = True))
        image_rotated_editable = ImageDraw.Draw(image_rotated)

        #The starting x and y coordinates mirror the measurements in the unrotated image.
        #The left side of the dark rectangle is then one inch from the top of the canvas
        #in the rotated image, with 35 pixels to reach the point where the text will start
        #to be written, with the addition of the "offset_x".
        #The top of the dark rectangle now stands 5.5 inches from the top of the canvas
        #(the origin 0,0 being in the top left corner), with "space_offset/2" pixels to reach
        #the point where the text will start to be written, with the addition of the "offset_y"
        spine_text_starting_x = round(1.0*4200/14 + 35 + offset_x)
        spine_text_starting_y = round(5.5*4200/14 + (space_offset/2) + offset_y)

        image_rotated_editable.text((spine_text_starting_x, spine_text_starting_y),
        spine_text, fill=cover_text_color, font=font_spine, align="center")

    #The image is once more outputted in PDF format, and the original
    #unrotated PNG image is deleted.
    image_rotated.save(title + " (cover).pdf", quality=100, resolution=300)
    os.remove(title + " (cover).png")

    current_page = 1
    unmatching_pages = 0
    page_numbers_list = list(range(1, number_of_pages+1))

    #A new blank canvas in landscape format (2550 pixels in height by 3300 pixels in width)
    #is created for every page of the notebook. An editable version is created to allow
    #for modifications ("blank_canvas_editable").
    for i in range(1, round((total_number_of_pages)/2)+1):
        blank_canvas = Image.open(os.path.join(cwd, "Blank Letter Landscape Canvas", "Blank Letter Landscape Canvas.jpg"))
        blank_canvas_editable = ImageDraw.Draw(blank_canvas)

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
            pixel_increment = round(line_distance_inches*2550/8.5 + line_width)
            line_y_coordinates = []
            while starting_y <= bottom_margin_y_pixel:
                line_y_coordinates.append(starting_y)
                starting_y += pixel_increment
            return line_y_coordinates

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
                #The "dot_y_shift_down" variable stores the
                #amount of pixels that will be added to the
                #starting "y" coordinate.  The graph paper
                #starting "y" coordinate needs to be shifted
                #down by the same amount of pixels (dot_diameter_pixels)
                #as the lines of the TOC were, so that both
                #the TOC lines and the horizontal graph paper
                #lines may line up with the dots.
                starting_y = top_margin_y_pixel + dot_diameter_pixels
            else:
                starting_y = top_margin_y_pixel
            pixel_increment = round(line_distance_inches*2550/8.5)
            line_y_coordinates_graph = []
            while starting_y <= bottom_margin_y_pixel:
                line_y_coordinates_graph.append(starting_y)
                starting_y += pixel_increment
            return line_y_coordinates_graph

        if graph_paper == True or graph_paper_left == True or graph_paper_right == True:
            line_y_coordinates_graph = get_line_y_coordinates_graph_paper(1/squares_per_inch, graph_line_width)
            two_last_y_graph = [line_y_coordinates_graph[-2], line_y_coordinates_graph[-1]]

        def get_dot_y_coordinates(inches_between_dots, dot_diameter_pixels):
            #The "dot_y_shift_down" variable stores the
            #amount of pixels that will be added to the
            #starting "y" coordinate.  The value of
            #"dot_y_shift_down" is only different than
            #zero if there are no ruled lines in the notebook,
            #so that the dots may line up with TOC ruled lines.
            starting_y = top_margin_y_pixel + dot_y_shift_down
            pixel_increment = round(inches_between_dots*2550/8.5)
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


        #The function "get_last_y_TOC" will compare the last "y" coordinate
        #for a ruled/dot/graph format with the last "y" coordinate of the TOC
        #in order to line them up better at the bottom of the page. A separate
        #function from "get_last_y" is required, as the "maximum_y_coordinate"
        #only pertains to pages that could have page numbers, which is not
        #the case for TOC pages. Thus, "y_coordinates_2[-1]" is always returned
        #in this function for the value of "maximum_y_coordinate".
        def get_last_y_TOC(TOC_line_spacing, y_coordinates_2):
            if TOC_line_spacing[-1] < y_coordinates_2[-1]:
                if (abs(y_coordinates_2[-2]-TOC_line_spacing[-1]) <
                abs(y_coordinates_2[-1]-TOC_line_spacing[-1])):
                    y_coordinates_2.pop(-1)
                    return y_coordinates_2[-1], TOC_line_spacing, y_coordinates_2
                else:
                    return y_coordinates_2[-1], TOC_line_spacing, y_coordinates_2
            elif TOC_line_spacing[-1] > y_coordinates_2[-1]:
                if (abs(TOC_line_spacing[-2]-y_coordinates_2[-1]) <
                abs(TOC_line_spacing[-1]-y_coordinates_2[-1])):
                    TOC_line_spacing.pop(-1)
                    return y_coordinates_2[-1], TOC_line_spacing, y_coordinates_2
                else:
                    return y_coordinates_2[-1], TOC_line_spacing, y_coordinates_2
            else:
                return y_coordinates_2[-1], TOC_line_spacing, y_coordinates_2

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
            page_number_vertical_center_point = (2550-maximum_y_coordinate)/2
            #If the user hasn't specified a value for "page_numbers_bottom_margin_y_pixel" and
            #the center "y" coordinate of the page numbers, when half the font size in pixels are subtracted
            #from it (to give the lowest "y" coordinate of the page numbers) is greater than 75 pixels
            #(the equivalent of 0.25 inch at 300 ppi, 0.25 in * 2550 px / 8.5 in = 75 px), it means that
            #there is enough room to center the text and the value of "page_numbers_bottom_margin_y_pixel"
            #is set to that corresponding pixel.
            if page_numbers_bottom_margin_y_pixel == 2550-(75 + (page_numbers_font_size/2)*2/3) and (page_number_vertical_center_point - page_numbers_font_size/2 > 75):
                page_numbers_bottom_margin_y_pixel = 2550 - page_number_vertical_center_point
        elif ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
        (college_ruled == True or college_ruled_left == True or college_ruled_right == True or
        wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True or
        custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True)):
            maximum_y_coordinate, dot_y_coordinates, line_y_coordinates = get_last_y(dot_y_coordinates, line_y_coordinates)
            page_number_vertical_center_point = (2550-maximum_y_coordinate)/2
            if page_numbers_bottom_margin_y_pixel == 2550-(75 + (page_numbers_font_size/2)*2/3) and (page_number_vertical_center_point - (page_numbers_font_size/2) > 75):
                page_numbers_bottom_margin_y_pixel = 2550 - page_number_vertical_center_point
        elif ((graph_paper == True or graph_paper_left == True or graph_paper_right == True) and
        (college_ruled == True or college_ruled_left == True or college_ruled_right == True or
        wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True or
        custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True)):
            maximum_y_coordinate, line_y_coordinates_graph, line_y_coordinates = get_last_y(line_y_coordinates_graph, line_y_coordinates)
            page_number_vertical_center_point = (2550-maximum_y_coordinate)/2
            if page_numbers_bottom_margin_y_pixel == 2550-(75 + (page_numbers_font_size/2)*2/3) and (page_number_vertical_center_point - page_numbers_font_size/2 > 75):
                page_numbers_bottom_margin_y_pixel = 2550 - page_number_vertical_center_point

        #If the notebook doesn't contain ruled pages (apart from the TOC) and has dot grids
        #(left pages, right pages or both pages), then the ruled lines on the TOC need to
        #line up with the horizontal lines dots, so the function "get_dot_y_coordinates" is
        #called instead of "get_line_y_coordinates". This will allow users to use the
        #"High Five" indexing method, as the TOC lines and dots line up.
        if (college_ruled == False and college_ruled_left == False and college_ruled_right == False and
        wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False and
        custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False and
        (dot_grid == True or dot_grid_left == True or dot_grid_right == True)):
            #The "dot_y_shift_down" variable stores the
            #amount of pixels that will be added to the
            #starting "y" coordinate.  The value of
            #"dot_y_shift_down" is only different than
            #zero if there are no ruled lines in the notebook,
            #so that the dots may line up with TOC ruled lines.
            dot_y_shift_down = dot_diameter_pixels
            line_y_coordinates_TOC = get_dot_y_coordinates(TOC_line_spacing, TOC_line_width)
        else:
            line_y_coordinates_TOC = get_line_y_coordinates(TOC_line_spacing, TOC_line_width)

        #The following "if" and "elif" statements deal with notebooks comprised of only one
        #design (ruled lines, graph paper or dot grids) or combinations of any one of those
        #designs with blank pages. The corresponding lists of "y" coordinates are passed into
        #the "get_last_y" function in order to ensure that the TOC pages and notebook pages
        #end as closely as possible on the "y" axis.
        if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
        (graph_paper == False and graph_paper_left == False and graph_paper_right == False) and
        (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
        (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
        (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
            maximum_y_coordinate, line_y_coordinates_TOC, dot_y_coordinates = get_last_y_TOC(line_y_coordinates_TOC, dot_y_coordinates)
            page_number_vertical_center_point = (2550-maximum_y_coordinate)/2
            if page_numbers_bottom_margin_y_pixel == 2550-(75 + (page_numbers_font_size/2)*2/3) and (page_number_vertical_center_point - page_numbers_font_size/2 > 75):
                page_numbers_bottom_margin_y_pixel = 2550 - page_number_vertical_center_point
        elif ((dot_grid == False and dot_grid_left == False and dot_grid_right == False) and
        (graph_paper == True or graph_paper_left == True or graph_paper_right == True) and
        (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
        (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
        (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
            maximum_y_coordinate, line_y_coordinates_TOC, line_y_coordinates_graph = get_last_y_TOC(line_y_coordinates_TOC, line_y_coordinates_graph)
            page_number_vertical_center_point = (2550-maximum_y_coordinate)/2
            if page_numbers_bottom_margin_y_pixel == 2550-(75 + (page_numbers_font_size/2)*2/3) and (page_number_vertical_center_point - page_numbers_font_size/2 > 75):
                page_numbers_bottom_margin_y_pixel = 2550 - page_number_vertical_center_point
        elif ((dot_grid == False and dot_grid_left == False and dot_grid_right == False) and
        (graph_paper == False and graph_paper_left == False and graph_paper_right == False) and
        ((college_ruled == True or college_ruled_left == True or college_ruled_right == True) or
        (wide_ruled == True or wide_ruled_left == True or wide_ruled_right == True) or
        (custom_ruled == True or custom_ruled_left == True or custom_ruled_right == True))):
            maximum_y_coordinate, line_y_coordinates_TOC, line_y_coordinates = get_last_y_TOC(line_y_coordinates_TOC, line_y_coordinates)
            page_number_vertical_center_point = (2550-maximum_y_coordinate)/2
            if page_numbers_bottom_margin_y_pixel == 2550-(75 + (page_numbers_font_size/2)*2/3) and (page_number_vertical_center_point - page_numbers_font_size/2 > 75):
                page_numbers_bottom_margin_y_pixel = 2550 - page_number_vertical_center_point

        if TOC_pages_text == "" and TOC_subject_text == "":
            first_TOC_line_index = 0
        else:
            first_TOC_line_index = 1

        #If the user didn't discard the table of contents ("TOC_pages_list != []") by entering zero
        #pages ("TOC_pages_spacing:0") and if the first page in "TOC_pages_list" is an odd number
        #(the first page of the list is popped out upon drawing a TOC page, hence this verification),
        #then the TOC heading is written on the right-hand (odd numbered) page.
        if TOC_pages_list != [] and (TOC_pages_list[0])%2 != 0:
            if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
            (graph_paper == False and graph_paper_left == False and graph_paper_right == False) and
            (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
            (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
            (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
                #Using the ImageDraw module, some ellipses are drawn, with a square dimensioned
                #bounding box, giving the corresponding circles with a diameter of "dot_diameter_pixels".
                #The dots are evenly spaced on the horizontal and vertical axes by a distance of
                #"inches_between_dots*2550/8.5" pixels, as there are 2550 pixels in 8.5 inches at an image
                #resolution of 300 ppi. The first horizontal line of dots at index 0 of "dot_y_coordinates"
                #is skipped over in order to allow for some space for the "Pages" and "Subject" subheadings
                #below the "Content" TOC heading.
                for j in range(first_TOC_line_index, len(dot_y_coordinates)):
                    starting_x = right_margin_x_pixel
                    while starting_x >= 3300/2+gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x -= round(inches_between_dots*2550/8.5)
            else:
                #The lines are then drawn for each of the "y" coordinates within the "line_y_coordinates_TOC"
                #list, starting at the "x" coordinate to the right of the gutter margin on the odd pages
                #("3300/2 + gutter_margin_width_pixels", so starting at the halfway point of the page on the
                #horizontal axis (3300/2 pixels), and then adding the number of pixels for the width of the
                #gutter margin), and ending at the right margin ("right_margin_x_pixel").
                for j in range(first_TOC_line_index, len(line_y_coordinates_TOC)):
                    blank_canvas_editable.line([(3300/2+gutter_margin_width_pixels, line_y_coordinates_TOC[j]),
                    (right_margin_x_pixel, line_y_coordinates_TOC[j])], fill = TOC_line_color, width = line_width)
            #The headers will be centered, using the "x" coordinate located at
            #three quarter of the page width pixels ("3300*0.75") and "y" coordinate at the
            #top of the upper margin ("heading_top_margin_y_pixel").
            blank_canvas_editable.text((3300*0.75, heading_top_margin_y_pixel),
            TOC_heading_text, fill=TOC_heading_text_color, font=TOC_heading_font, anchor="ms")
            #The "page" and "subject" headings are written at a vertical distance 1.5 times the heading text size,
            #to ensure that it is always proportionally spaced to the "contents" heading. The horizontal alignment
            #for the "pages" heading is set to the midway point of the horizontal dimension of the blank canvas
            #(3300/2 pixels, plus a third of the right page, with middle baseline "ms" anchoring.
            #On the other hand, the "subject" heading is written a two-thirds of the page width to the right
            #of the midway point of the page (3300/2+(3300/2*2/3).
            blank_canvas_editable.text((2200, heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_pages_text, fill=TOC_pages_text_color, font=TOC_pages_font, anchor="ms")
            blank_canvas_editable.text((2750, heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_subject_text, fill=TOC_subject_text_color, font=TOC_pages_font, anchor="ms")
        #A similar approach is taken if the first page in the "TOC_pages_list" is an even number.
        elif TOC_pages_list != [] and (TOC_pages_list[0])%2 == 0:
            if ((dot_grid == True or dot_grid_left == True or dot_grid_right == True) and
            (graph_paper == False and graph_paper_left == False and graph_paper_right == False) and
            (college_ruled == False and college_ruled_left == False and college_ruled_right == False) and
            (wide_ruled == False and wide_ruled_left == False and wide_ruled_right == False) and
            (custom_ruled == False and custom_ruled_left == False and custom_ruled_right == False)):
                for j in range(first_TOC_line_index, len(dot_y_coordinates)):
                    starting_x = left_margin_x_pixel
                    while starting_x <= 3300/2-gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x += round(inches_between_dots*2550/8.5)
            else:
                for j in range(first_TOC_line_index, len(line_y_coordinates_TOC)):
                    blank_canvas_editable.line([(left_margin_x_pixel, line_y_coordinates_TOC[j]),
                    (3300/2-gutter_margin_width_pixels, line_y_coordinates_TOC[j])], fill = TOC_line_color, width = line_width)
            blank_canvas_editable.text((3300/4, heading_top_margin_y_pixel),
            TOC_heading_text, fill=TOC_heading_text_color, font=TOC_heading_font, anchor="ms")
            blank_canvas_editable.text((550, heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_pages_text, fill=TOC_pages_text_color, font=TOC_pages_font, anchor="ms")
            blank_canvas_editable.text((1100, heading_top_margin_y_pixel + 1.5*heading_font_size),
            TOC_subject_text, fill=TOC_subject_text_color, font=TOC_pages_font, anchor="ms")

        #The user can choose to add a design to one or both pages by adding the JPEG image(s) to the
        #working folder, of which the file name starts with "left page" and/or "right page", so that the
        #code might distinguish it from the cover image (of which the file name begins with "cover").
        #The user would then pass in "custom_template_both_pages", "custom_template_left_page" or
        #"custom_template_right_page" when running the code.
        #The three "if" and "elif" statements below paste the design image onto both left and right pages
        #("if" statement), only on the left pages (first "elif" statement), or only on the right pages
        #("elif" statement).
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
                #which corresponds to the coordinates (3300/2+gutter_margin_width_pixels).
                blank_canvas.paste(right_custom_template_image, (int(3300/2), 0))
        elif custom_template_left_page == True:
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
               blank_canvas.paste(left_custom_template_image, (0, 0))

        elif custom_template_right_page == True:
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                blank_canvas.paste(right_custom_template_image, (int(3300/2), 0))


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
                    (3300/2-gutter_margin_width_pixels, y)], fill = line_color, width = line_width)
            #If there are no more table of contents pages to be drawn ("TOC_pages_list == []") or there are
            #still some table of contents pages to be drawn ("TOC_pages_list != []"), but the first page in
            #the "TOC_pages_list" is an even number, then the lines for the right side notebook page (odd numbered)
            #can be drawn in the second "if" statement.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(3300/2+gutter_margin_width_pixels, y),
                    (right_margin_x_pixel, y)], fill = line_color, width = line_width)
        elif (college_ruled == False and wide_ruled == False and custom_ruled == False and
        (college_ruled_left == True or wide_ruled_left == True or custom_ruled_left == True) and
        college_ruled_right == False and wide_ruled_right == False and custom_ruled_right == False):
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(left_margin_x_pixel, y),
                    (3300/2-gutter_margin_width_pixels, y)], fill = line_color, width = line_width)
        elif (college_ruled == False and wide_ruled == False and custom_ruled == False and
        college_ruled_left == False and wide_ruled_left == False and custom_ruled_left == False and
        (college_ruled_right == True or wide_ruled_right == True or custom_ruled_right == True)):
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                for y in line_y_coordinates:
                    blank_canvas_editable.line([(3300/2+gutter_margin_width_pixels, y),
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
                pixel_increment = round(1/squares_per_inch*2550/8.5)
                line_x_coordinates = []
                #The list of "x" coordinates where to draw the vertical lines is stored in the
                #"line_x_coordinates" list.
                while starting_x <= 3300/2-gutter_margin_width_pixels:
                    line_x_coordinates.append(starting_x)
                    starting_x += pixel_increment
                #Similarly to when drawing horizontal lines, bold lines are drawn whenever
                #the current line number is a multiple of "bold_line_every_n_squares" (if it isn't
                #equal to zero).
                for j in range(len(line_x_coordinates)):
                    if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                        blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                        (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
                        width = round(line_boldness_factor*graph_line_width))
                    elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                        blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                        (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
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
                pixel_increment = round(1/squares_per_inch*2550/8.5)
                line_x_coordinates = []
                while starting_x >= 3300/2+gutter_margin_width_pixels:
                    line_x_coordinates.append(starting_x)
                    starting_x -= pixel_increment
                for j in range(len(line_x_coordinates)):
                    if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                        blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                        (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
                        width = round(line_boldness_factor*graph_line_width))
                    elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                        blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                        (line_x_coordinates[j], line_y_coordinates_graph[-1])],
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
            pixel_increment = round(1/squares_per_inch*2550/8.5)
            line_x_coordinates = []
            while starting_x <= 3300/2-gutter_margin_width_pixels:
                line_x_coordinates.append(starting_x)
                starting_x += pixel_increment
            for j in range(len(line_x_coordinates)):
                if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                    blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                    (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
                    width = round(line_boldness_factor*graph_line_width))
                elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                    blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                    (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
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
            pixel_increment = round(1/squares_per_inch*2550/8.5)
            line_x_coordinates = []
            while starting_x >= 3300/2+gutter_margin_width_pixels:
                line_x_coordinates.append(starting_x)
                starting_x -= pixel_increment
            for j in range(len(line_x_coordinates)):
                if bold_line_every_n_squares != 0 and j%bold_line_every_n_squares == 0:
                    blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                    (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
                    width = round(line_boldness_factor*graph_line_width))
                elif bold_line_every_n_squares == 0 or j%bold_line_every_n_squares != 0:
                    blank_canvas_editable.line([(line_x_coordinates[j], line_y_coordinates_graph[0]),
                    (line_x_coordinates[j], line_y_coordinates_graph[-1])], fill = graph_line_color,
                    width = graph_line_width)

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
                #"inches_between_dots*2550/8.5" pixels, as there are 2550 pixels in 8.5 inches at an image
                #resolution of 300 ppi.
                for j in range(len(dot_y_coordinates)):
                    starting_x = left_margin_x_pixel
                    while starting_x <= 3300/2-gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x += round(inches_between_dots*2550/8.5)
            #Similar to the lined and graph pages on even and odd pages above, a second "if"
            #statement deals with drawing dots on the odd (right) pages.
            if TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0):
                for j in range(len(dot_y_coordinates)):
                    starting_x = right_margin_x_pixel
                    while starting_x >= 3300/2+gutter_margin_width_pixels:
                        blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                        dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                        (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                        fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                        starting_x -= round(inches_between_dots*2550/8.5)

        elif (dot_grid == False and dot_grid_left == True and dot_grid_right == False and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0))):
            for j in range(len(dot_y_coordinates)):
                starting_x = left_margin_x_pixel
                while starting_x <= 3300/2-gutter_margin_width_pixels:
                    blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                    dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                    (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                    fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                    starting_x += round(inches_between_dots*2550/8.5)

        elif (dot_grid == False and dot_grid_left == False and dot_grid_right == True and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0))):
            for j in range(len(dot_y_coordinates)):
                starting_x = right_margin_x_pixel
                while starting_x >= 3300/2+gutter_margin_width_pixels:
                    blank_canvas_editable.ellipse([(starting_x - int(dot_diameter_pixels/2),
                    dot_y_coordinates[j] - int(dot_diameter_pixels/2)),
                    (starting_x + int(dot_diameter_pixels/2), dot_y_coordinates[j] + int(dot_diameter_pixels/2))],
                    fill = dot_fill_color, outline = dot_outline_color, width = dot_line_width)
                    starting_x -= round(inches_between_dots*2550/8.5)

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
                #Otherwise, the headings on left pages are centered, with 3300/4 pixels being the
                #central "x" pixel on even pages.
                else:
                    blank_canvas_editable.text((3300/4, heading_top_margin_y_pixel),
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
                #Here the centered position on right pages is 3300*0.75 pixels (three quarters of
                #the total pixel width of the canvas).
                else:
                    blank_canvas_editable.text((3300*0.75, heading_top_margin_y_pixel),
                    heading_text_right, fill=heading_text_color, font=heading_font, anchor="ms")
        #Similar to above, except that the headings are only written on the left hand pages, provided
        #that all of the TOC pages have been included, or that the next TOC page is odd numbered.
        elif (heading_text_left != None and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 != 0))):
            if heading_corner == True:
                blank_canvas_editable.text((left_margin_x_pixel, heading_top_margin_y_pixel),
                heading_text_left, fill=heading_text_color, font=heading_font, anchor="ls")
            else:
                blank_canvas_editable.text((3300/4, heading_top_margin_y_pixel),
                heading_text_left, fill=heading_text_color, font=heading_font, anchor="ms")

        #Similar to above, except that the headings are only written on the right hand pages, provided
        #that all of the TOC pages have been included, or that the next TOC page is even numbered.
        elif (heading_text_right != None and
        (TOC_pages_list == [] or (TOC_pages_list != [] and TOC_pages_list[0]%2 == 0))):
            if heading_corner == True:
                blank_canvas_editable.text((right_margin_x_pixel, heading_top_margin_y_pixel),
                heading_text_right, fill=heading_text_color, font=heading_font, anchor="rs")
            else:
                blank_canvas_editable.text((3300*0.75, heading_top_margin_y_pixel),
                heading_text_right, fill=heading_text_color, font=heading_font, anchor="ms")

        #The following "if" and "elif" statements deal with page numbering either on both pages
        #("if" statement), on left pages only (first "elif" statement) or only on right pages
        #(second "elif" statement). The user could also choose not to write page numbers, by not
        #passing in any of the following arguments: "page_numbers", "page_numbers_left" or
        #"page_numbers_right". The page numbers are written with left or right middle text
        #anchoring ("lm" or "rm", respectively), in order to simplify the automatic vertical
        #centering of the page numbers in the available space in-between the last horizontal
        #line and the bottom of the page.
        if page_numbers != None and page_numbers_left == None and page_numbers_right == None:
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
        elif page_numbers_left != None and page_numbers == None and page_numbers_right == None:
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
        elif page_numbers_right != None and page_numbers == None and page_numbers_left == None:
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

        #If the list of table of contents pages ("TOC_pages_list")
        #isn't empty, the first page (that was just included in the
        #current "blank_canvas_editable") is removed from the list.
        if TOC_pages_list != []:
            TOC_pages_list.pop(0)

        if no_merging == True:
            blank_canvas.save(title + " (page " + str(current_page) + ").pdf", quality=100, resolution=300)
        elif no_merging == False and current_page == 1:
            blank_canvas.save(title + " (notebook pages).pdf", quality=100, resolution=300)
        elif no_merging == False and current_page > 1:
            blank_canvas.save(title + " (notebook pages).pdf", append=True, quality=100, resolution=300)
        current_page += 1

    print("\nYour notebook has been created successfully! Here are the colors used for the boxes and text of the cover:")
    print("Cover boxes color: " + cover_box_color)
    print("Cover text color: " + cover_text_color)

#If the user hasn't provided a title, author and valid file name,
#the following error message will be displayed on screen.
else:
    print("\nPlease provide the title and number of pages of the notebook as additional " +
    "arguments (with a space in-between each argument) when running the code. Also, " +
    "add the number of pages and thickness of a ream of 500 pages (in inches) when running " +
    "the code, so that the spine dimensions may be determined accordingly.\n")

    print('For example: python3 printanotebook.py "title:Skeches and Poetry" '
    + '"author:Your Name Here" "number_of_pages:192" "inches_per_ream_500_pages:2"')
