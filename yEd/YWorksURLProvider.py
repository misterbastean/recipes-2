import os
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["YWorksURLProvider"]

class YWorksURLProvider(Processor):
    """This processor obtains a download URL for the latest version of yWorks"""
    description = __doc__
    input_variables = {
        "product_name": {
	    "required": True,
	    "description":
	        "Product to fetch URL for. Right now, only 'yEd'.",
	},
    }
    output_variables = {
        "url": {
	    "description": "URL to latest version of the given product.",
	},
    }

    def main(self):
        """Provide a yWorks product download URL"""
	product_name = self.env["product_name"]
	# http://www.yworks.com/products/yed/demo/yEd-CurrentVersion.txt
	base_url = "http://www.yworks.com/products"
	check_url = "%s/%s/demo/%s-CurrentVersion.txt" % ( base_url, product_name.lower(), product_name)

	# Get the text file
	try:
	    fref = urllib2.urlopen(check_url)
	    txt = fref.read()
	    fref.close()
	except BaseException as err:
	    raise ProcessorError("Can't download %s: %s" % (check_url, err))

	# Create download link
	latest=txt.rstrip()
	base_prod_url="http://www.yworks.com/products"
	download_url = "%s/%s/demo/%s-%s_with-JRE8.dmg" % (base_prod_url, product_name.lower(), product_name, latest)
	self.env["url"] = download_url
	self.output("Found URL as %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = YWorksURLProvider()
    PROCESSOR.execute_shell()