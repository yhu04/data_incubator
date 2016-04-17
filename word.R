library('wordcloud')
dm = read.csv('log_ratio.csv',header=FALSE,stringsAsFactors=FALSE,col.names=c('token','ratio'))
head(dm)

positive = dm[dm$ratio>1,]
png("Positive_word.png", width=12, height=8, units="in", res=300)
wordcloud(positive$token, round(positive$ratio*100), random.order=FALSE, colors=brewer.pal(8, "Dark2"))
dev.off()

negative = dm[dm$ratio<-1,]
png("Negative_word.png", width=12, height=8, units="in", res=300)
wordcloud(negative$token, round(negative$ratio*100), random.order=FALSE, colors=brewer.pal(8, "Dark2"))
dev.off()