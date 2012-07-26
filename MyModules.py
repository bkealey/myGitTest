from lxml import html
import MyModules

#trying to see what it is like to edit on github

def parse_isys_output(path_to_csv,directory_details):
    """
Opens a file created using the directEDGAR Add-In and creates
a list of dictionaries the list has one entry for each row in the CSV file.
Each dictionary has the following keys

cik - Central Index Key
date_details - the dates related to the filing in the form
               RYYYYMMDD-CYYYYMMDD-F##
file-type - the file extension that identifies the type of filethat has
file-path - the fully conformed file path for the name
            required inputs are
path_to_csv - the full path and name of the csv file created
              using the Add-In
directory_details - the path from the drive root to the year folder
                    where the original filings were found
            example c:\\directEDGAR_Accounting\\10KMASTER\\Y2009-Y2012\\
            change the MASTER and Y part of the file name to match the index

    """
    isys_results=open(path_to_csv).readlines()
    partial_paths_list=[]
    #below we are starting with the second row because the first row has the column
    # headings 
    start=1
    for item in isys_results[start:]:
        partial_path=item.split(',')[0]
        partial_paths_list.append(partial_path)
    filing_details=[]
    for partial_path in partial_paths_list:
        temp_dict={}
        split_partial_path=partial_path.split('\\')
        temp_dict['cik']=split_partial_path[1]
        temp_dict['date_details']=split_partial_path[2]
        temp_dict['file_type']=split_partial_path[3].split('.')[-1]
        temp_dict['file_path']=directory_details+partial_path
        filing_details.append(temp_dict)
    return filing_details

def save_dE_string(temp_dict,string,out_directory):

    """
Save a string with a name based on the filing directory which was the
source for the input in your program

temp_dict is assumed to be similar to the dictionary created using
the function MyModules.parse_isys_output this will be used to help
construct the file name the string is what needs to be saved

If it is not the dictionary created by MyModules.parse_isys_output the
dictionary used must have at minimum the following keys

cik - Central Index Key
date_details - the dates related to the filing in the form
               RYYYYMMDD-CYYYYMMDD-F##
file-type - the file extension that identifies the type of filethat has

string - a string that was created by processing something

out_directory - the full path to the directory where the files
                are to be saved
The file names will be in the form
    CIK-RYYYYMMDD-CYYYYMMDD-F##-0.ext where ext is the extension
"""


    file_name = (out_directory + '\\' + temp_dict['cik'] + '-' + 
                temp_dict['date_details'] + '-0.' + temp_dict['file_type'])
    file_handle=open(file_name,'w')
    file_handle.write(string)
    file_handle.close()
    return

def create_string(element_list):
    """
uses lxml.html.tostring to converst a list of elements discovered using
lxml.html.fromstring back to a string representation so that the results
can be saved to disk

element_list - list of html elements

    """
   
    outstring = '<html><body>'
    
    for element in element_list:
        outstring += html.tostring(element)
    outstring+='</body></html>'
    return outstring

def get_slice(the_tree,begin_element,end_element):
    """
returns the section of the_tree from the begin_element to the
end_element. Since some elements are nested duplicates those are
eliminated by testing to see if any ancestors of the element
being tested are already present elements that have an ancestor
present would duplicate the information contiained in the ancestor so
they are not used in constructing the final list of elements

the_tree - a tree created using lxml.html.fromstring
begin_element - the element that defines the beginning of the section
                of the tree that needs to be isolated
end-element - the element that defines the end of the section

    """
    all_elements=[e for e in the_tree.iter()]
    begin_index=all_elements.index(begin_element)
    end_index=all_elements.index(end_element)+1
    uniq_elements=[]
    for element in all_elements[begin_index:end_index]:
        tempset=set(uniq_elements)
        ancestors=set([e for e in element.iterancestors()])
        if len (tempset & ancestors) == 0:
            uniq_elements.append(element)
    return uniq_elements


def check_bold_font(the_tree, some_lc_words):
    """
Inspect a tree to determine if it has font tags if so isolate
them. Examine each font tag to determine if it the specific
phrase in their text_content().  As elements that have the specific phrase
are found the element is checked to see if it has a bold attribute.  The
case found is returned.  (Element must be font, have words and bold attribute)
Nothing is returned if element not found.

Paramteres

some_tree - a tree created from a string using lxml.html.fromstring
some_lc_words - a phrase in lower case

    """
    font_elements=[e for e in the_tree.iter(tag='font')]
    if len(font_elements)==0:
        return
    for element in font_elements:
        if some_lc_words in element.text_content().lower():
            if 'bold' in element.values()[0]:
                return element
    return


def check_bold(some_tree,some_lc_words):
    """
Inspect a tree for bold tags if present isolate them to examine them
to find the first where the phrase some_lc_words can be found
in text_content.  Nothing is returned if it is the case that there
are no bold element or no bold element can be found that has the
phrase some_lc_words

Paramteres

some_tree - a tree created from a string using lxml.html.fromstring
some_lc_words - a phrase in lower case

    """
    bold_elements=[e for e in some_tree.iter(tag='b')]
    if len(bold_elements)==0:
        return
    for element in bold_elements:
        if some_lc_words in element.text_content().lower():
            return element
    return
