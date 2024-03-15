---
title: "GEOMetadataDownloader"
author: "Edris Sharif Rahmani"
date: "2024-03-14"
output: pdf_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```


# Installation

```r{}
pip install GEOMetadataDownloader
```
# Running
## Provide a list of GEO series in a text file such as Accessions.txt (each accession number in a line)
## Then run the following commands

```r{}
from GEOMetadataDownloader.GEOmetadata import GEOMetadataDownloader
# Initialize the downloader
downloader = GEOMetadataDownloader()

# Start the download process with the filename containing accession numbers
downloader.download_geo_metadata("Accessions.txt")

```
