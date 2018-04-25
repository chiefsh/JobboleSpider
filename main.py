from scrapy.cmdline import execute
import sys,os



if __name__=="__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','jobbole'])