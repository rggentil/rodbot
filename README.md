# rodbot
The dumbest bot for cryptotrading


## Purpose

The purpose of "rodbot - the dumbest bot for cryptotrading" is not making money with crypto trading for buying lambos. The main purpose for "developing" this program is to **learn how to program better**. I'm not a code developer although I've been working in SW development for 9 years. But my role has been QA Engineer, this is testing what others do.

During my first 6 years I've been doing mostly functional black box testing and especially manual testing. However I started to feel that all about testing couldn't be mostly manual tests, but in order to achieve a better quality for the product the companies need to rely on automated tests. This need along with agile methodologies that require fast feedback on CI/CD made me put my hands on coding, first with simple scripts in bash and python and then with more professional automated testing with python.

So it's been during my last 3 years when I really learned how to program and one thing that I discovered is that I actually like it, apart of thinking that is more than necessary for today's testing. My expirience is with python's BDD framework: behave.

I was lucky to work in my Scrum team with some really good code developers colleagues that helped me a lot to learn the important things of basic coding and this also made me "open my mind" to focus my tests scenarios and to realize how code developers work and what their point of view is, empathy for understanding better the typical coder/tester disagreements.

But developing only BDD tests is not enough to learn how to program and I feel that I need to improve my coding skills and to face also typical SW tasks like SW design. This is the purpose to start this "project", I want to try to build my own program that do stuff, not just to test other's stuff.

I'd like to remark that I know that this is probably not very good code, but since my purpose is to learn I'll be happy if after some months I see that I've been able to improve it.

Some of the things I want to learn are:
- basic coding design and how to organize code
- work with APIs
- create simple servers (in this case with Flask)
- how to work with unit tests and why they are required
- how to start a BDD framework
- how to manage logging
- configure and use IDEs like PyCharm or VSC.
- use a CVS like Git/GitHub
- work with DBs
- python 3
- learn other languages like Java or Javascript
- some basics about trading (why not?)
- ...

I hope that by the end of the year (2018!!) I can say that I learned some of them.



## How to use rodbot
Up to now rodbot only performs one task, getting the volume of the pairs of an exchange and sorting them by volume.
The use of rodbot is very simple, just execute:
```
python rodbot.py -h

usage: rodbot.py [-h] [-x {cobinhood,simulator}] [-c {USD,BTC,ETH}]
                 [-i INTERVAL] [-v]

Simple script/bot to manage trading in exchanges

optional arguments:
  -h, --help            show this help message and exit
  -x {cobinhood,simulator}, --exchange {cobinhood,simulator}
                        Select exchange to operate with.
  -c {USD,BTC,ETH}, --currency {USD,BTC,ETH}
                        Select exchange to operate with.
  -i INTERVAL, --interval INTERVAL
                        checking interval
  -v, --verbosity       increase output verbosity
 ```
 
 A simple example:
 ```
 python rodbot.py -x cobinhood -c USD -i 600
 
 -trading- Top 10 pairs by volume [(u'UTNP-ETH', 105163.33164882012), (u'CMT-ETH', 90072.54242774536), (u'LYM-ETH', 88087.10082292685), (u'ETH-BTC', 71587.64046432552), (u'UTNP-BTC', 55046.710816846404), (u'COB-ETH', 43611.21613522199), (u'COB-BTC', 33014.908648198754), (u'ETH-USDT', 26002.0298957544), (u'BTC-USDT', 23265.649275408)]
 ```
 
 We'll see the result on the console and also it is logged in log/rodbot.info and the last request is stored in out/pairs_volume.json
 
 The idea is from this point to start adding more "features" like get to know more things about the pairs (depht gap, tendencies, etc) and basde on this data just to post some simple limit orders.
 
 NOTE: Currently this stupid bot only works with Cobinhood exchange.
 
