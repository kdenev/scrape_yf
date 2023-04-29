<img align="center"
    src="https://cdn.vox-cdn.com/thumbor/kiURuyuTEhwsLZwGLaA5msb5Its=/0x0:2000x1333/1400x1400/filters:focal(1000x667:1001x668)/cdn.vox-cdn.com/uploads/chorus_asset/file/19224216/mb_yahoo_02.jpg">
<h1 align="center" style="font-size:35px;">Yahoo Finance Scraper</h1>

<h2 align="center" style="font-size:30px;">Equite Screener</h2>

<h3 style="font-size:25px;">Intro</h3>
<p style="font-size:18px;"> In this notebook I document my logic of a scraping bot for the yahoo finance equite scanner.
    However, the logic can be changed and applied to the ohers YF screeners.</p>
<h3 style="font-size:25px;">Basics</h3>
<p style="font-size:18px;">The link provided as input has filtered the data to use US markets and companies mid-size and
    up. Of course, the default starting point can be change to user liking. However, the bot can only scrape loop
    through filters that have selectable options(clickable check boxes).
</p>
<h3 style="font-size:18px;">Results</h3>
<p style="font-size:18px;">The script produces a csv as an output with the YF ticker, name and the selected filters
    options. The results from
    the initial run will be attached as a csv to this project, including all the US stock tickers, apart from
    small-caps, with their name, exchange and sector of operation.</p>
<h3 style="font-size:18px;">Further improvements</h3>
<ul>
    <li>Can scrape the whole information on the page including volumes and P/E ratio, rather than just company name and
        ticker.</li>
    <li>Can scrape infromation from range filters</li>
</ul>

<h3>Kaggle</h3>
<a style="font-size:18px;" href="https://www.kaggle.com/code/kdenev/yf-scraper">Scraper Project</a>
