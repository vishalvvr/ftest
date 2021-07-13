import subprocess
import sys
import json
import unittest
import json

class fonttest(unittest.TestCase):
    
    font_config_dir = "/etc/fonts/conf.d/"
    config = None

    @classmethod
    def setUpClass(cls):
        # load config file
        with open("./config.json") as fobj:
            cls.config = json.load(fobj)

        # get filepaths for the given font
        font_filepath, err = cls.execute_command("fc-list | grep {0} | cut -d':' -f1".format(cls.config['fontname']))
        font_filepath = font_filepath.split("\n")
        cls.font_file_list = list(filter(None, font_filepath))
        
        with open('mylog.txt', 'w') as fp:
            pass
        
        if err:
            sys.stdout.write(err)
            sys.exit(1)


    @staticmethod
    def execute_command(command_str):
        '''
        Execute cli commands and return output
        '''
        out, err = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return (str(out, 'utf-8'), str(err, 'utf-8'))


    def test_font_conf(self):
        '''
        This function will get all conf file path for given font
        '''
        # get list of font conf files 
        font_conflist, err = fonttest.execute_command("fc-conflist | grep {0}".format(self.config["fontname"]))
        if not err and font_conflist: 
            # clean data
            font_conflist = font_conflist.split("\n")
            font_conflist = [x.split(" ")[1].replace(":","").replace(self.font_config_dir,"") for x in font_conflist[:-2]]
            
            if set(self.config['font_conf_list']).issubset(set(font_conflist)):
                self.assertLessEqual(len(self.config['font_conf_list']), len(font_conflist))
        else:
            sys.stdout.write(err)
            sys.exit(1)


    def test_font_family(self):
        '''
        This function will excute fc-list and check fontfamily  
        '''
        font_family, err = self.execute_command("fc-list | grep {0} | cut -d':' -f2".format(self.config['fontname'])) 
        
        # if font file exist create a font family list
        if not err and font_family:
            font_family_list = font_family.split("\n")
            font_family_list = list(filter(None, font_family_list))
            font_family_list = set([font.strip() for font in font_family_list])
            if set(self.config['font_family_list']).issubset(font_family_list):
                self.assertLessEqual(len(self.config['font_family_list']), len(font_family))
        else:
            sys.stdout.write(err)
            sys.exit(1)
        

    def test_lang_coverage(self):
        '''
        This function will check language coverage as specifed in parameter with fontfiles 
        '''
        for font_file_path in self.font_file_list:
            # get all lang covarage by font    
            font_langlist, err = self.execute_command("fc-query -f 'lang: %{lang}' "+font_file_path) 
            PendingDeprecationWarning
            if not err and font_langlist: 
                font_langlist = font_langlist.split("|")
                font_langlist[0] = font_langlist[0].replace("lang: ","")
                if set(self.config['lang']).issubset(set(font_langlist)):
                    self.assertLessEqual(len(self.config['lang']), len(font_langlist))
            else:
                sys.stdout.write(err)
                sys.exit(1)


if __name__ == "__main__":    
    unittest.main()