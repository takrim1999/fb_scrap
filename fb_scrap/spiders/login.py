from getpass import getpass
from scrapy import Request
from scrapy import Spider
from scrapy.http import FormRequest, request
from scrapy.utils.response import open_in_browser
global total_count
total_count = 0
class LoginSpider(Spider):
    name = 'login'
    allowed_domains = ['mbasic.facebook.com']
    start_urls = ['http://mbasic.facebook.com/login/device-based/regular/login/']

    def parse(self, response):
        data_list = response.xpath("//input/@value").extract()
        #print(data_list)
        data = {'lsd' : data_list[0] , 'jazoest' : data_list[1] , 'm_ts' : data_list[2], 'li' : data_list[3], 'try_number' : data_list[4], 'unrecognized_tries' : data_list[5], 'email': input("your email/phone:\n>"), 'pass' : getpass("your password: "), 'login' : 'Log+In'}
        return FormRequest.from_response(response = response , formdata = data, callback = self.another)
    
    def another(self, response):
        id_url = response.urljoin(response.xpath("//a/@href").extract_first())
        return Request(id_url , callback = self.msg)
                
    # def status(self,response):
        
    #     status_data_list = response.xpath("//*[@id='mbasic-composer-form']/input/@value").extract()
    #     status_data = {'fb_dtsg' : status_data_list[0], 'jazoest' : status_data_list[1], 'privacyx' : status_data_list[2], 'target' : status_data_list[3], 'c_src' : status_data_list[4], 'cwevent' : status_data_list[5], 'referrer' : status_data_list[6], 'ctype' : status_data_list[7], 'cver' : status_data_list[8], 'rst_icv' : '' , 'xc_message' : input("your status:\n>"), 'view_post' : 'Post'}        
    #     status_url = response.urljoin(response.xpath("//*[@id='mbasic-composer-form']/@action").extract_first())
        
    #     return FormRequest(status_url , formdata = status_data , callback = self.show)

    def msg(self,response):
        msg_url="/messages/?ref_component=mbasic_home_header&ref_page=%2Fwap%2Fhome.php&refid=7" 
        with open("msg.csv" , "w") as f:
                    f.write(f"name,msg_url")
        return Request(response.urljoin(msg_url) , callback = self.recipient)

    def recipient(self,response):
        #print("\n\n\n\n\n\n\n")
        # print(response.xpath('//*[@id = "objects_container"]//a'))
        global total_count
        for i in response.xpath("//*[@id = 'objects_container']//a/@href").extract():
            if "tid" in i:
                # msg_id_dict = {}
                name = response.xpath(f"//*[@href = '{i}']/text()").extract_first()
                msg_url = response.urljoin(i)
                #msg_id_dict[name]
                with open("msg.csv" , "a") as f:
                    f.write(f"\n{name},{msg_url}")
                total_count = total_count + 1            
        #print("\n\n\n\n\n\n\n")
        
        next = response.urljoin(response.xpath('//*[@id="see_older_threads"]/a/@href').extract_first())
        print("*"*25)
        print(f"fetched total {total_count} messages")
        print("*"*25)
        yield Request(next , callback= self.recipient)
        
    
    def show(self, response):
        open_in_browser(response)

