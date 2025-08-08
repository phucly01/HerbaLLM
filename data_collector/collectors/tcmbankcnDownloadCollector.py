from requests_html import HTMLSession
import re 
import os
import json
from data_collector.collectors.Collector import Collector
from data_collector.parsers.Parser import Parser

class tcmbankcnDownloadCollector(Collector):
    
    
    def collect(self, url:str, user:str=None, passwd:str=None) -> list: 
        if url.startswith('file:///'):
            url = url[8:]
        if not hasattr(self, 'parser'):
            self.parser = self.parser_class(self.config, self.storage_class)
        if os.path.exists(url):
            return self.__collect_file(url)
        else:
            return self.__collect_url(url, user, passwd)


    def __collect_file(self, url):
        filename = re.search(rf'{self.config['key-map-regex']}', url)
        filename = filename.group(1) if filename else url[url.rindex('/')+1:]
        if not Parser.get_data_parser(category_map=self.config['parser']['categories'], filename=filename):
            print(f'No parser found for {filename}. Skipping ...')
            return False
        with open(url, 'rb') as file:
            data = file.read()
            # filename = url[url.rindex('/')+1:]
            print(self.config)
            return self.parser.parse(filename, data) 
            
        return False
    
    def __collect_url(self, url, user:str=None, passwd:str=None):
        session = HTMLSession(verify=False)
        authurl = url
        if user and passwd:
            authurl = f'{user}@{url}'
        resp = session.get(authurl, verify=False)
        resp.html.render()
        if resp.status_code == 200:
            html = resp.html.html.replace('\n','')
            found = re.search(r'tableData: \[(.*),\],.*', html)
            if found:
                tabledata = re.sub(r',[ ]+}', '}', re.sub(r'[ ]*([a-zA-Z]+): ', r'"\1": ', f'[{found.group(1)}]'.replace("'", "\"")))
                print(tabledata)
                tablejson = json.loads(tabledata)
                for row in tablejson:
                    filename = re.search(rf'{self.config['key-map-regex']}', row['link'])
                    filename = filename.group(1) if filename else row['link'][row['link'].rindex('/')+1:]
                    #This is just look ahead to avoid downloading something that won't be processed
                    if not Parser.get_data_parser(category_map=self.config['parser']['categories'], filename=filename):
                        print(f'No parser found for {filename}. Skipping ...')
                        continue
                    print(f'#### Collecting {row['link']}')
                    download = session.get(row['link'])
                    if download.status_code == 200:
                        # targetfile = f"/tmp/{filename}"
                        # with open(targetfile, 'wb') as file:
                        #     for block in download.iter_content(chunk_size=8192):
                        #         if block: 
                        #             file.write(block) 
                        self.parser.parse(filename, download.content)
                    download.close()
                return True
        resp.close()
        return False
                            
                
            