<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="2.0" exclude-result-prefixes="xsl tei xs">

    <xsl:output encoding="UTF-8" media-type="text/html" method="html" version="5.0" indent="yes"
        omit-xml-declaration="yes"/>

    <xsl:import href="partials/html_navbar.xsl"/>
    <xsl:import href="partials/html_head.xsl"/>
    <xsl:import href="partials/html_footer.xsl"/>
    <xsl:import href="partials/typesense_libs.xsl"/>
    <xsl:template match="/">
        <xsl:variable name="doc_title" select="'Linguistische Volltextsuche'"/>
        <html class="h-100" lang="{$default_lang}">
            <head>
                <xsl:call-template name="html_head">
                    <xsl:with-param name="html_title" select="$doc_title"/>
                </xsl:call-template>
                <link rel="stylesheet" href="css/search.css" type="text/css"/>
            </head>

            <body class="d-flex flex-column h-100">
                <xsl:call-template name="nav_bar"/>
                <main class="flex-shrink-0 flex-grow-1">
                    <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb"
                        class="ps-5 p-3">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item">
                                <a href="index.html">
                                    <xsl:value-of select="$project_short_title"/>
                                </a>
                            </li>
                            <li class="breadcrumb-item active" aria-current="page">
                                <xsl:value-of select="$doc_title"/>
                            </li>
                        </ol>
                    </nav>
                    <div class="container-fluid d-md-px-5 pb-4">
                        <h1 class="display-5 text-center">
                            <xsl:value-of select="$doc_title"/>
                        </h1>
                        <div class="container-fluid d-md-px-5 pb-4">
                            <div id="noske-search"></div>
                            <div id="hitsbox-test"></div>
                            <div>
                                <div id="noske-pagination-test"></div>
                                <div id="noske-stats"></div>
                            </div>
                        </div>
                    </div>
                </main>
                <xsl:call-template name="html_footer"/>
                <script type="module">
    import { NoskeSearch } from "./vendor/acdh-noske-search/index.js";
    const search = new NoskeSearch({
      container: "noske-search",
      autocomplete: false,
      wordlistattr: [
        "word",
        "lemma",
        "pos",
        "id",
        "placeName",
        "persName",
        "pbId",
        "landingPageURI"
      ],
    });

    search.minQueryLength = 2;
    search.search({
      debug: false,
      client: {
        base: "https://corpus-search.acdh.oeaw.ac.at/",
        corpname: "wienerrundschau",
        attrs: "word,lemma,pos,landingPageURI",
        structs: "sen",
        refs: "doc.id,doc.title",
      },
      hits: {
        id: "hitsbox-test",
        css: {
          div: "grid grid-cols-5 gap-4",
        },
      },
      pagination: {
        id: "noske-pagination-test",
      },
      searchInput: {
        id: "noske-input",
        placeholder:
          "Suche nach Wörter, Phrase oder CQL-Query (Regex erlaubt)",
        button: "Suchen",
      },
      config: {
        tableView: true,
        customUrlTransform: function(lines) {
          let kwic_attr = lines.kwic_attr?.split("/");
          let doc_id = kwic_attr[kwic_attr.length - 1];
          return doc_id;
        },
      },
      stats: {
        id: "noske-stats",
      },
    });
   </script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
