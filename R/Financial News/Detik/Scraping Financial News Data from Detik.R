# ===== SCRAPING FINANCIAL NEWS DATA - DETIK.COM =====

library(tidyverse)
library(rvest)

# FUNCTION
scrape_detik = function(url) {
  # MAKE EMPTY VECTOR
  data_frame_text = c()
  data_frame_title = c()
  data_frame_date = c()
  
  # GET LINK OF NEWS EACH 
  links_loop = url %>%
    read_html() %>%
    html_nodes('div.desc_idx.ml10') %>%
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
        html_nodes('div.detail_text') %>%
        html_text()
      # Get Title
      data_title = url_loop %>%
        html_nodes('div.jdl') %>%
        html_nodes('h1') %>%
        html_text()
      # Get the Date
      data_date = url_loop %>%
        html_nodes('div.jdl') %>%
        html_nodes('div.date') %>%
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
  data_full = data.frame(date = data_frame_date,
                         title = data_frame_title,
                         news = data_frame_text)
  return(data_full)
}
# Sample URL: 'https://finance.detik.com/indeks?date=11%2F01%2F2019'

# GET DAILY NEWS
data_date = read.csv(file = './Date Data for Scraping - Detik.csv',
                     header = TRUE,
                     sep = ',')
data_date$date = gsub(pattern = '/',replacement = '%2F',x = data_date$date)

# SCRAPING DATA
data_full_news = c()
for (k in 29:dim(data_date)[1]) {
  url_daily = paste('https://finance.detik.com/indeks?date=',data_date[k,],sep = '')
  data_news = scrape_detik(url_daily)
  data_full_news = rbind(data_full_news,data_news)
}

# Dimension of Data
View(data_full_news)

# Save Data
write.csv(x = data_news,
          file = 'Data/Financial Detik 2019-01-01 to 2019-12-31.csv',
          row.names = FALSE)
# How to handle unused connection
CatchupPause = function(Secs){
  Sys.sleep(Secs) #pause to let connection work
  closeAllConnections()
  gc()
}
CatchupPause(Secs = 3)
