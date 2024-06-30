<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
>
    <xsl:output method="html" encoding="utf-8" indent="yes"/>
    <xsl:template match="/">
        <html>
        <head>
            <title><xsl:value-of select="/rss/channel/title"/></title>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }

                h1 {
                    color: #333;
                    border-bottom: 2px solid #ccc;
                    padding-bottom: 10px;
                }

                .item {
                    margin-bottom: 30px;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 20px;
                }

                .item h2 {
                    margin-bottom: 10px;
                }

                .item a {
                    color: #0066cc;
                    text-decoration: none;
                    font-weight: bold;
                }

                .item a:hover {
                    text-decoration: underline;
                }

                .description {
                    color: #555;
                    margin-top: 10px;
                }

                .date {
                    color: #888;
                    font-size: 0.9em;
                    margin-top: 5px;
                }
            </style>
        </head>
        <body>
        <h1>
            <xsl:value-of select="/rss/channel/title"/>
        </h1>
        <p>
            <xsl:value-of select="/rss/channel/description"/>
        </p>

        <xsl:for-each select="/rss/channel/item">
            <div class="item">
                <h2><a href="{link}">
                    <xsl:value-of select="title"/>
                </a></h2>
                <p class="description">
                    <xsl:value-of select="description"/>
                </p>
                <p class="date">
                    <xsl:value-of select="pubDate"/>
                </p>
            </div>
        </xsl:for-each>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>