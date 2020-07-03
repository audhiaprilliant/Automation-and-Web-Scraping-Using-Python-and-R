# ===== SCRAPING DATA - KOMPAS.COM =====

library(tidyverse)
library(rvest)

# FUNCTION
scrape_kompas = function(url) {
  # MAKE EMPTY VECTOR
  data_frame_text = c()
  data_frame_title = c()
  data_frame_date = c()
  
  # GET LINK OF INDEX
  # Get the Last Index
  last_index = url %>%
    read_html() %>%
    html_nodes('div.paging__item') %>%
    html_text('a.paging__link.paging__link--active')
  if (length(last_index) > 0) {
    index = seq(from = 2,to = as.numeric(last_index[length(last_index) - 1]),by = 1)
    links_scroll = c(url,paste(url,index,sep = '')) # Merge main URL with index
  }
  else {
    links_scroll = url
  }
  
  # GET LINK OF NEWS EACH 
  for (i in 1:length(links_scroll)) {
    links_loop = links_scroll[i] %>%
      read_html() %>%
      html_nodes('div.terkini__caption') %>%
      html_nodes('a') %>%
      html_attr('href')
    
    for (j in 1:length(links_loop)) {
      if (substr(x = links_loop[j],start = 1,stop = 4) == 'http') {
        tryCatch(
          {
            url_loop = links_loop[j] %>%
              read_html()
          },
          error = function(e){
            cat("ERROR :",conditionMessage(e), "\n")
          }
        )
          
          # Get Raw Text
          data_text = url_loop %>%
            html_nodes('p') %>%
            html_text()
          # Get Title
          data_title = url_loop %>%
            html_nodes('div.col-bs10-10') %>%
            html_nodes('h1') %>%
            html_text()
          # Get the Date
          data_date = url_loop %>%
            html_nodes('div.col-bs10-10') %>%
            html_nodes('div.read__time') %>%
            html_text()
      }
      else {
        data_text = ''
        data_title = ''
        data_date = ''
      }
      # APPEND THE DATA
      data_frame_text = c(data_frame_text,paste(data_text, collapse = ''))
      data_frame_title = c(data_frame_title,paste(data_title, collapse = ''))
      data_frame_date = c(data_frame_date, paste(data_date, collapse = ''))
    }
  }
  data_full = data.frame(date = data_frame_date,
                         title = data_frame_title,
                         news = data_frame_text)
  return(data_full)
}
# Sample URL: 'https://money.kompas.com/search/2019-03-04/'

# GET DAILY NEWS
data_date = read.csv(file = './Date Data for Scraping - Okezone Kompas.csv',
                     header = TRUE,
                     sep = ',')

# SCRAPING DATA
data_full_news = c()
for (k in 23:dim(data_date)[1]) {
  url_daily = paste('https://money.kompas.com/search/',data_date[k,],'/',sep = '')
  data_news = scrape_kompas(url_daily)
  data_full_news = rbind(data_full_news,data_news)
}

# Dimension of Data
dim(data_full_news)

# Save Data
write.csv(x = data_full_news,
          file = 'Data/Financial Kompas 2019-01-01 to 2019-12-31.csv',
          row.names = FALSE)
# How to handle unused connection
CatchupPause = function(Secs){
  Sys.sleep(Secs) #pause to let connection work
  closeAllConnections()
  gc()
}
CatchupPause(Secs = 4)
