# dyson-link-status-downloader
Gets status information from a Dyson Pure air purifier e.g. 
http://www.dyson.com/air-treatment/purifiers/dyson-pure-cool-link/dyson-pure-cool-link-tower-white-silver.aspx
The Dyson Link app (https://play.google.com/store/apps/details?id=com.dyson.mobile.android&hl=en) works fine, but I wanted to archive the environment data for later analysis, so I investigated getting the data via an API. Fortunately, someone had already done this and I found  a blog post - in Japanese - which greatly shortened the process (and which you need to read to get the User Name and Password for your own Dyson Link device): 
http://aakira.hatenablog.com/entry/2016/08/12/012654

Runs on a raspberry pi on my local network. 
Analysis and backup are done separately.
