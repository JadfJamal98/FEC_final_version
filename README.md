# Financial-Econometrics-Project

1. Topic
Sentiment analysis on 10-k reports and proxy statements to study how companies' awareness on ESG matters changed over time.

2. Files
The project contains quite some files. Overall, we tried to keep as much of the data as possible in the same directory to avoid losing oversight. The directory is set up as follows:

    2.1 Excel Data
    We have three files in Excel. The LoughranMcDonald files contains the word list from the paper of 'T. Loughran, B. Mcdonald: “When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks” (February 2011)'. The ESG_word_list.excel 
    and finally the SP500_ESG.excel has all the scores that we initially obtained via the UNIL Bloomberg terminal access kindly provided. Unfortunately, we assumed that scores also are actually from bloomberg. Therefore in the code often the term 'bloomberg', 'bloomberg_score' or similar is used. However, there are from Refinitiv, so this might cause confusion, we apologize for this.

    2.2 Company data
    The company data was downloaded via the sec_edgar_downloader API. It should be noted first, that the API is not perfect and, among others, sometimes did not allow download due to permission errors (this was fixed during the project so we re-downloaded large amounts of data) and some companies had multiple filings. Afterall, we have the folders 'Top 40' which contains the initial 40 companies that we downloaded. 'score_files_bow' and 'score_files_word2vec' contain the computed scores put in text files for bag-of-words and word2vec, respectively. 

    2.3 Python files
    The following python files are contained in the directory: Bag_of_Words.py, Word2Vec.py Create_Plots.py, Create_ScoreFiles.py, Download.py, Refinitiv_Import.py, Wordlist_Import.py, Text_Writer.py

3. How to run the files
In case the could is executed, first one should make sure that no files from 2.2 company files are in the directory. Although we tried to implement check-points such that it is checked whether a file exists, dealing with around 20 GB of data always makes it difficult to consider all possible cases. Then, first the Download.py should be executed (not recommended, takes extremely long), which will get all the company files from the sec edgar database. Next, the Text_Writer.py file creates text files from the html files that can be used and contains the tokenization function needed for the bag-of-words and word2vec. Next, the Create_ScoreFiles.py can be executed such that the tokenized text files are used to compute scores for bag-ofw-words and word2vec and also saves then in text files (not recommended as it takes extremely long). Finally, with the Create_Plots.py the scores are plotted or alternatively saved in the desired directory.



