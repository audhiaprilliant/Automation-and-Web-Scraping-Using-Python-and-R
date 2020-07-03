# ===== SCRAPING FINANCIAL NEWS DATA - OKEZONE.COM =====

library(tidyverse)
library(rvest)

# FUNCTION
scrape_okezone = function(url) {
  # MAKE EMPTY VECTOR
  data_frame_title = c()
  data_frame_date = c()
  
  last_index = url %>%
    read_html() %>%
    html_nodes('div.pagination-komentar') %>%
    html_nodes('a') %>%
    html_attr('data-ci-pagination-page')
  
  index = seq(from = 10,to = (as.numeric(last_index[3]) - 1) * 10,by = 10)
  links_scroll = c(url,paste(url,index,sep = '')) # Merge main URL with index
  
  # GET LINK OF NEWS EACH 
  for (i in 1:length(links_scroll)) {
    links_loop = links_scroll[i] %>%
      read_html()
    
    # Get the title
    data_title = links_loop %>%
      html_nodes('h4.f17') %>%
      html_nodes('a') %>%
      html_text()
    
    # Get the Date
    data_date = links_loop %>%
      html_nodes('time.category-hardnews.f12') %>%
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
# Sample URL: 'https://economy.okezone.com/index/2019/10/01/'

# GET DAILY NEWS
data_date = read.csv(file = 'Date Data for Scraping - Okezone Kompas.csv',
                     header = TRUE,
                     sep = ',')
data_date$date = gsub(pattern = '-',replacement = '/',x = data_date$date)

# SCRAPING DATA
data_full_news = c()
for (k in 1:dim(data_date)[1]) {
  url_daily = paste('https://economy.okezone.com/index/',data_date[k,],'/',sep = '')
  data_news = scrape_okezone(url_daily)
  data_full_news = rbind(data_full_news,data_news)
}

# Dimension of Data
View(data_full_news)

# Save Data
write.csv(x = data_full,
          file = 'Data/Title - Financial Okezone 2019-01-01 to 2019-12-31.csv',
          row.names= FALSE)
# How to handle unused connection
CatchupPause = function(Secs){
  Sys.sleep(Secs) #pause to let connection work
  closeAllConnections()
  gc()
}
CatchupPause(Secs = 3)
