#Import the necessary modules
import urllib.request
import datetime

#Define the default route and the blocklist URL
defaultRoute = "0.0.0.0"
blocklist = "https://cp.sync.com/mfs-60:1ae1e6ad4a678d43896bbe98cdad2510=============================/u/hosts.txt?cachekey=60:1ae1e6ad4a678d43896bbe98cdad2510=============================&datakey=GGoAPxnGoDSw8eMIEaPNgPnyJYsLopn+a6MRQCkeuXZDtnuZmvSRIZwm2RhCrSgDWAkJmdFyevblXSGWsspMbYYyTYL/FHiMWuJ7icERcW7MIiKnzDGdDA5Lx+R/XB4xDDqJyClv6w9zOtWJBi7W4oZE6cX/5MpAV900edttk0MBGzp1zjhj8sfAeoLnmBTiWqUKLjIsBhzcx1FXp5FcE6RcNmE8SAtjj0WMaCQYMPHznqxsBbrMiJFc9gvOhatF9no8V5Nlhll3oINWde6y6KV2xi+D5bGmkMbyg4VT3FIsN72gJmClopnFijNj4dJNvgejFbzyz3Zs52HpjVMhqQ&mode=101&api_version=1&header1=Q29udGVudC1UeXBlOiB0ZXh0L3BsYWlu&header2=Q29udGVudC1EaXNwb3NpdGlvbjogaW5saW5lOyBmaWxlbmFtZT0iaG9zdHMudHh0IjtmaWxlbmFtZSo9VVRGLTgnJ2hvc3RzLnR4dDs&servtime=1697643309135&engine=cp-3.1.38&userid=2016210009&deviceid=4508960009&devicetypeid=3&access_token=eb3d43fb0bd36c8168badb5244c6c37eeb183453e4f3b2dbd8d951c18c0bb234"

#Define the Zone Header for the output file
zoneHeader = """$TTL 1w ; default TTL = 1w
            ; TODO: should be adjusted to frequency of list updates
@   IN  SOA  localhost. root.localhost.(
             2019102401      ; serial yyyymmddvv
             1w              ; refresh  (match default TTL)
             1w              ; retry  (match default TTL)
             1w              ; expiry  (match default TTL)
             1d              ; negative caching
        )
    IN  NS  localhost.
;   *****   START OF BLOCKLIST *****"""

# Open the output file for writing
file = open("/etc/bind/adsblocker.db","w")

#Write the zone header to the output file  
file.write(zoneHeader + "\n")

#Get the current date and time
now = datetime.datetime.now()

#Initialize the total number of updated domains to  0
totalDomains  = 0

#Open the blocklist URL and Iterate through each line
with urllib.request.urlopen(blocklist) as f:
    for bytes in f:
        
        #Decode the line from bytes to string and remove any leading/trailing white space
        line = bytes.decode("utf-8").strip()

        #If the line starts with the default route , extract the domain
        if (line.startswith(defaultRoute)):
            #Ignore the IP address and extract the domain
            domain = line[8:]

            #If the domain is the default route or contains a comment, skip it
            if domain == defaultRoute or "#" in domain:
                continue
            #Write the domain as CNAME Record to the output file
            file.write(domain+" CNAME .\n")

            #Increment the the total number of updated domains
            totalDomains =totalDomains + 1
#Close the output file
file.close()

#Print a success message with the current daate/time and the total number of updated domains
print("List updated successfully at",now.strftime("%Y-%m-%d %H:%M:%S"),", with total updated domains", totalDomains)
