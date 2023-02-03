# PrintANotebook
PrintANotebook lets you create your own notebooks, complete with page numbering and your favorite designs!

![PrintANotebook Thumbnail](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Daily%20Planner%20Cover.jpg)
<h3 align="center">PrintANotebook</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/LICENSE)
  [![GitHub issues](https://img.shields.io/github/issues/LPBeaulieu/Book-Generator-PrintABook)](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook)
  [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
  [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
  [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
  
</div>

---

<p align="left"> <b>PrintANotebook</b> is a tool allowing you to create your own personalized notebooks, complete with page numbering, personalized headings, and your choice of any combination of either blank pages, ruled lines, dot grid or graph pages. 
You can even select your own designs to create some nifty planners! <b>PrintANotebook</b> also lets you personalize the cover with your favorite graphic design, and the text of your choosing on the front cover and spine of the notebook!</p>
<br> 


## 📝 Table of Contents
- [Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)
<br><br><br>
## ⛓️ Limitations <a name = "limitations"></a>
The code for cover image generation was optimized on notebooks having at least 100 pages (of 20 lb bond paper). However, I typically generate notebooks having a total of around 200 pages, and print them on 28 lb bond perforated paper from the Perforated Paper company, which works wonderfully with my homemade biodegradable phycocyanin fountain pen ink (https://www.linkedin.com/feed/update/urn:li:activity:7027151841851265024/), which lends itself very nicely to writing on both sides of the sheet of paper with minimal bleeding and ghosting. Moreover, the perforations of this paper are quite precise, with only slight spine sanding being required in order to craft professional looking notebooks. While I’m not affiliated with this company in any way, I find that their paper is very smooth and gives good results when binding books. They also sell some 24 lb bond perforated paper in cream color. Check them out at www.perforatedpaper.com!

![Figure 1](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Phycocyanin%20Ink%20Review%20Github%20Image.jpg)<hr> <b>Figure 1.</b> Here is my review of the 28 lb perforated paper from the Perforated Paper company with the blue spirulina (phycocyanin) fountain pen ink that I have formulated! The ink is more saturated on the actual sheet (a few shades darker, actually), but this gives a good general idea of how it behaves on this paper. It shows some very modest water resistance, but care should still be taken to avoid exposing the pages to moisture.
<br><br><br>


## 🏁 Getting Started <a name = "getting_started"></a>

The following instructions will be provided in great detail, as they are intended for a broad audience and will allow to run a copy of <b>PrintANotebook</b> on a local computer. You can also view the YouTube version of the instructions at the following link: <b>The Youtube link will be added once the video has been uploaded.</b>
   
The instructions below are for Windows operating systems, but the code should run nicely on Linux and Mac-OS as well.

<b>Step 1</b>- Hold the "Shift" key while right-clicking in your working folder and select "Open PowerShell window here" to access the PowerShell in your working folder. Then, install <b>NumPy</b> and <b>Pillow</b> (Required Python modules to generate the cover image) by entering the following command:
```
py -m pip install NumPy --upgrade Pillow
```

<b>Step 2</b>- You're now ready to use <b>PrintANotebook</b>! 🎉
<br><br><br>

## 🎈 Usage <a name="usage"></a>

<b>Step 1</b> In the <b>"Cover font TTF file" folder</b> within your working folder, you need to have exactly <b>one True Type Font file (.ttf) for the cover text font</b>. When you set up your system, the "Baskerville" TTF file will be included in this folder by default. Similarly, <b>another TTF font file needs to be included in the "Header and footer font TTF file" subfolder for the headings and page numbers</b> (the "Baskerville" TTF file is also included in this folder by default). 
 
<b>Step 2</b>- <b>A JPEG image for the cover illustration</b> in legal paper size and landscape format (4200 pixels in width and 2550 pixels in height) <b>needs to be included in the working folder. Its file name must start with "Cover"</b>, so that the code may recognize it. You can find instructions on preparing such background images by viewing the following YouTube video (https://www.youtube.com/watch?v=xPY7dMcKfVY). A public domain background image by Karen Arnold is provided in the working folder, which you could replace with your own preferred image.

<b>Step 3</b>- With every file in its right place, it is now time to run the code! Start by holding the "Shift" key while right-clicking in your working folder, then select "Open PowerShell window here" to access the PowerShell in your working folder and enter the commands described below. The following figures will explain which arguments should be added after the Python code call in order to generate different types of notebooks. In all cases, you will need to <b>pass in the width or thickness of a ream of 500 pages of the paper that you will be printing on, in inches and decimal form, but without units, after the "inches_per_ream_500_pages:" argument</b>, which will allow the code to properly size the spine of the cover. For measurements in centimeters, use "cm_per_ream_500_pages:" instead. Although the different arguments delimited by double quotes may be provided in any order, they must be separated from one another by a space, as in the examples below.

![Figure 2](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages.jpg)<hr> <b>Figure 2.</b> For a notebook with dotted pages and page numbering on both left and right pages, the following command would be entered: 
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" 
```
<br><br>


![Figure 3](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%20with%20same%20headings%20on%20both%20pages.jpg)<hr> <b>Figure 3.</b> In order to add the same heading to both left and right pages, you would add the heading text, preceded by the "heading_text:" argument:
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" "heading_text:Your Heading Text Here"
```
<br><br>

![Figure 4](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%20with%20same%20headings%20on%20both%20pages%2C%20in%20corners.jpg)<hr> <b>Figure 4.</b> Should you like the headings to be in the outer corners instead of being centered, you would pass in the additional argument "heading_corners":
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" "heading_text:Your Heading Text Here" "heading_corners"
```
<br><br>

![Figure 5](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%20with%20different%20headings%20on%20both%20pages.jpg)<hr>
<b>Figure 5.</b> In order to include different headings on left and right pages, enter the corresponding text as additional arguments, preceded by "heading_text_left:" and "heading_text_right:", respectively:
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" "heading_text_left:Left Page Heading" "heading_text_right:Right Page Heading"
```
<br><br>


![Figure 6](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%20with%20heading%20on%20right%20pages.jpg)<hr>
<b>Figure 6.</b> Should you only want headings on right-hand pages, enter the corresponding text as a single additional argument, preceded by "heading_text_right:". The same is true for headings only appearing on left-hand pages when passing in the "heading_text_left:" argument alone.
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" "heading_text_right:Right Page Heading"
```
<br><br>


![Figure 7](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%2C%20page%20numbers%20only%20on%20right%20pages.jpg)<hr>
<b>Figure 7.</b> Similarly, should you want page numbers only on right-hand pages (here framed in orange), enter the "page_numbers_right" argument instead of "page_numbers". The same could be done for page numbering only on left-hand pages by passing in the "page_numbers_left" argument instead of "page_numbers".
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers_right" "inches_per_ream_500_pages:2.63" "dot_grid" 
```
<br><br>

![Figure 8](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%20with%20same%20headings%20on%20both%20pages%2C%20different%20font%20size%20and%20color.jpg)<hr>
<b>Figure 8.</b> The default font size (75 pixels) and font color ("LightSlateGrey") of the headings may be changed by adding the desired font size after the "heading_font_size:" (without units) and color after the "heading_text_color:" (either RGB code or HTML color name) arguments, respectively. The same may be done for the page numbers, by specifying the desired values after the following arguments: "page_numbers_font_size:" (60 pixels by default) and "page_numbers_text_color:" ("LightSteelBlue" by default).
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" "heading_text:Your Heading Text Here" "heading_font_size:90" "heading_text_color:Teal" "page_numbers_font_size:70" "page_numbers_text_color:SeaGreen"
```
<br><br>

![Figure 9](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20both%20pages%20with%20same%20headings%20on%20both%20pages%2C%20different%20font%20size%2C%20dot%20diameter%2C%20spacing%20and%20color.jpg)<hr>
<b>Figure 9.</b> The default dot spacing (0.2 inch), diameter (5 pixels) and line width (1 pixel) may also be changed to your preferred settings, by adding them in sequence after the "dot_grid:" argument, with colon dividers in-between. Moreover, the dot fill color and dot outline colors (both being "LightSlateGrey" by default) may be changed by adding the HTML color name or RGB code after the "dot_fill_color:" and "dot_outline_color:" arguments, respectively.
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid:0.25:10:0" "heading_text:Your Heading Text Here" "heading_font_size:90" "heading_text_color:Teal" "page_numbers_font_size:70" "page_numbers_text_color:SeaGreen" "dot_fill_color:(143, 188, 143)"
```
<br><br>
 
![Figure 10](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/TOC%20with%20different%20line%20spacing%2C%20line%20thickness%2C%20line%20color%2C%20font%20size%2C%20font%20color%20and%20text.jpg)<hr>
<b>Figure 10.</b> In order to specify a different number of pages than the default of 8 and another line spacing for the Table of Contents (TOC), simply pass in both preferred settings in sequence after the "toc_pages_spacing:" argument, with colon separators in-between, and the line spacing expressed in inches and in decimal form. In order to alter the line width of the TOC ruled lines (5 pixels by default), enter the desired value after the "toc_line_width:" argument. To change the TOC heading font size, text color and text itself, add the desired parameters after the "toc_heading_font_size:" (75 pixels by default), "toc_heading_text_color:" ("LightSlateGrey" by default) and "toc_heading_text:" ("Contents" by default), respectively. Similarly, the "Pages" and "Subject" subheadings font sizes (both 60 pixels by default), text colors (each written in "LightSlateGrey" color by default) and text may be altered by entering your parameters of choice after the "toc_pages_font_size:" and "toc_subject_font_size:", "toc_pages_text_color:" and "toc_subject_text_color:" as well as "toc_pages_text:" and "toc_subject_text:" arguments, respectively. Finally, you may opt to remove the TOC altogether by specifying zero as the number of pages ("toc_pages_spacing:0"). Please keep in mind that the number of TOC pages needs to be an even number to ensure that the first of the numbered notebook pages lands on a right-hand page. For this reason, the code will automatically round up any inputted uneven pages to the next even numbers. Also, to make sure that the PDF document may be easily printed in duplex mode, additional notebook pages will automatically be added by the code if the total amount of pages (including the TOC) is not a multiple of four. 
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "dot_grid" "heading_text:Your Heading Text Here" "toc_pages_spacing:6:0.3" "toc_line_width:3" "toc_heading_text:Index" "toc_heading_font_size:90" "toc_heading_text_color:Teal" "toc_pages_text:Page" "toc_pages_font_size:75" "toc_pages_text_color:SeaGreen" "toc_subject_text:Topic" "toc_subject_font_size:75" "toc_subject_text_color:SeaGreen" "toc_line_color:(143, 188, 143)"
```
<br><br>


![Figure 11](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20right%20pages%2C%20blank%20pages%20on%20left%20pages.jpg)<hr>
<b>Figure 11.</b> Should you like to have the dot grid pattern only on the right pages, and blank pages on left-hand pages, you would need to pass in the argument "dot_grid_right" instead of "dot_grid". The reverse outcome would require you to enter the "dot_grid_left" argument instead of "dot_grid".
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers_right" "inches_per_ream_500_pages:2.63" "dot_grid_right"
```
<br><br>


![Figure 12](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Dot%20grid%20on%20right%20pages%2C%20college%20ruled%20pages%20on%20left%20pages%2C%20thinner%20lines%20and%20different%20colored%20lines.jpg)<hr>
<b>Figure 12.</b> In order to have college ruled lined pages (9/32 inch line spacing) on the left alternating with dot grids on right-hand pages, you would need to pass in the arguments "college_ruled_left" and "dot_grid_right". The inverse result could also be acheived by entering "college_ruled_right" and "dot_grid_left", and it would also be possible to have college ruled lines on both pages by only passing in "college_ruled". The lower margins will be adjusted automatically such that the last horizontal dot grid line matches up as well as possible with the last ruled line on the page.
Finally, the default line width of 5 px and "Gainsboro" line color could be changed by providing the selected parameters after the "line_width:" and "line_color:" arguments, respectively, where either the HTML color name or RGB code may be specified for the line color.
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "college_ruled_left" "dot_grid_right" "line_width:4" "line_color:BurlyWood"
```
<br><br>


![Figure 13](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Custom%20ruled%20lines%20on%20left%20pages%20and%20dot%20grid%20on%20right%20pages%2C%20with%20same%20titles%20and%20page%20numbers%20on%20both%20pages.jpg)<hr>
<b>Figure 13.</b> For wide ruled pages (11/32 inch line spacing), the "wide_ruled" argument would need to be passed in. Furthermore, ruled pages with custom line spacing may also be generated by entering "custom_ruled:" followed by the line spacing in inches and in decimal format. Of note, unlike dot grid formats where the distances in-between dots are measured relative to the dot centers, line spacing is calculated as the actual space in-between the lines (excluding the pixels of the lines themselves).
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "heading_text:Your Heading Text Here" "custom_ruled_left:0.2" "dot_grid_right:0.2"
```
<br><br>

![Figure 14](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Graph%20paper%20left%20(5-5-2)%2C%20line%20width%205%20px%2C%20%20dot%20grid%20right.jpg)<hr>
<b>Figure 14.</b> Should you want to have dot grids on right-hand pages alternating with graph paper on the left pages, you would need to pass in the arguments "dot_grid_right" and "graph_paper_left:". The latter argument ends with a colon, which is then followed by the number of squares per inch, a colon divider, the number of squares in-between every thicker line, another colon, and finally the width ratio between the thicker line and the regular line having a default width of 5 px. The reverse could also be done by entering "dot_grid_left" as well as "graph_paper_right:", with the same information as above. It would also be possible to have graph paper on both pages by only passing "graph_paper:", with the same abovementioned parameters". Once again, the lower margins will be adjusted automatically such that the last horizontal dot grid line matches up as well as possible with the horizontal graph paper line on the page. 
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "heading_text:Your Heading Text Here" "graph_paper_left:5:5:2" "dot_grid_right"
```
<br><br>

![Figure 15](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Graph%20paper%20left%20(5-5-2)%2C%20line%20width%203%20px%2C%20blue%20lines%2C%20%20dot%20grid%20right.jpg)<hr>
<b>Figure 15.</b> The default graph paper line width of 5 px and "Gainsboro" line color could be changed by providing the selected parameters after the "graph_line_width:" and "graph_line_color:" arguments, respectively, where either the HTML color name or RGB code may be specified for the graph line color.
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "heading_text:Your Heading Text Here" "graph_paper_left:5:5:2" "graph_line_width:3" "graph_line_color:rgb(172, 231, 248)" "dot_grid_right"
```
<br><br>

![Figure 16](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Graph%20paper%20left%20(5)%2C%20line%20width%203%20px%2C%20blue%20lines%2C%20%20dot%20grid%20right%2C%20altered%20margins.jpg)<hr>
<b>Figure 16.</b> For simple graph paper without bold lines, simply omit the two last parameters after the number of squares per inch. Besides that, you might wish to extend the lower border (0.6 inch by default) in order to include more lines on the page. This could be done by passing in the number of inches (in decimal form, without units) from the bottom of the page where the lowest line could be drawn, after the "bottom_margin:" argument. You could also alter the default left page left margin and right page right margin of 0.25 inch, as well as the top margin of 0.95 inch, by entering the desired measurements after the "left_margin:", "right_margin:" and "top_margin:" arguments, respectively.
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "heading_text:Your Heading Text Here" "graph_paper_left:5" "graph_line_width:3" "graph_line_color:rgb(172, 231, 248)" "dot_grid_right" "bottom_margin:0.55" "left_margin:0.4" "right_margin:0.4"
```
<br><br>

![Figure 17](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Graph%20paper%20left%20(5)%2C%20line%20width%203%20px%2C%20blue%20lines%2C%20%20college%20ruled%20right%2C%20larger%20header%20and%20footer%2C%20altered%20margins.jpg)<hr> 
<b>Figure 17.</b> Other page combinations can be generated, such as graph paper and blank pages or graph paper and ruled lines, similarly to what was done above. It is also possible to alter the header and footer margins (which are by default 0.6 inch from the top and automatically vertically centered in the bottom of the page, respectively), by providing the selected measurements after the corresponding arguments "heading_top_margin:" and "page_numbers_bottom_margin:". Note that the horizontal alignment of the headings may be shifted through the inclusion of spaces in the arguments that are passed into the Python code. 
<br>
```
py -m printanotebook.py "title:Your Title Here" "author:Your Name Here" "spine_text:Your Spine Text Here" "number_of_pages:192" "page_numbers" "inches_per_ream_500_pages:2.63" "heading_text_left:Sketch No.:        " "heading_text_right:Date:                " "graph_paper_left:5" "graph_line_width:3" "graph_line_color:rgb(172, 231, 248)" "college_ruled_right" "top_margin:1" "bottom_margin:0.5" "heading_top_margin:0.65" "page_numbers_bottom_margin:8.1" "heading_font_size:100" "page_numbers_font_size:70"
```
<br><br>

![Figure 18](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Graph%20paper%20left%20(5)%2C%20line%20width%203%20px%2C%20blue%20lines%2C%20%20college%20ruled%20right%2C%20larger%20header%20and%20footer%2C%20altered%20margins%2C%20different%20font.jpg)<hr> 
<b>Figure 18.</b> Different fonts for the headings and page numbers can be used simply by changing the True Font File (.ttf) within the "Header and footer font TTF file" folder. No further arguments are required when running the Python code. The image above illustrates this, as the same arguments as those of Figure 16 were passed in, when running the Python code with the satisfy font (https://fonts.google.com/specimen/Satisfy?query=satisfy).
<br><br><br>

![Figure 19](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Daily%20Planner.jpg)<hr> 
<b>Figure 19.</b> Custom Designs may also be incorporated in your notebook, such as this daily planner journal (which is also featured in the thumbnail image of this Github page). Notice in the Python call below that the TOC headings and subheadings have been removed, leaving behind regular dot grid pages without page numbers. You could use these to write your bullet journal key and index, as well as monthly spreads, before the start of the daily planner numbered pages themselves. Should you want to have daily planner pages both on the left and right-hand pages, you would then pass in both "custom_template_left_page" and "custom_template_right_page". Please refer to the PDF document entitled "PrintANotebook - Custom Design Generation.pdf" for more on how to create and export custom designs in LibreOffice Draw. 
<br>
```
py -m printanotebook.py "title:Winter 2023 Daily Planners" "author:Louis-Philippe Bonhomme-Beaulieu" "number_of_pages:180" "page_numbers_right" "inches_per_ream_500_pages:2.63" "heading_text_left:Daily Planner" "custom_template_left_page" "dot_grid_right" "toc_pages_spacing:8" "toc_subject_text:" "toc_pages_text:" "toc_heading_text:" "top_margin:0.8" "bottom_margin:0.5" "right_margin:0.5" "cover_box_color:rgb(150, 63, 92)" "cover_text_color:White"
```
<br><br>

<h3><b>Printing Your Notebook</b></h3>
<p>In order to print the notebook sheets, each consisting of two pages per side of a sheet of 8 1/2" by 11" paper, simply print them in landscape duplex mode with the "flip on short side" option. It should be noted that the page numbering is already in booklet format, so as to facilitate the printing process and book assembly.</p>

<p>For <b>instructions on how to generate and print the notebook covers</b>, I would direct you to my other Github repository PrintABook, which lets you generate books in printable format from Project Gutenberg novel text files. The code is the same when it comes to making the book covers, so please refer to Figure 3 of the PrintABook Readme page for the list of arguments pertaining to cover generation, and to Step 8 onwards of the "Usage" section for more on how to print the notebook covers. Also, please refer to this Youtube instructions video on how to prepare your own JPEG images for cover creation: https://www.youtube.com/watch?v=xPY7dMcKfVY.</b>
<br><br>

![Figure 20](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/Budgie%20Journal.jpg)<hr> 
<b>Figure 20.</b> Other custom designs may also be included in your notebook, such as this weekly spread template that is included in the pet journal that I have created for my budgies. In this case the Python script was only used to generate the journal cover, as there were too many custom journal sections for the code to handle them nicely. It just goes to show that even if you were only to use the code to generate customized notebook covers, it would still be quite useful! You can find all of my custom designs in my Google Drive at the following link: (https://drive.google.com/drive/folders/1r1BLipQujz22kFHMnLVYw_qzv5OBq9cv?usp=sharing).
<br><br><br>

![Figure 21](https://github.com/LPBeaulieu/Notebook-Maker-PrintANotebook/blob/main/Github%20Page%20Images/PrintANotebook%20Results.jpg)<hr> 
<b>Figure 21.</b> Here is what the finished bound notebooks using 28 lb perforated paper from www.perforatedpaper.com look like!
<br><br><br>

<b>Well there you have it!</b> You can now generate your own customized notebooks and print the notebook pages in your favorite color! Now dollop some glue onto the spine, slap on the cover, let it dry under some books and you'll soon be able to lay down your most treasured thoughts in your personalized notebook! 🎉📖

 
## ✍️ Authors <a name = "author"></a>
- 👋 Hi, I’m Louis-Philippe!
- 👀 I’m interested in natural language processing (NLP) and anything to do with words, really! 📝
- 🌱 I’m currently reading about deep learning (and reviewing the underlying math involved in coding such applications 🧮😕)
- 📫 How to reach me: By e-mail! louis.philippe.bonhomme.beaulieu.1@gmail.com 💻


## 🎉 Acknowledgments <a name = "acknowledgments"></a>
- <b>Shout out to the talented Rajesh Misra for the gorgeous illustration</b> featured on the cover (https://www.publicdomainpictures.net/en/view-image.php?image=214080&picture=floral-pattern-background-843) 
- Hat tip to [@kylelobo](https://github.com/kylelobo) for the GitHub README template!



<!---
LPBeaulieu/LPBeaulieu is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
