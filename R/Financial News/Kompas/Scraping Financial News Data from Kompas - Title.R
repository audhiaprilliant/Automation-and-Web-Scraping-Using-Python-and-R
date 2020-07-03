# ===== SCRAPING DATA - KOMPAS.COM =====

library(tidyverse)
library(rvest)

# FUNCTION
scrape_kompas = function(url) {
  # MAKE EMPTY VECTOR
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
      read_html()
    
    # Get the title
    data_title = links_loop %>%
      html_nodes('h2.terkini__title') %>%
      html_text()
    
    # Get the Date
    data_date = links_loop %>%
      html_nodes('div.terkini__date') %>%
      html_text()
    
    if (length(data_title) == length(data_date)) {
      # APPEND THE DATA
      data_frame_title = c(data_frame_title,gsub('[\t\n]', '', data_title))
      data_frame_date = c(data_frame_date,gsub('[\t\n]', '', data_date))
    }
  }
  data_full = data.frame(date = data_frame_date,
                         title = data_frame_title)
  return(data_full)
}
# Sample URL: 'https://money.kompas.com/search/2019-03-04/'

# GET DAILY NEWS
data_date = read.csv(file = './Date Data for Scraping - Okezone Kompas.csv',
                     header = TRUE,
                     sep = ',')

# SCRAPING DATA
data_full_news = c()
for (k in 1:dim(data_date)[1]) {
  url_daily = paste('https://money.kompas.com/search/',data_date[k,],'/',sep = '')
  data_news = scrape_kompas(url_daily)
  data_full_news = rbind(data_full_news,data_news)
}

# Dimension of Data
View(data_full_news)

# Save Data
write.csv(x = data_full_news,
          file = 'Data/Title - Financial Kompas 2019-01-01 to 2019-12-31.csv',
          row.names = FALSE)
# How to handle unused connection
CatchupPause = function(Secs){
  Sys.sleep(Secs) #pause to let connection work
  closeAllConnections()
  gc()
}
CatchupPause(Secs = 4)
# 16
