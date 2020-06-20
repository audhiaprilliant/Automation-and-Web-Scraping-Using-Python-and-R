## Web Scraping KnapSackFamily Metabolite Using selenium - Python

### Overview
The purpose of the KNApSAcK Metabolomics is to search metabolites from MS peak, molecular weight and molecular formula, and species. It consists of KNApSAcK Metabolomics Search Engine and KNApSAcK Core System. To search information about a metabolite, users should select radio button corresponding to its name, molecular formula, C_ID *(identifier in metabolites in KNApSAcK Core DB)* or *CAS_ID*, and input corresponding information and then click the “List” button. For example, a user selects radio button Metabololite, inputs “Alliin”, and clicked List button.

### Prerequisites
1. Python 3.x, of course
2. Good internet connection is recommended
3. Several python's modules
   - **pandas** for data manipulation
   - **os** provides functions for interacting with the operating system
   - **sys** provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
   - **selenium** provides a simple API to write functional/acceptance tests using Selenium WebDriver

### Steps
The program is easy to run by following steps:
1. Clone this repo
2. Open your terminal
3. Download the module dependencies by typing `pip install -r requirements.txt`
4. Modify `data_species.txt` which is the list of species we want to scrape directly
4. Type `python3 'KnapSackFamily Metabolite Activity.py' data/data_species.txt`
5. Finally, the data will be stored in your `data` directory with format `%Y-%m-%d %H:%M:%S`
