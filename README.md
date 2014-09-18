google-voice-vote
=================

An SMS real-time voting system built on Google Voice. 

Written by Richard Guo, DCSSA, Duke University

How it works
-----------

Google Voice lets you receive SMS from a virtual mobile number that Google gives to you. 
Google Voice can automatically forward all SMS received from that number to your Gmail. 
This Python script fetches SMS from Gmail, counts the votes and draws a barplot every several seconds. 

This solution proves successful for events held by [DCSSA](http://www.dukechina.org/) with ~100 people.

Dependencies
-------

A few Python libs are required. 

* imaplib
* email
* numpy
* matplotib

Usage
-----

1. Register a Google account if you don't have one. Open Gmail and Google Voice accounts.

2. Enable "forwarding SMS to Gmail" in your Google Voice

3. Edit `acc.info`. Put your Gmail address as first row, password as second row. 
Be careful if you enabled 2-step verification. Also, watch out for security concerns.

4. Edit `vote-pattern.txt`. Each row has two fields separated with a TAB. 
The first field is the content of SMS. The second field is to whom that vote should be counted. 
For example, if one rule reads "001\tSAM", then Sam earns one vote for each "001" SMS received. 

Warning: 

* These patterns are matched from top to bottom. 
* Each number can only vote for one option. Only the first vote will be counted if a number sends more than 1 SMS. Yet, you can easily configure this behavior by editing the script!

5. Run `python vote-fetch.py`. It will prompts you with `Record a new vote (N) or continue with record (C)?`.
Choose (N) if you want to start a new vote. 
Choose (C) if you want to resume a previous voting. It will recover from `vote-record.txt` and then continue counting based on that.

6. Now check out `voting-now.png`. It is bar-plot image that is refreshed every 15 seconds. You can display a real-time voting results with an auto-refreshing image viewer!


