# HerbaLLM
Training Large Language Model for Herbal Medicine From Scratch


1. Data Collection
   The data collection involves everything in data_collector directory and some files in the config directory, namely collectors.yaml and settings.yaml.
   The collectors.yaml contains information about the source (where to get the data) and basic information on how to parse and store the data, such as how to parse the data, what data to take, where to store and what key to use.
   The settings.yaml contains information about the database
   The data_collector has three folders:
   - collectors: Where specific collection class to be defined.  The class name has the format of the stripped url postfixed by "Collector.py".  The stripped string is all characters and letters between the "//" and "?" exclusive.  For example, if the url is "https://tcmbank.cn/Download" then the string is tcmbankcnDownload, and the class/filename would be tcmbankcnDownloadCollector.
   - parsers: Where specific parsers to be defined.  For example, parser for excel files.  Similar to collectors, the specific parser name follows the same logic, which is the stripped url appended by "Parser.py"
   - storage: Where the class to save data into database is defined.  There is no specifc storage class here.  The data coming out of the parser(s) has the same format. Hence no specific storage class is needed.  On the reverse, data read from the database and fed into the parser(s) will be converted on the output.  The parser should have all the information to do the translation.
2. 