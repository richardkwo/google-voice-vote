google-voice-vote
=================

A SMS voting system built on Google Voice. 

Written by Richard Guo, DCSSA, Duke University

How it works
-----------

Google Voice lets you receive SMS from a virtual mobile number that Google gives to you. 
Google Voice can automatically forward all SMS received from that number to your Gmail. 
This Python script fetches SMS from Gmail, counts the votes and draws a barplot every several seconds. 

This solution proves successful for events held by [DCSSA](http://www.dukechina.org/) with ~100 people.

Dependencies
-------

* imaplib
* email
* numpy
* matplotib

Usage
-----

1. Register a Google account if you don't have one. Open Gmail and Google Voice accounts.

2. 